import pytest
from kedro.io import DataCatalog
from kedro.io.memory_dataset import MemoryDataset
from kedro.pipeline import node
from kedro_datasets.pandas import CSVDataset
from pandera.errors import SchemaError
from pandera.io import from_yaml

from kedro_pandera.framework.hooks.pandera_hook import PanderaHook


def _get_test_catalog(csv_file, schema_file, convert=False):
    test_schema = from_yaml(schema_file)
    test_catalog = DataCatalog(
        {
            "iris": CSVDataset(
                filepath=csv_file,
                metadata={"pandera": {"schema": test_schema, "convert": convert}},
            ),
            "params:pandera": MemoryDataset(data={"convert": False}),
        }
    )
    return test_catalog


def _get_test_hook(test_catalog):
    test_hook = PanderaHook()
    return test_hook


def _run_hook(csv_file, schema_file, convert=False):
    test_catalog = _get_test_catalog(csv_file, schema_file, convert)
    test_hook = _get_test_hook(test_catalog)
    test_inputs = {"iris": test_catalog.load("iris")}
    test_node = node(
        name="test_node", func=lambda iris: True, inputs=["iris"], outputs=None
    )
    converted_inputs = test_hook.before_node_run(
        node=test_node,
        catalog=test_catalog,
        inputs=test_inputs,
        is_async=False,
        session_id=0,
    )
    return test_inputs, converted_inputs


def test_hook():
    _run_hook(
        csv_file="tests/data/iris.csv",
        schema_file="tests/data/iris_schema.yml",
        convert=False,
    )


def test_hook_validation_error():
    with pytest.raises(SchemaError):
        _run_hook(
            csv_file="tests/data/iris.csv",
            schema_file="tests/data/iris_schema_fail.yml",
            convert=False,
        )


def test_hook_unexpected_error():
    test_catalog = _get_test_catalog(
        csv_file="tests/data/iris.csv", schema_file="tests/data/iris_schema.yml"
    )
    test_hook = _get_test_hook(test_catalog)
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
            session_id=0,
        )


def test_hook_output_validation():
    test_catalog = _get_test_catalog(
        csv_file="tests/data/iris.csv", schema_file="tests/data/iris_schema.yml"
    )
    test_hook = _get_test_hook(test_catalog)
    test_outputs = {"iris": test_catalog.load("iris")}
    test_node = node(
        name="test_node", func=lambda iris: True, inputs=["iris"], outputs=None
    )
    test_hook.after_node_run(
        node=test_node,
        catalog=test_catalog,
        outputs=test_outputs,
    )
