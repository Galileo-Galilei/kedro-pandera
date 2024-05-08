import pandas as pd
from kedro.io import DataCatalog
from kedro.pipeline import node
from kedro_datasets.pandas import CSVDataset
from pandera.io import from_yaml

from kedro_pandera.framework.hooks.pandera_hook import PanderaHook


def _run_hook(csv_file, schema_file, convert=False):
    test_schema = from_yaml(schema_file)
    test_catalog = DataCatalog(
        {
            "iris": CSVDataset(
                filepath=csv_file,
                metadata={"pandera": {"schema": test_schema, "convert": convert}},
            )
        }
    )
    test_hook = PanderaHook()
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


def test_hook_with_converting():
    test_inputs, converted_inputs = _run_hook(
        csv_file="tests/data/iris.csv",
        schema_file="tests/data/iris_schema.yml",
        convert=True,
    )
    # test if species column is converted to string type
    assert ~isinstance(
        test_inputs["iris"].dtypes["species"], pd.core.arrays.string_.StringDtype
    )
    assert isinstance(
        converted_inputs["iris"].dtypes["species"],
        pd.core.arrays.string_.StringDtype,
    )
