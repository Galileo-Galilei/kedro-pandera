import pytest
from click.testing import CliRunner

from kedro_pandera.framework.cli.cli import infer_schema as cli_infer_schema


@pytest.mark.parametrize("flag_extension", ["--python", "--yaml"])
def test_schema_is_persisted_with_correct_extension(
    monkeypatch, kedro_project_iris, flag_extension
):
    monkeypatch.chdir(kedro_project_iris)
    # launch the command to initialize the project
    cli_runner = CliRunner()
    result = cli_runner.invoke(
        cli_infer_schema, ["-d", "example_iris_data", flag_extension]
    )
    file_extension = "py" if flag_extension == "--python" else "yml"

    assert result.exit_code == 0
    assert (
        kedro_project_iris / "conf" / "local" / f"example_iris_data.{file_extension}"
    ).is_file()
