from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter
from kedro import __version__ as kedro_version
from kedro.framework.cli.starters import TEMPLATE_PATH

# cloned with version 0.18.12
# modified to have configloader by default
# removed tests to avoid pytest conflicts
PANDAS_IRIS_PATH = (Path(__file__).parent / "_data" / "pandas-iris").as_posix()

_FAKE_PROJECT_NAME = "fake project"
_FAKE_REPO_NAME = "fake-project"
_FAKE_PACKAGE_NAME = "fake_project"


@pytest.fixture
def kedro_project(tmp_path):
    # TODO : this is also an integration test since this depends from the kedro version
    config = {
        "output_dir": tmp_path,
        "kedro_version": kedro_version,
        "repo_name": _FAKE_REPO_NAME,
        "project_name": _FAKE_PROJECT_NAME,
        "python_package": _FAKE_PACKAGE_NAME,
    }

    cookiecutter(
        str(TEMPLATE_PATH),
        output_dir=config["output_dir"],
        no_input=True,
        extra_context=config,
        accept_hooks=False,
    )
    return tmp_path / _FAKE_REPO_NAME


@pytest.fixture
def kedro_project_iris(tmp_path):
    # TODO : this is also an integration test since this depends from the kedro version

    config = {
        "output_dir": tmp_path,
        "kedro_version": kedro_version,
        "repo_name": _FAKE_REPO_NAME,
        "project_name": _FAKE_PROJECT_NAME,
        "python_package": _FAKE_PACKAGE_NAME,
    }
    cookiecutter(
        template=PANDAS_IRIS_PATH,
        output_dir=config["output_dir"],
        no_input=True,
        extra_context=config,
    )

    return tmp_path / _FAKE_REPO_NAME
