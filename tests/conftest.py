import shutil

import pytest
from cookiecutter.main import cookiecutter
from kedro import __version__ as kedro_version
from kedro.framework.cli.starters import TEMPLATE_PATH

_FAKE_PROJECT_NAME = "fake_project"


@pytest.fixture
def kedro_project(tmp_path):
    # TODO : this is also an integration test since this depends from the kedro version
    config = {
        "output_dir": tmp_path,
        "kedro_version": kedro_version,
        "project_name": _FAKE_PROJECT_NAME.replace("_", " "),
        "repo_name": _FAKE_PROJECT_NAME.replace("_", "-"),
        "python_package": _FAKE_PROJECT_NAME,
        "include_example": True,
    }

    cookiecutter(
        str(TEMPLATE_PATH),
        output_dir=config["output_dir"],
        no_input=True,
        extra_context=config,
    )

    shutil.rmtree(
        tmp_path / "fake-project" / "src" / "tests"
    )  # avoid conflicts with pytest

    return tmp_path / "fake-project"


@pytest.fixture
def kedro_project_iris(tmp_path):
    # TODO : this is also an integration test since this depends from the kedro version
    config = {
        "output_dir": tmp_path,
        "kedro_version": kedro_version,
        "project_name": _FAKE_PROJECT_NAME.replace("_", " "),
        "repo_name": _FAKE_PROJECT_NAME.replace("_", "-"),
        "python_package": _FAKE_PROJECT_NAME,
        "include_example": True,
    }

    cookiecutter(
        str(TEMPLATE_PATH),
        output_dir=config["output_dir"],
        no_input=False,
        extra_context=config,
    )

    shutil.rmtree(
        tmp_path / "fake-project" / "src" / "tests"
    )  # avoid conflicts with pytest

    return tmp_path / "fake-project"
