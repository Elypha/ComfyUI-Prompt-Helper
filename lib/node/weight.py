import re

from .base import BaseNode
from .helper import trim_prompt_string


class PromptHelper_WeightedPrompt(BaseNode):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "prompt_1": ("STRING", {"default": "", "multiline": True}),
                "weight_1": ("FLOAT", {"default": 1.0, "min": 0, "max": 2, "step": 0.1}),
                "prompt_2": ("STRING", {"default": "", "multiline": True}),
                "weight_2": ("FLOAT", {"default": 1.0, "min": 0, "max": 2, "step": 0.1}),
                "prompt_3": ("STRING", {"default": "", "multiline": True}),
                "weight_3": ("FLOAT", {"default": 1.0, "min": 0, "max": 2, "step": 0.1}),
                "multiplier": ("FLOAT", {"default": 1.0, "min": 0, "max": 2, "step": 0.1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)

    FUNCTION = "get_weighted_prompts"

    """
    NOTE:
    1.  Explicit weight, like (cat:1.25) is final weight, i.e., ignores all brackets.
        e.g., `((cat:1.25), dog, bird:0.5)` equals to `cat:1.25, dog:0.5, bird:0.5`
    """

    def get_weighted_prompts(self, **kwargs):
        multiplier = float(kwargs.get("multiplier", 1.0))

        prompts = []
        for i in [1, 2, 3]:
            prompt = trim_prompt_string(kwargs[f"prompt_{i}"])
            weight = kwargs[f"weight_{i}"]
            if prompt == "" or weight == 0.0:
                continue
            final_weight = weight * multiplier
            if final_weight == 1.0:
                prompts.append(prompt)
            else:
                prompts.append(f"({prompt}:{final_weight:.3f})")

        prompts_str = ", ".join(prompts)
        return (prompts_str,)
