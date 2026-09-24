"""Tests for Windows autostart helpers."""

import pytest

from kbdf.autostart import AutostartError, install, installed_scripts, uninstall


def test_install_copies_kbdf_ahk(tmp_path, monkeypatch):
    startup = tmp_path / "Startup"
    startup.mkdir()

    monkeypatch.setattr("kbdf.autostart.sys.platform", "win32")
    monkeypatch.setattr("kbdf.autostart.startup_dir", lambda: startup)

    paths = install()
    assert len(paths) == 1
    assert paths[0].name == "kbdf.ahk"
    assert (startup / "kbdf.ahk").is_file()


def test_uninstall_removes_scripts(tmp_path, monkeypatch):
    startup = tmp_path / "Startup"
    startup.mkdir()

    monkeypatch.setattr("kbdf.autostart.sys.platform", "win32")
    monkeypatch.setattr("kbdf.autostart.startup_dir", lambda: startup)

    install()
    removed = uninstall()
    assert not installed_scripts(startup)
    assert removed


def test_install_rejects_non_windows(monkeypatch):
    monkeypatch.setattr("kbdf.autostart.sys.platform", "linux")
    with pytest.raises(AutostartError):
        install()
