"""Tests for CLI argument parsing."""

from unittest.mock import patch

import pytest

from kbdf.cli import build_parser, main, _normalize_argv


def test_normalize_default_is_run():
    assert _normalize_argv([]) == ["run"]


def test_normalize_legacy_mode():
    assert _normalize_argv(["selection"]) == ["run", "selection"]
    assert _normalize_argv(["--no-layout-switch"]) == ["run", "--no-layout-switch"]


def test_parser_run_defaults():
    args = build_parser().parse_args(["run"])
    assert args.command == "run"
    assert args.mode == "line"
    assert args.no_layout_switch is False


def test_parser_selection_mode():
    args = build_parser().parse_args(["run", "selection"])
    assert args.mode == "selection"


def test_parser_no_layout_switch():
    args = build_parser().parse_args(["run", "--no-layout-switch"])
    assert args.no_layout_switch is True


def test_parser_rejects_unknown_mode():
    with pytest.raises(SystemExit):
        build_parser().parse_args(["run", "word"])


def test_main_passes_switch_layout_false_from_flag():
    with patch("kbdf.cli.run", return_value=0) as run_mock:
        assert main(["--no-layout-switch"]) == 0
        run_mock.assert_called_once_with(mode="line", switch_layout=False)


def test_main_passes_switch_layout_false_from_env(monkeypatch):
    monkeypatch.setenv("KBDF_NO_LAYOUT_SWITCH", "1")
    with patch("kbdf.cli.run", return_value=0) as run_mock:
        assert main([]) == 0
        run_mock.assert_called_once_with(mode="line", switch_layout=False)


def test_main_selection_mode():
    with patch("kbdf.cli.run", return_value=0) as run_mock:
        assert main(["selection"]) == 0
        run_mock.assert_called_once_with(mode="selection", switch_layout=True)


def test_main_autostart_install():
    with patch("kbdf.cli.install", return_value=["C:\\Startup\\kbdf.ahk"]):
        with patch("kbdf.cli.find_autohotkey", return_value=None):
            assert main(["autostart", "install"]) == 0


def test_main_autostart_status():
    with patch("kbdf.cli.status_lines", return_value=["ok"]):
        assert main(["autostart", "status"]) == 0
