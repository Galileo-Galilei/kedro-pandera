from __future__ import annotations

from typing import Any

import kedro
import pandas as pd
import pandera.pyspark as ps
import pyspark.sql.types as T
import pytest
from kedro.framework.hooks import _create_hook_manager
from kedro.framework.hooks.manager import _register_hooks
from kedro.io import DataCatalog, MemoryDataset
from kedro.pipeline import Pipeline, node, pipeline
from kedro.runner import SequentialRunner
from kedro_datasets.pandas import CSVDataset
from pandera.errors import SchemaError
from pandera.io import from_yaml
from pyspark.sql import SparkSession

from kedro_pandera.framework.hooks.pandera_hook import PanderaHook


def _get_test_catalog(csv_file, schema_file):
    test_schema = from_yaml(schema_file)

    # Check Kedro version to use appropriate catalog creation method
    kedro_version = tuple(map(int, kedro.__version__.split(".")[:2]))

    if kedro_version >= (1, 0):
        # Kedro 1.0+ uses DataCatalog.from_config
        catalog_config = {
            "iris": {
                "type": "kedro_datasets.pandas.CSVDataset",
                "filepath": csv_file,
                "metadata": {"pandera": {"schema": test_schema}},
            },
            "factory.iris": {
                "type": "MemoryDataset",
                "metadata": {"pandera": {"schema": test_schema}},
            },
        }
        test_catalog = DataCatalog.from_config(catalog_config)
    else:
        # Kedro 0.19 uses DataCatalog constructor with dataset_patterns
        test_catalog = DataCatalog(
            {
                "iris": CSVDataset(
                    filepath=csv_file,
                    metadata={"pandera": {"schema": test_schema}},
                ),
            },
            dataset_patterns={
                "{foo}.iris": {
                    "type": "MemoryDataset",
                    "metadata": {"pandera": {"schema": test_schema}},
                },
            },
        )
    return test_catalog


def _get_test_hook():
    test_hook = PanderaHook()
    return test_hook


def _run_hook(csv_file, schema_file):
    test_catalog = _get_test_catalog(csv_file, schema_file)
    test_hook = _get_test_hook()
    test_inputs = {"iris": test_catalog.load("iris")}
    test_node = node(
        name="test_node", func=lambda iris: True, inputs=["iris"], outputs=None
    )
    converted_inputs = test_hook.before_node_run(
        node=test_node,
        catalog=test_catalog,
        inputs=test_inputs,
        is_async=False,
    )
    return test_inputs, converted_inputs


def test_hook():
    _run_hook(
        csv_file="tests/data/iris.csv",
        schema_file="tests/data/iris_schema.yml",
    )


def test_hook_validation_error():
    with pytest.raises(SchemaError):
        _run_hook(
            csv_file="tests/data/iris.csv",
            schema_file="tests/data/iris_schema_fail.yml",
        )


def test_hook_unexpected_error():
    test_catalog = _get_test_catalog(
        csv_file="tests/data/iris.csv", schema_file="tests/data/iris_schema.yml"
    )
    test_hook = _get_test_hook()
    test_inputs = {"iris": []}
    test_node = node(
        name="test_node", func=lambda iris: True, inputs=["iris"], outputs=None
    )
    with pytest.raises(Exception):
        test_hook.before_node_run(
            node=test_node,
            catalog=test_catalog,
            inputs=test_inputs,
            is_async=False,
        )


def test_hook_output_validation(caplog):
    test_catalog = _get_test_catalog(
        csv_file="tests/data/iris.csv", schema_file="tests/data/iris_schema.yml"
    )
    test_hook = _get_test_hook()
    iris_data = test_catalog.load("iris")
    test_outputs = {"iris": iris_data}
    test_node = node(
        name="test_node", func=lambda: iris_data, inputs=None, outputs=["iris"]
    )
    test_hook.after_node_run(
        node=test_node,
        catalog=test_catalog,
        outputs=test_outputs,
    )
    assert caplog.text.count("successfully validated") == 1


def test_hook_factory_output_validation(caplog):
    test_catalog = _get_test_catalog(
        csv_file="tests/data/iris.csv", schema_file="tests/data/iris_schema.yml"
    )
    test_hook = _get_test_hook()
    iris_data = test_catalog.load("iris")
    test_outputs = {"factory.iris": iris_data}
    test_node = node(
        name="test_node", func=lambda: iris_data, inputs=None, outputs=["factory.iris"]
    )
    test_hook.after_node_run(
        node=test_node,
        catalog=test_catalog,
        outputs=test_outputs,
    )
    assert caplog.text.count("successfully validated") == 1


def test_validate_only_once(caplog):
    test_catalog = _get_test_catalog(
        csv_file="tests/data/iris.csv", schema_file="tests/data/iris_schema.yml"
    )
    test_hook = _get_test_hook()
    test_inputs = {"iris": test_catalog.load("iris")}
    test_node = node(
        name="test_node", func=lambda iris: True, inputs=["iris"], outputs=None
    )
    test_hook.before_node_run(
        node=test_node,
        catalog=test_catalog,
        inputs=test_inputs,
        is_async=False,
    )
    test_hook.before_node_run(
        node=test_node,
        catalog=test_catalog,
        inputs=test_inputs,
        is_async=False,
    )
    # should only be validated once
    assert caplog.text.count("successfully validated") == 1


def test_no_exception_on_memory_dataset_output():
    test_hook_manager = _create_hook_manager()
    test_hook = _get_test_hook()
    HOOKS = (test_hook,)
    _register_hooks(test_hook_manager, HOOKS)
    test_catalog = DataCatalog(
        {
            "Input": MemoryDataset("data"),
            "Output": MemoryDataset(),
        }
    )
    test_pipeline = pipeline(
        [
            node(func=lambda x: x, inputs="Input", outputs="MemOutput", name="node1"),
            node(func=lambda x: x, inputs="MemOutput", outputs="Output", name="node2"),
        ]
    )
    assert test_hook_manager.is_registered(test_hook)
    SequentialRunner().run(test_pipeline, test_catalog, hook_manager=test_hook_manager)


@pytest.fixture(scope="session")
def spark_session():
    return SparkSession.builder.master("local[*]").getOrCreate()


class TestPySparkDataframeLazyEvaluation:
    class IrisCorrectSchema(ps.DataFrameModel):
        sepal_length: T.DoubleType
        sepal_width: T.DoubleType
        petal_length: T.DoubleType
        petal_width: T.DoubleType
        species: T.StringType

    class IrisWrongSchema(ps.DataFrameModel):
        sepal_length: T.StringType

    def create_test_catalog(
        self, spark_session: SparkSession, schema: ps.DataFrameModel, lazy: bool
    ) -> DataCatalog:
        return DataCatalog(
            {
                "Input": MemoryDataset(
                    data=spark_session.createDataFrame(
                        pd.read_csv("tests/data/iris.csv")
                    ),
                    metadata={
                        "pandera": {"schema": schema, "validate_kwargs": {"lazy": lazy}}
                    },
                ),
            }
        )

    def create_test_pipeline(self) -> Pipeline:
        return pipeline(
            [node(func=lambda x: x, inputs="Input", outputs="Output", name="node1")]
        )

    def run_pipeline(self, test_catalog: DataCatalog) -> dict[str, Any]:
        test_hook_manager = _create_hook_manager()
        test_hook = _get_test_hook()
        HOOKS = (test_hook,)
        _register_hooks(test_hook_manager, HOOKS)
        test_pipeline = self.create_test_pipeline()
        assert test_hook_manager.is_registered(test_hook)
        return SequentialRunner().run(
            test_pipeline, test_catalog, hook_manager=test_hook_manager
        )

    def test_spark_dataframe_correct_schema_lazy_validation(
        self, spark_session: SparkSession
    ):
        test_catalog = self.create_test_catalog(
            spark_session, self.IrisCorrectSchema, lazy=True
        )
        self.run_pipeline(test_catalog)
        output_data = test_catalog.load("Output")
        assert len(output_data.pandera.errors) == 0

    def test_spark_dataframe_wrong_schema_lazy_validation_raises_no_error(
        self, spark_session: SparkSession
    ):
        test_catalog = self.create_test_catalog(
            spark_session, self.IrisWrongSchema, lazy=True
        )
        self.run_pipeline(test_catalog)
        output_data = test_catalog.load("Output")
        assert len(output_data.pandera.errors) > 0

    def test_spark_dataframe_wrong_schema_eager_validation_raises_error(
        self, spark_session: SparkSession
    ):
        test_catalog = self.create_test_catalog(
            spark_session, self.IrisWrongSchema, lazy=False
        )
        with pytest.raises(SchemaError):
            self.run_pipeline(test_catalog)

    def test_spark_dataframe_correct_schema_eager_validation_raises_no_error(
        self, spark_session: SparkSession
    ):
        test_catalog = self.create_test_catalog(
            spark_session, self.IrisCorrectSchema, lazy=False
        )
        self.run_pipeline(test_catalog)
        output_data = test_catalog.load("Output")
        assert len(output_data.pandera.errors) == 0
