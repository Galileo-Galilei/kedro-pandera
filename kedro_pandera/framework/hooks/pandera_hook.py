import logging
from typing import Any, Dict

from kedro.framework.context import KedroContext
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro.pipeline.node import Node
from pandera.errors import SchemaError

from kedro_pandera.framework.config.resolvers import (
    resolve_dataframe_model,
    resolve_interpolated_yaml_schema,
    resolve_yaml_schema,
)

# if we do not import ``frictionless`` manually here, we get
# >  ImportError: ('# ERROR: failed to register fsspec file#systems', TypeError("argument of type '_Cached' is not iterable"))
# if we try to use ``Schema.to_yaml()`` after ``context.catalog``
# The command ``kedro pandera infer-schema -d example_iris_data``
# then raises the very useless error:
# > ImportError: IO and formatting requires 'pyyaml', 'black' and 'frictionless'to be installed.
# > You can install pandera together with the IO dependencies with:
# > pip install pandera[io]
# despite all the dependencies being properly installed


class PanderaHook:
    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    @hook_impl
    def after_context_created(
        self,
        context: KedroContext,
    ) -> None:
        """Hooks to be invoked after a `KedroContext` is created. This is the earliest
        hook triggered within a Kedro run. The `KedroContext` stores useful information
        such as `credentials`, `config_loader` and `env`.
        Args:
            context: The context that was created.
        """
        context.config_loader._register_new_resolvers(
            {
                "pa.dict": resolve_yaml_schema,
                "pa.yaml": resolve_interpolated_yaml_schema,
                "pa.python": resolve_dataframe_model,
            }
        )

    def _validate_datasets(
        self, node: Node, catalog: DataCatalog, datasets: Dict[str, Any]
    ):
        for name, data in datasets.items():
            if (
                catalog._datasets[name].metadata is not None
                and "pandera" in catalog._datasets[name].metadata
            ):
                try:
                    catalog._datasets[name].metadata["pandera"]["schema"].validate(data)
                except SchemaError as err:
                    self._logger.error(
                        f"Dataset '{name}' pandera validation failed before running '{node.name}', see details in the error message. "
                    )
                    raise err
                except Exception as err:
                    self._logger.error(
                        f"Dataset '{name}' validation raised an unknown error before running '{node.name}'"
                    )
                    raise err

                self._logger.info(
                    f"(kedro-pandera) Dataset '{name}' was successfully validated with pandera"
                )

    @hook_impl
    def before_node_run(  # noqa : PLR0913
        self,
        node: Node,
        catalog: DataCatalog,
        inputs: Dict[str, Any],
        is_async,
        session_id,
    ):
        return self._validate_datasets(node, catalog, inputs)

    @hook_impl
    def after_node_run(self, node: Node, catalog: DataCatalog, outputs: Dict[str, Any]):
        return self._validate_datasets(node, catalog, outputs)


pandera_hook = PanderaHook()
