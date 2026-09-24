"""Tests for app helpers that do not need a real clipboard/keyboard."""

from unittest.mock import patch

from kbdf.app import ClipboardError, run
from kbdf.translate import translate as pure_translate


def test_run_rejects_bad_mode():
    assert run(mode="words") == 2


def test_run_line_with_selection():
    with patch("kbdf.app.clipboard_paste", side_effect=["backup", "ghbdtn"]):
        with patch("kbdf.app.clipboard_copy") as copy_mock:
            with patch("kbdf.app.copy_selection", return_value="ghbdtn"):
                with patch("kbdf.app.insert_text") as insert_mock:
                    with patch("kbdf.app.switch_keyboard_layout") as switch_mock:
                        with patch("kbdf.app.select_line") as select_mock:
                            assert run(mode="line", switch_layout=True) == 0
                            select_mock.assert_not_called()
                            insert_mock.assert_called_once_with("привет")
                            switch_mock.assert_called_once_with("привет")
                            assert copy_mock.call_args_list[-1].args[0] == "backup"


def test_run_line_selects_when_no_selection():
    with patch("kbdf.app.clipboard_paste", return_value="backup"):
        with patch("kbdf.app.clipboard_copy"):
            with patch(
                "kbdf.app.copy_selection", side_effect=["", "ghbdtn"]
            ) as copy_sel:
                with patch("kbdf.app.insert_text") as insert_mock:
                    with patch("kbdf.app.switch_keyboard_layout"):
                        with patch("kbdf.app.select_line") as select_mock:
                            assert run(mode="line", switch_layout=False) == 0
                            select_mock.assert_called_once()
                            insert_mock.assert_called_once_with("привет")
                            assert copy_sel.call_args_list[0].kwargs.get(
                                "expect_text"
                            ) is False
                            assert copy_sel.call_args_list[1].kwargs.get(
                                "expect_text"
                            ) is True


def test_run_selection_does_not_expand_to_line():
    with patch("kbdf.app.clipboard_paste", return_value=""):
        with patch("kbdf.app.clipboard_copy"):
            with patch("kbdf.app.copy_selection", return_value=""):
                with patch("kbdf.app.insert_text") as insert_mock:
                    with patch("kbdf.app.switch_keyboard_layout") as switch_mock:
                        with patch("kbdf.app.select_line") as select_mock:
                            assert run(mode="selection", switch_layout=True) == 0
                            select_mock.assert_not_called()
                            insert_mock.assert_not_called()
                            switch_mock.assert_not_called()


def test_run_skips_layout_switch_when_disabled():
    with patch("kbdf.app.clipboard_paste", return_value=""):
        with patch("kbdf.app.clipboard_copy"):
            with patch("kbdf.app.copy_selection", return_value="a"):
                with patch("kbdf.app.insert_text"):
                    with patch("kbdf.app.switch_keyboard_layout") as switch_mock:
                        assert run(mode="selection", switch_layout=False) == 0
                        switch_mock.assert_not_called()


def test_run_clipboard_error_returns_1():
    with patch("kbdf.app.clipboard_paste", return_value="backup"):
        with patch(
            "kbdf.app.copy_selection", side_effect=ClipboardError("fail")
        ):
            with patch("kbdf.app.clipboard_copy") as copy_mock:
                assert run(mode="line") == 1
                copy_mock.assert_called_with("backup")


def test_copy_selection_probe_returns_empty_without_spinning():
    with patch("kbdf.app.clipboard_copy"):
        with patch("kbdf.app._hotkey"):
            with patch("kbdf.app.clipboard_paste", return_value="") as paste_mock:
                with patch("kbdf.app._sleep") as sleep_mock:
                    from kbdf.app import copy_selection

                    assert copy_selection(expect_text=False) == ""
                    assert paste_mock.call_count == 1
                    # no extra sleeps from empty-clipboard polling
                    sleep_mock.assert_not_called()


def test_pure_translate_matches_package():
    assert pure_translate("ghbdtn") == "привет"
