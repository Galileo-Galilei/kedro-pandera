from kedro.io import DataCatalog
from kedro.pipeline import node
from kedro_datasets.pandas import CSVDataset
from pandera.io import from_yaml

from kedro_pandera.framework.hooks.pandera_hook import PanderaHook


def test_hook():
    test_schema = from_yaml("tests/data/iris_schema.yml")
    test_catalog = DataCatalog(
        {
            "iris": CSVDataset(
                filepath="tests/data/iris.csv",
                metadata={"pandera": {"schema": test_schema}},
            )
        }
    )
    test_hook = PanderaHook()
    test_inputs = {"iris": test_catalog.load("iris")}
    test_node = node(
        name="test_node", func=lambda iris: True, inputs=["iris"], outputs=None
    )
    test_hook.before_node_run(
        node=test_node,
        catalog=test_catalog,
        inputs=test_inputs,
        is_async=False,
        session_id=0,
    )
