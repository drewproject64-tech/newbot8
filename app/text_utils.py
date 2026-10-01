import re

def split_words(text: str) -> list[str]:
    return re.findall(r"\S+", text.strip())

def sort_words(text: str, reverse: bool = False) -> str:
    words = split_words(text)
    return "\n".join(sorted(words, key=str.casefold, reverse=reverse))

def count_text(text: str) -> tuple[int, int, int]:
    words = len(split_words(text))
    chars = len(text)
    non_space = len(re.sub(r"\s", "", text))
    return words, chars, non_space

def clean_text(text: str) -> str:
    lines = [" ".join(line.split()) for line in text.splitlines()]
    return "\n".join(line for line in lines if line).strip()
