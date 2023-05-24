from pathlib import Path
from typing import Optional

import click
import pandera as pa
from kedro.framework.project import settings
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project


@click.group(name="Pandera")
def commands():
    """Kedro plugin for interactions with pandera"""
    pass  # pragma: no cover


@commands.command(name="pandera")
def pandera_commands():
    """Use pandera-specific commands inside kedro project."""
    pass  # pragma: no cover


@pandera_commands.command()
@click.option(
    "--dataset",
    "-d",
    "dataset_name",
    help="The name of the dataset whom schema will be inferred.",
)
@click.option(
    "--env",
    "-e",
    default="local",
    help="The kedro environment where the dataset to retrieve is available. Default to 'local'",
)
@click.option(
    "--filename",
    "-f",
    default=None,
    help="The name of the file where the schema will be stored. Its extension must be '.yml' or '.py'. Default to 'dataset_name.yml'. ",
)
def infer_schema(dataset_name: str, env: str = "local", filename: Optional[str] = None):
    """Opens the mlflow user interface with the
    project-specific settings of mlflow.yml. This interface
    enables to browse and compares runs.
    """

    project_path = Path().cwd()
    bootstrap_project(project_path)
    with KedroSession.create(
        project_path=project_path,
        env=env,
    ) as session:
        context = session.load_context()
        catalog = context.catalog
        data = catalog.load(dataset_name)
        data_schema = pa.infer_schema(data)

        filename = filename or f"{dataset_name}.yml"
        # TODO: decide if we should store in env or base?
        filepath = (project_path / settings.CONF_SOURCE / env / filename).as_posix()
        if filename.endswith(".py"):
            data_schema.to_script(filepath)
        else:
            data_schema.to_yaml(filepath)

        # TODO: should we add a metadata key to the catalog file?
        # I hate the idea of modifying a config flag on the fly,
        # but it will be very confusing for users to have to add it manually each time, and they will likely forget
        # This suggestion :https://github.com/kedro-org/kedro/issues/1076#issuecomment-1490277770
        # seems ultimately the best solution, but we need the omegaconfigloader to be more stable
        # https://github.com/kedro-org/kedro/issues/1076#issuecomment-1491008769

        # TODO: where should we store the output file? in a config folder?
        # What will happen in package mode when running with "--conf-source=path/to/conf"?
