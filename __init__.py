from .lib.node.const import *
from .lib.node.format import *
from .lib.node.preset import *
from .lib.node.weight import *
from .lib.custom_server import *
from .lib.node.file_io import *
from .lib.preset import PresetManager

NODE_CLASS_MAPPINGS = {
    "PromptHelper_String": PromptHelper_String,
    "PromptHelper_StringMultiLine": PromptHelper_StringMultiLine,
    "PromptHelper_WeightedPrompt": PromptHelper_WeightedPrompt,
    "PromptHelper_LoadPreset": PromptHelper_LoadPreset,
    "PromptHelper_LoadPresetAdvanced": PromptHelper_LoadPresetAdvanced,
    "PromptHelper_EncodeMultiStringCombine": PromptHelper_EncodeMultiStringCombine,
    "PromptHelper_ConcatString": PromptHelper_ConcatString,
    "PromptHelper_ConcatConditioning": PromptHelper_ConcatConditioning,
    "PromptHelper_CombineConditioning": PromptHelper_CombineConditioning,
    "PromptHelper_FormatString": PromptHelper_FormatString,
    "PromptHelper_LoadImageBatchFromDir": PromptHelper_LoadImageBatchFromDir,
    "PromptHelper_LoadImageListFromDir": PromptHelper_LoadImageListFromDir,
    "PromptHelper_SaveImageToDir": PromptHelper_SaveImageToDir,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptHelper_String": "String",
    "PromptHelper_StringMultiLine": "String (multi-line)",
    "PromptHelper_WeightedPrompt": "Weighted Prompt",
    "PromptHelper_LoadPreset": "Load Preset",
    "PromptHelper_LoadPresetAdvanced": "Load Preset (Advanced)",
    "PromptHelper_EncodeMultiStringCombine": "Encode (multi-str)",
    "PromptHelper_ConcatString": "Concat (str)",
    "PromptHelper_ConcatConditioning": "Concat (cond)",
    "PromptHelper_CombineConditioning": "Combine (cond)",
    "PromptHelper_FormatString": "Format (str)",
    "PromptHelper_LoadImageBatchFromDir": "Load Image Batch (dir)",
    "PromptHelper_LoadImageListFromDir": "Load Image List (dir)",
    "PromptHelper_SaveImageToDir": "Save Image (dir)",
}

WEB_DIRECTORY = "./scripts"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
