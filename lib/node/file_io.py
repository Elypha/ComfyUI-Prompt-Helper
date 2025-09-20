import json
import re
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageOps
from PIL.PngImagePlugin import PngInfo

from comfy.cli_args import args

VALID_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]
SORT_METHODS = [
    "None",
    "As Text (Asc)",
    "As Text (Desc)",
    "As Number (Asc)",
    "As Number (Desc)",
    "Time Modified (ASC)",
    "Time Modified (DESC)",
]


def sort_files(image_files: list[Path], method: str | None = None):
    if method is None or method == "None":
        return image_files

    def as_number(s):
        if match := re.search(r"\d+", s):
            return int(match.group())
        return sys.maxsize

    if method == "As Text (Asc)":
        return sorted(image_files)
    elif method == "As Text (Desc)":
        return sorted(image_files, reverse=True)
    elif method == "As Number (Asc)":
        return sorted(image_files, key=lambda x: as_number(x.stem))
    elif method == "As Number (Desc)":
        return sorted(image_files, key=lambda x: as_number(x.stem), reverse=True)
    elif method == "Time Modified (ASC)":
        return sorted(image_files, key=lambda x: x.stat().st_mtime)
    elif method == "Time Modified (DESC)":
        return sorted(image_files, key=lambda x: x.stat().st_mtime, reverse=True)
    else:
        raise ValueError(f"Unknown sort method: {method}")


def load_image_to_tensor(image_path: Path) -> tuple[Image.Image, torch.Tensor]:
    # from comfyui `class LoadImage` at nodes.py, modified to general purpose function
    image = Image.open(image_path)
    image = ImageOps.exif_transpose(image)
    image_rgb = image.convert("RGB")
    image_array = np.array(image_rgb).astype(np.float32) / 255.0
    tensor = torch.from_numpy(image_array)[None,]
    return image, tensor


def get_mask_from_image(image: Image.Image) -> torch.Tensor:
    # from comfyui `class LoadImage` at nodes.py
    if "A" in image.getbands():
        mask = np.array(image.getchannel("A")).astype(np.float32) / 255.0
        mask = 1.0 - torch.from_numpy(mask)
    elif image.mode == "P" and "transparency" in image.info:
        mask = np.array(image.convert("RGBA").getchannel("A")).astype(np.float32) / 255.0
        mask = 1.0 - torch.from_numpy(mask)
    else:
        mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
    return mask


class PromptHelper_LoadImageBatchFromDir:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
            },
            "optional": {
                "skips": ("INT", {"default": 0, "min": 0, "max": sys.maxsize, "step": 1}),
                "sort_by": (SORT_METHODS,),
                "trim_suffix": ("BOOLEAN", {"default": False, "tooltip": "If enabled, FILENAMES output will have the file suffix removed."}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK", "INT", "STRING")
    RETURN_NAMES = ("IMAGE", "MASK", "COUNT", "FILENAMES")
    FUNCTION = "load_images"
    CATEGORY = "image"
    DESCRIPTION = "Loads all images from a directory as a single batch. All images must have the same dimensions."

    def load_images(self, directory: str, skips: int = 0, sort_by=None, trim_suffix=False):
        input_dir = Path(directory)
        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory '{directory}' does not exist.")
        if not input_dir.is_dir():
            raise NotADirectoryError(f"Input path '{directory}' is not a directory.")

        image_files = [file for file in input_dir.rglob("*") if file.suffix.lower() in VALID_IMAGE_EXTENSIONS]
        image_files = sort_files(image_files, sort_by)
        if skips > 0:
            image_files = image_files[skips:]
        if len(image_files) == 0:
            raise FileNotFoundError(f"No image files found in directory '{directory}'.")

        image_tensors = []
        mask_tensors = []
        image_count = 0
        target_shape = None
        for image_path in image_files:
            image, tensor = load_image_to_tensor(image_path)
            mask = get_mask_from_image(image)

            # Ensure all images have the same dimensions
            if target_shape is None:
                target_shape = tensor.shape[1:3]  # (height, width)
            if tensor.shape[1:3] != target_shape:
                raise ValueError(f"All images must have the same dimensions. Expected {target_shape}, but got {tensor.shape[1:3]} for file '{image_path.name}'.")

            image_tensors.append(tensor)
            mask_tensors.append(mask)
            image_count += 1

        final_images = torch.cat(image_tensors, dim=0)
        final_masks = torch.cat([m.unsqueeze(0) for m in mask_tensors], dim=0)
        count = len(image_tensors)
        filenames = [p.stem if trim_suffix else p.name for p in image_files]

        return (final_images, final_masks, count, filenames)


class PromptHelper_LoadImageListFromDir:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
            },
            "optional": {
                "skips": ("INT", {"default": 0, "min": 0, "max": sys.maxsize, "step": 1}),
                "sort_by": (SORT_METHODS,),
                "trim_suffix": ("BOOLEAN", {"default": False, "tooltip": "If enabled, FILENAMES output will have the file suffix removed."}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK", "INT", "STRING")
    RETURN_NAMES = ("IMAGE", "MASK", "INDEX", "FILENAMES")
    OUTPUT_IS_LIST = (True, True, True, True)
    FUNCTION = "load_images"
    CATEGORY = "image"
    DESCRIPTION = "Loads all images from a directory as a list of individual images."

    def load_images(self, directory: str, skips: int = 0, sort_by=None, trim_suffix=False):
        input_dir = Path(directory)
        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory '{directory}' does not exist.")
        if not input_dir.is_dir():
            raise NotADirectoryError(f"Input path '{directory}' is not a directory.")

        image_files = [file for file in input_dir.rglob("*") if file.suffix.lower() in VALID_IMAGE_EXTENSIONS]
        image_files = sort_files(image_files, sort_by)
        if skips > 0:
            image_files = image_files[skips:]
        if len(image_files) == 0:
            raise FileNotFoundError(f"No image files found in directory '{directory}'.")

        image_tensors = []
        mask_tensors = []
        image_count = 0
        for image_path in image_files:
            image, tensor = load_image_to_tensor(image_path)
            mask = get_mask_from_image(image)

            image_tensors.append(tensor)
            mask_tensors.append(mask)
            image_count += 1

        indices = list(range(len(image_files)))
        filenames = [p.stem if trim_suffix else p.name for p in image_files]

        return (image_tensors, mask_tensors, indices, filenames)


class PromptHelper_SaveImageToDir:
    def __init__(self):
        self.type = "output"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "directory": ("STRING",),
            },
            "optional": {
                "sub_directory": ("STRING", {"default": ""}),
                "filenames": ("STRING", {"default": ""}),
                "compress_level": ("INT", {"default": 4, "min": 0, "max": 9, "step": 1, "tooltip": "PNG compression level (0-9). 0 = no compression, 9 = maximum compression."}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "save_images"
    CATEGORY = "image"
    DESCRIPTION = "Saves images to a specified directory with optional metadata."

    def save_images(
        self,
        images: list[torch.Tensor],
        directory="",
        sub_directory="",
        filenames: str | list[str] = None,
        prompt=None,
        extra_pnginfo=None,
        compress_level=4,
    ):
        results = list()
        print(f"Saving {len(images)} images to directory: {directory} {sub_directory}, filenames: {filenames}")
        for index, image in enumerate(images):
            # from comfyui `class SaveImage` at nodes.py
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            output_dir = Path(directory)
            if sub_directory:
                output_dir = output_dir / sub_directory

            if isinstance(filenames, str):
                filename = filenames.strip()
            elif isinstance(filenames, list):
                filename = filenames[index].strip()
            if not filename:
                filename = str(index)

            output_file = output_dir / f"{filename}.png"
            output_file.parent.mkdir(parents=True, exist_ok=True)

            img.save(output_file, pnginfo=metadata, compress_level=compress_level)
            results.append({"filename": output_file.name, "subfolder": output_file.parent.as_posix(), "type": self.type})

        return {"ui": {"images": results}}
