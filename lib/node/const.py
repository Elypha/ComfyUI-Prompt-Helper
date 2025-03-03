from .base import BaseNode
from .helper import trim_prompt_string


class PromptHelper_StringBase(BaseNode):
    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_string"

    def get_string(self, string: str):
        return (trim_prompt_string(string),)


class PromptHelper_String(PromptHelper_StringBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "multiline": False}),
            }
        }


class PromptHelper_StringMultiLine(PromptHelper_StringBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": "", "multiline": True}),
            }
        }
