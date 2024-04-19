import re

from click.testing import CliRunner

from kedro_pandera.framework.cli.cli import pandera_commands as cli_pandera


def extract_cmd_from_help(msg):
    # [\s\S] is used instead of "." to match any character including new lines
    cmd_txt = re.search((r"(?<=Commands:)([\s\S]+)$"), msg).group(1)
    cmd_list_detailed = cmd_txt.split("\n")

    cmd_list = []
    for cmd_detailed in cmd_list_detailed:
        cmd_match = re.search(r"[\w-]+(?=  )", string=cmd_detailed)
        if cmd_match is not None:
            cmd_list.append(cmd_match.group(0))
    return cmd_list


def test_pandera_commands_inside_kedro_project(monkeypatch, kedro_project):
    monkeypatch.chdir(kedro_project)
    # launch the command to initialize the project
    cli_runner = CliRunner()
    result = cli_runner.invoke(cli_pandera)
    assert {"infer"} == set(extract_cmd_from_help(result.output))
