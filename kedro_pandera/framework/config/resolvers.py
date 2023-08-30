from omegaconf import Container
from omegaconf.resolvers.oc import select
from pandera import DataFrameSchema
from pandera.io import deserialize_schema


# will be registered as pa.dict
def resolve_yaml_schema(schema: str) -> DataFrameSchema:
    # intended use in catalog is :
    # schema: ${pa.dict:${oc.select:_example_iris_data_schema,null}}

    # This will fail (e.g. with the CLI "kedro pandera infer") if the key does not exist yet, that's why we need a default "null"
    pandera_schema = deserialize_schema(schema)
    return pandera_schema


# will be registered as pa.yaml
def resolve_interpolated_yaml_schema(
    key: str, *, _parent_: Container
) -> DataFrameSchema:
    # the goal is to simplify pa.dict to avoid a complex combination of resolvers
    #  base way with resolve_yaml_schema : ${pa.dict:${oc.select:_example_iris_data_schema,null}}
    # simplified way with resolve_interpolated_yaml_schema : ${pa.yaml:_example_iris_data_schema}

    schema = select(key, default=None, _parent_=_parent_)
    pandera_schema = resolve_yaml_schema(schema)
    return pandera_schema


def resolve_dataframe_model(schema_name):
    import importlib

    module, _, schema = schema_name.rpartition(".")
    module = importlib.import_module(module)
    return getattr(module, schema)
