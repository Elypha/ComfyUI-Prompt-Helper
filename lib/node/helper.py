import re

REGEX_MULTI_SPACE = re.compile(r"(\s|\n|\r|\t)+")


def trim_prompt_string(prompt: str) -> str:
    prompt = prompt.strip()
    prompt = REGEX_MULTI_SPACE.sub(" ", prompt)
    prompt = prompt.strip(",")
    return prompt
