from __future__ import annotations

from pathlib import Path

import click
import frictionless  # noqa: F401
import yaml
from kedro.framework.project import settings
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pandera import infer_schema
from pandera.io import serialize_schema

# if we do not import ``frictionless`` manually here, we get
# >  ImportError: ('# ERROR: failed to register fsspec file#systems', TypeError("argument of type '_Cached' is not iterable"))
# if we try to use ``Schema.to_yaml()`` after ``context.catalog``
# The command ``kedro pandera infer-schema -d example_iris_data``
# then raises the very useless error:
# > ImportError: IO and formatting requires 'pyyaml', 'black' and 'frictionless'to be installed.
# > You can install pandera together with the IO dependencies with:
# > pip install pandera[io]
# despite all the dependencies being properly installed


@click.group(name="pandera")
def commands():
    """Kedro plugin for interactions with pandera"""
    pass  # pragma: no cover


@commands.group(name="pandera")
def pandera_commands():
    """Use pandera-specific commands inside kedro project."""
    pass  # pragma: no cover


@pandera_commands.command(name="infer")
@click.option(
    "--dataset",
    "-d",
    "dataset_name",
    help="The name of the dataset whom schema will be inferred.",
)
@click.option(
    "--python/--yaml",
    "use_python_ext",
    is_flag=True,
    default=False,
    help="Should the schema be written to a 'yaml' or a 'python' file? ",
)
@click.option(
    "--env",
    "-e",
    default="base",
    help="The kedro environment where the dataset to retrieve is available. Default to 'local'",
)
@click.option(
    "--outfile",
    "-o",
    default=None,
    help="The name of the file where the schema will be stored. Its extension must be '.yml' or '.py'. Default to 'dataset_name.yml'. ",
)
def infer_dataset_schema(
    dataset_name: str,
    use_python_ext: bool = False,
    env: str = "base",
    outfile: str | None = None,
):
    """Infer the schema of a dataset and dump it in a catalog file
    so that it will enable validation at runtime.
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
        data_schema = infer_schema(data)
        file_extension = "py" if use_python_ext else "yml"
        filename = f"catalog_{dataset_name}.{file_extension}"
        # TODO: decide if we should store in env or base?
        filepath = (project_path / settings.CONF_SOURCE / env / filename).as_posix()
        if use_python_ext:
            data_schema.to_script(filepath)
        else:
            statistics = serialize_schema(data_schema)
            with open(filepath, "w", encoding="utf-8") as fhandler:
                statistics = serialize_schema(data_schema)
                yaml.safe_dump(
                    {f"_{dataset_name}_schema": statistics},
                    stream=fhandler,
                    sort_keys=False,
                )
                # data_schema.to_yaml(filepath)

        click.secho(f"The schema is written to {filepath}", fg="green")

        # TODO: should we add a metadata key to the catalog file?
        # I hate the idea of modifying a config flag on the fly,
        # but it will be very confusing for users to have to add it manually each time, and they will likely forget
        # This suggestion :https://github.com/kedro-org/kedro/issues/1076#issuecomment-1490277770
        # seems ultimately the best solution, but we need the omegaconfigloader to be more stable
        # https://github.com/kedro-org/kedro/issues/1076#issuecomment-1491008769

        # TODO: where should we store the output file? in a config folder?
        # What will happen in package mode when running with "--conf-source=path/to/conf"?

        # TODO: should we check if the file already exists before overwriting ?
        # TODO: should we compare an existing file with the inferred one to spot the differences?

        # TODO: Define if we should have a flag --py //--yml or infer from the file extension
