import shutil

import pytest
from cookiecutter.main import cookiecutter
from kedro import __version__ as kedro_version
from kedro.framework.cli.starters import TEMPLATE_PATH

_FAKE_PACKAGE_NAME = "fake_project"
_FAKE_REPO_NAME = _FAKE_PACKAGE_NAME.replace("_", "-")


@pytest.fixture
def kedro_project(tmp_path):
    # TODO : this is also an integration test since this depends from the kedro version
    config = {
        "output_dir": tmp_path,
        "kedro_version": kedro_version,
        "project_name": _FAKE_PACKAGE_NAME.replace("_", " "),
        "repo_name": _FAKE_REPO_NAME.replace("_", "-"),
        "python_package": _FAKE_PACKAGE_NAME,
    }

    cookiecutter(
        str(TEMPLATE_PATH),
        output_dir=config["output_dir"],
        no_input=True,
        extra_context=config,
    )

    shutil.rmtree(
        config["output_dir"] / _FAKE_REPO_NAME / "src" / "tests"
    )  # avoid conflicts with pytest

    return tmp_path / _FAKE_REPO_NAME


@pytest.fixture
def kedro_project_iris(tmp_path):
    # TODO : this is also an integration test since this depends from the kedro version

    config = {
        "output_dir": tmp_path,
        "kedro_version": kedro_version,
        "project_name": _FAKE_PACKAGE_NAME.replace("_", " "),
        "repo_name": _FAKE_REPO_NAME.replace("_", "-"),
        "python_package": _FAKE_PACKAGE_NAME,
    }
    cookiecutter(
        template="git+https://github.com/kedro-org/kedro-starters.git",
        no_input=True,
        output_dir=config["output_dir"],
        directory="pandas-iris",
        extra_context=config,
    )

    shutil.rmtree(
        config["output_dir"] / _FAKE_REPO_NAME / "src" / "tests"
    )  # avoid conflicts with pytest

    return tmp_path / "fake-project"
