import subprocess
from unittest.mock import patch, MagicMock
import pytest
from typing import Set
from ..pip_install import check_pip_installed, install_lib


@patch("shutil.which")
def test_pip_installed_success(mock_which):
    mock_which.return_value = "/usr/bin/pip3"
    assert check_pip_installed() is True


@patch("shutil.which")
def test_pip_installed_failure(mock_which):
    mock_which.return_value = None
    assert check_pip_installed() is False


@patch("subprocess.run")
@patch("os.path.exists")
@patch("builtins.open", new_callable=MagicMock)
def test_install_lib_success_new_file(mock_open, mock_exists, mock_run):
    mock_exists.side_effect = [False, False]  # requirements не существует
    mock_run.return_value = MagicMock(
        returncode=0, stdout="Successfully installed requests", stderr=""
    )

    libs_list: Set[str] = set()
    install_lib("requests", libs_list)

    mock_run.assert_called_once_with(
        [__import__("sys").executable, "-m", "pip", "install", "requests"],
        check=True,
        text=True,
        capture_output=True,
    )

    mock_open.assert_any_call("requirements.txt", "w", encoding="utf-8")
    mock_open.assert_any_call("requirements.txt", "a", encoding="utf-8")
    assert "requests" in libs_list


@patch("subprocess.run")
@patch("os.path.exists")
def test_install_lib_already_installed(mock_exists, mock_run):
    mock_exists.return_value = True
    mock_run.return_value = MagicMock(
        returncode=0, stdout="Requirement already satisfied: requests in ...", stderr=""
    )

    libs_list: Set[str] = {"requests"}
    install_lib("requests", libs_list)

    assert mock_run.called is True
    assert len(libs_list) == 1


@patch("subprocess.run")
def test_install_lib_failure(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(
        1,
        ["pip3", "install", "xxx"],
        stderr="No matching distribution found",
    )

    libs_list: Set[str] = set()
    with pytest.raises(subprocess.CalledProcessError):
        install_lib("xxx", libs_list)
