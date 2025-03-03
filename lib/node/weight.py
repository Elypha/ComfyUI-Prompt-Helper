import re

from .base import BaseNode
from .helper import trim_prompt_string


class PromptHelper_WeightedPrompt(BaseNode):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt_1": ("STRING", {"default": "", "multiline": True}),
                "weight_1": ("FLOAT", {"default": 1.0, "min": -100, "max": 100, "step": 0.1}),
            },
            "optional": {
                "prompt_2": ("STRING", {"default": "", "multiline": True}),
                "weight_2": ("FLOAT", {"default": 1.0, "min": -100, "max": 100, "step": 0.1}),
                "prompt_3": ("STRING", {"default": "", "multiline": True}),
                "weight_3": ("FLOAT", {"default": 1.0, "min": -100, "max": 100, "step": 0.1}),
                "prompt_4": ("STRING", {"default": "", "multiline": True}),
                "weight_4": ("FLOAT", {"default": 1.0, "min": -100, "max": 100, "step": 0.1}),
                "prompt_5": ("STRING", {"default": "", "multiline": True}),
                "weight_5": ("FLOAT", {"default": 1.0, "min": -100, "max": 100, "step": 0.1}),
                "weight": ("STRING", {"default": "", "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)

    FUNCTION = "get_weighted_prompts"

    """
    NOTE:
    1.  Explicit weight, like (cat:1.25) is final weight, i.e., ignores all brackets.
        e.g., `((cat:1.25), dog, bird:0.5)` equals to `cat:1.25, dog:0.5, bird:0.5`
    """

    def get_weighted_prompts(self, **kwargs):
        overall_weight = float(kwargs.get("weight", 1.0))

        prompts = []
        for i in [1, 2, 3, 4, 5]:
            prompt = trim_prompt_string(kwargs[f"prompt_{i}"])
            weight = kwargs[f"weight_{i}"]
            if prompt == "" or weight == 0.0:
                continue
            if (final_weight := weight * overall_weight) == 1.0:
                prompts.append(prompt)
            else:
                prompts.append(f"({prompt}:{final_weight:.3f})")

        prompts_str = ", ".join(prompts)
        return (prompts_str,)
