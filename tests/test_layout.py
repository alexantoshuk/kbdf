"""Tests for keyboard layout helpers."""

from unittest.mock import patch

from kbdf.layout import guess_layout, switch_to_match_text


def test_guess_layout_russian():
    assert guess_layout("привет") == "ru"
    assert guess_layout("Привет, мир!") == "ru"


def test_guess_layout_english():
    assert guess_layout("hello") == "en"
    assert guess_layout("Hello, World!") == "en"


def test_guess_layout_mixed_prefers_majority():
    assert guess_layout("hello мир") == "en"
    assert guess_layout("привет world") == "ru"


def test_guess_layout_no_letters():
    assert guess_layout("") is None
    assert guess_layout("123\n\t") is None


def test_switch_to_match_text_windows():
    with patch("kbdf.layout.sys.platform", "win32"):
        with patch("kbdf.layout._windows_set_layout", return_value=True) as set_mock:
            assert switch_to_match_text("привет") is True
            set_mock.assert_called_once_with("ru")


def test_switch_to_match_text_windows_english():
    with patch("kbdf.layout.sys.platform", "win32"):
        with patch("kbdf.layout._windows_set_layout", return_value=True) as set_mock:
            assert switch_to_match_text("hello") is True
            set_mock.assert_called_once_with("en")


def test_switch_to_match_text_skips_without_letters():
    with patch("kbdf.layout._windows_set_layout") as set_mock:
        assert switch_to_match_text("!!!") is False
        set_mock.assert_not_called()
