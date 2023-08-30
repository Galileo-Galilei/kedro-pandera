from contextlib import contextmanager
import pandera as pa
import pytest
import yaml
from omegaconf import OmegaConf
from pandera import DataFrameModel, DataFrameSchema
from pandera.errors import SchemaDefinitionError
from pandera.typing import Series
from kedro_pandera.framework.config.resolvers import (
    resolve_interpolated_yaml_schema,
    resolve_yaml_schema,
    resolve_dataframe_model,
)
import sys


@contextmanager
def register_temporary_resolver(name, resolver):
    _flag_restore = True if OmegaConf.has_resolver(name) else False
    if _flag_restore:
        old_resolver = OmegaConf._get_resolver(name)

    OmegaConf.register_new_resolver(name, resolver, replace=True)

    yield

    if _flag_restore:
        OmegaConf.register_new_resolver(name, old_resolver, replace=True)
    else:
        OmegaConf.clear_resolver(name)


MINIMAL_SCHEMA_EXAMPLE = yaml.safe_load(
    """
schema_type: dataframe
version: 0.16.1
columns:
sepal_length:
    title: null
    description: null
    dtype: float64
    nullable: false
    checks:
    greater_than_or_equal_to: 4.3
    less_than_or_equal_to: 7.9
    unique: false
    coerce: false
    required: true
    regex: false
checks: null
index:
- title: null
description: null
dtype: int64
nullable: false
checks:
    greater_than_or_equal_to: 0.0
    less_than_or_equal_to: 149.0
name: null
unique: false
coerce: false
dtype: null
coerce: true
strict: false
name: null
ordered: false
unique: null
report_duplicates: all
unique_column_names: false
add_missing_columns: false
title: null
description: null
"""
)


def test_resolve_yaml_schema():
    df_schema = resolve_yaml_schema(MINIMAL_SCHEMA_EXAMPLE)
    assert isinstance(df_schema, DataFrameSchema)


def test_resolve_yaml_schema_fails_with_invalid_yaml():
    with pytest.raises(SchemaDefinitionError):
        _ = resolve_yaml_schema("foobar")


def test_resolve_yaml_schema_works_as_resolver():
    # maybe not a useful test: after all, this is OmegaConf responsibility
    with register_temporary_resolver("pa.dict", resolve_yaml_schema):
        config = OmegaConf.create(
            {
                "my_data": {
                    "type": "pandas.CSVDataSet",
                    "filepath": "path/to/data.csv",
                    "metadata": {
                        "pandera": {
                            "schema": "${pa.dict:${oc.select:_data_schema,null}}",
                        }
                    },
                },
                "_data_schema": MINIMAL_SCHEMA_EXAMPLE,
            }
        )
        assert isinstance(config.my_data.metadata.pandera.schema, DataFrameSchema)


def test_resolve_interpolated_yaml_schema():
    config = OmegaConf.create(
        {
            "my_data": {
                "type": "pandas.CSVDataSet",
                "filepath": "path/to/data.csv",
                "metadata": {
                    "pandera": {
                        "schema": "${_data_schema}",
                    }
                },
            },
            "_data_schema": MINIMAL_SCHEMA_EXAMPLE,
        }
    )
    df_schema = resolve_interpolated_yaml_schema("_data_schema", _parent_=config)
    assert isinstance(df_schema, DataFrameSchema)


@pytest.fixture
def dummy_module(mocker):
    sys.modules["dummy"] = mocker.Mock()  # This is the easiest way to mock a module
    sys.modules["dummy.schema"] = mocker.Mock()
    yield
    del sys.modules["dummy"]
    del sys.modules["dummy.schema"]


def test_resolve_dataframe_model(mocker, monkeypatch, dummy_module):
    # assert True
    import dummy.schema

    fake_model = mocker.Mock()
    monkeypatch.setattr(dummy.schema, "dataframe_model", fake_model)
    fake_model = mocker.Mock()
    mock_model = "dummy.schema.dataframe_model"
    model = resolve_dataframe_model(mock_model)
    assert model == fake_model
