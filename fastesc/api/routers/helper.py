import re


def count_words(word: str, song_text: str, case_sensitive: bool, whole_word: bool) -> int:
    if whole_word:
        pattern = rf'\b{word}\b'
        return len(re.findall(pattern, song_text, re.IGNORECASE if not case_sensitive else 0))
    else:
        return song_text.lower().count(word.lower()) if not case_sensitive else song_text.count(word)
