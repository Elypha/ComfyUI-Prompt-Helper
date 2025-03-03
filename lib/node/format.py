import torch

from .base import BaseNode
from .helper import trim_prompt_string


class PromptHelper_FormatString(BaseNode):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "pattern": ("STRING", {"default": "[1], [2]"}),
            },
            "optional": {
                "str_1": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "format"

    def format(self, pattern: str, **kwargs):
        for i in range(1, len(kwargs) + 1):
            pattern = pattern.replace(f"[{i}]", kwargs[f"str_{i}"])
        return (pattern,)


class PromptHelper_JoinString(BaseNode):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "sep": ("STRING", {"default": ","}),
            },
            "optional": {
                "str_1": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "join"

    def join(self, sep: str, **kwargs):
        result = f"{sep.strip()} ".join([trim_prompt_string(x) for x in kwargs.values() if x])
        return (result,)


class PromptHelper_StringToConditioningCombine(BaseNode):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"default": "", "multiline": True, "tooltip": "Separate different parts of the conditioning with a newline."}),
                "clip": ("CLIP", {"tooltip": "The CLIP model used for encoding the text."}),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "combine"

    # def combine(self, conditioning_1, conditioning_2):
    #     return (conditioning_1 + conditioning_2, )

    def combine(self, clip, text: str):
        if clip is None:
            raise RuntimeError("ERROR: clip input is invalid: None\n\nIf the clip is from a checkpoint loader node your checkpoint does not contain a valid clip or text encoder model.")
        # split text
        parts = text.split("\n")
        parts = [trim_prompt_string(part) for part in parts]
        while "" in parts:
            parts.remove("")
        # encode parts
        parts_tokens = [clip.tokenize(part) for part in parts]
        parts_encoded = [clip.encode_from_tokens_scheduled(tokens) for tokens in parts_tokens]
        # combine parts
        base_conditioning = parts_encoded[0]
        if len(parts_encoded) > 1:
            for part in parts_encoded[1:]:
                base_conditioning += part
        return (base_conditioning,)


class PromptHelper_ConditioningConcat(BaseNode):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "to": ("CONDITIONING",),
                "from": ("CONDITIONING",),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "concat"

    def concat(self, **kwargs):
        _to = kwargs["to"]
        _from = kwargs["from"]

        if len(_from) > 1:
            raise RuntimeError("Warning: ConditioningConcat conditioning_from contains more than 1 cond, only the first one will actually be applied to conditioning_to.")
        cond_from = _from[0][0]

        out = []
        for i in range(len(_to)):
            t1 = _to[i][0]
            tw = torch.cat((t1, cond_from), 1)
            n = [tw, _to[i][1].copy()]
            out.append(n)

        return (out,)


class PromptHelper_ConditioningCombine(BaseNode):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "cond_1": ("CONDITIONING",),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "combine"

    def combine(self, **kwargs):
        base_conditioning = kwargs.get("cond_1", None)
        if base_conditioning is None:
            return (None,)
        for i in range(2, len(kwargs) + 1):
            cond = kwargs.get(f"cond_{i}", None)
            if cond is not None:
                base_conditioning += cond
        return (base_conditioning,)
