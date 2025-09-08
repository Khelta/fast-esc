import pytest

from fastesc.api.routers.helper import count_words


@pytest.mark.parametrize("song_text, word, ctwt, ctwf, cfwt, cfwf", [
    ("A catastrophic cat named Catherine is always a good Cat.", "cat", 1, 2, 2, 4),
    ("A catastrophic cat named Catherine is always a good Cat.", "Cat", 1, 2, 2, 4)
])
def test_count_words(song_text, word, ctwt, ctwf, cfwt, cfwf):
    assert count_words(word, song_text, True, True) == ctwt
    assert count_words(word, song_text, True, False) == ctwf
    assert count_words(word, song_text, False, True) == cfwt
    assert count_words(word, song_text, False, False) == cfwf
