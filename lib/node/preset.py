import json

import numpy as np

from .base import BaseNode
from ..preset import PresetManager, PresetManagerAdvanced
from .helper import trim_prompt_string

import folder_paths


class PromptHelper_LoadPreset(BaseNode):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string": ("STRING", {"default": "", "multiline": True}),
                "preset": (list(PresetManager.get_presets().keys()),),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "load_preset"

    def load_preset(self, string, preset):
        prompt_1 = trim_prompt_string(string)
        prompt_2 = trim_prompt_string(PresetManager.get_preset(preset))
        prompt = trim_prompt_string(f"{prompt_1}, {prompt_2}")
        return (prompt,)


class PromptHelper_LoadPresetAdvanced(BaseNode):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "preset": (list(PresetManagerAdvanced.get_presets().keys()),),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", folder_paths.get_filename_list("loras"), "FLOAT", "FLOAT", "LORA_STACK")
    RETURN_NAMES = ("positive prompt", "negative prompt", "lora name", "strength model", "strength clip", "lora stack")
    FUNCTION = "load_preset"

    def load_preset(self, preset):
        preset_ = PresetManagerAdvanced.get_preset(preset)
        positive_prompt, negative_prompt, lora_name, strength_model, sterngth_clip, lora_stack = PresetManagerAdvanced.parse_preset(preset_)

        return (positive_prompt, negative_prompt, lora_name, strength_model, sterngth_clip, lora_stack)
