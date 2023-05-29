from click.testing import CliRunner

from kedro_pandera.framework.cli.cli import infer_schema as cli_infer_schema


def test_schema_is_persisted(monkeypatch, kedro_project_iris):
    monkeypatch.chdir(kedro_project_iris)
    # launch the command to initialize the project
    cli_runner = CliRunner()
    result = cli_runner.invoke(cli_infer_schema, ["-d", "example_iris_data"])
    assert result.exit_code == 0
    assert (kedro_project_iris / "conf" / "local" / "example_iris_data.yml").is_file()
