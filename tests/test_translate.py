"""Tests for EN ↔ RU layout translation."""

from kbdf import __version__
from kbdf.translate import EN, RU, EN_RU, translate


def test_tables_same_length():
    assert len(EN) == len(RU)


def test_tables_no_duplicate_keys():
    assert len(EN) == len(set(EN))
    assert len(RU) == len(set(RU))


def test_translate_empty_and_whitespace():
    assert translate("") == ""
    assert translate("   ") == "   "
    assert translate("\n\t") == "\n\t"


def test_translate_english_to_russian():
    assert translate("ghbdtn") == "привет"
    assert translate("Ghbdtn") == "Привет"
    assert translate("QWERTY") == "ЙЦУКЕН"


def test_translate_russian_to_english():
    assert translate("руддщ") == "hello"
    assert translate("Руддщ") == "Hello"
    assert translate("привет") == "ghbdtn"


def test_translate_is_involutive_for_letters():
    samples = [
        "Hello, World!",
        "Привет, мир!",
        "mix MIX микс",
        "asdfghjkl",
        "фывапролдж",
    ]
    for sample in samples:
        assert translate(translate(sample)) == sample


def test_translate_preserves_unmapped_chars():
    text = "hello 123\n\t@*"
    # digits and some punctuation stay; letters swap
    out = translate(text)
    assert "123" in out
    assert "\n" in out
    assert "\t" in out
    assert translate(out) == text


def test_translate_multiline():
    src = "ghbdtn\nvbh"
    assert translate(src) == "привет\nмир"


def test_maketrans_roundtrip_all_mapped():
    assert EN.translate(EN_RU) == RU
    assert RU.translate(EN_RU) == EN


def test_version_format():
    parts = __version__.split(".")
    assert len(parts) >= 2
    assert all(p.isdigit() for p in parts)
