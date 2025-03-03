from .lib.node.const import *
from .lib.node.format import *
from .lib.node.preset import *
from .lib.node.weight import *
from .lib.custom_server import *
from .lib.preset import PresetManager

NODE_CLASS_MAPPINGS = {
    "PromptHelper_String": PromptHelper_String,
    "PromptHelper_StringMultiLine": PromptHelper_StringMultiLine,
    "PromptHelper_FormatString": PromptHelper_FormatString,
    "PromptHelper_JoinString": PromptHelper_JoinString,
    "PromptHelper_StringToConditioningCombine": PromptHelper_StringToConditioningCombine,
    "PromptHelper_ConditioningConcat": PromptHelper_ConditioningConcat,
    "PromptHelper_ConditioningCombine": PromptHelper_ConditioningCombine,
    "PromptHelper_LoadPreset": PromptHelper_LoadPreset,
    "PromptHelper_LoadPresetAdvanced": PromptHelper_LoadPresetAdvanced,
    "PromptHelper_WeightedPrompts": PromptHelper_WeightedPrompts,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptHelper_String": "String",
    "PromptHelper_StringMultiLine": "String (multi line)",
    "PromptHelper_FormatString": "Format String",
    "PromptHelper_JoinString": "Join String",
    "PromptHelper_StringToConditioningCombine": "String to Conditioning Combine",
    "PromptHelper_ConditioningConcat": "Concat Conditioning",
    "PromptHelper_ConditioningCombine": "Combine Conditioning",
    "PromptHelper_LoadPreset": "Load Preset",
    "PromptHelper_LoadPresetAdvanced": "Load Preset (Advanced)",
    "PromptHelper_WeightedPrompts": "Prompt Weight",
}

WEB_DIRECTORY = "./scripts"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
