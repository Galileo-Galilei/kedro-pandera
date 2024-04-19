# DataFrameModel
`pandera` offer a class-based [DataFrameModel schema](https://pandera.readthedocs.io/en/stable/dataframe_models.html) for data validation.

## Validate with DataFrameModel

Alternatively, `pandera` support a class-based `DataFrameModel` schema.

An example of schema look like:
```python
import pandera as pa
from pandera.typing import Series


class ExampleIrisDataSchema(pa.DataFrameModel):
    sepal_length: Series[float] = pa.Field(gt=2000)
```

We suggest to create a `schemas` folder to keep things organised. You can put this in `src/kedro_pandera_tutorial/schemas/example_iris_data.py` and create a `src/kedro_pandera_tutorial/schemas/__init__.py` file.

The `__init__.py` need to import the class.

```python
from .example_iris_data import ExampleIrisDataSchema
```

The file structure should look like this:
```bash
src/kedro_pandera_tutorial/schemas/
├── __init__.py
└── example_iris_data.py
```

### Update the catalog
```yaml
example_iris_data:
  type: pandas.CSVDataset
  filepath: data/01_raw/iris.csv
  metadata:
    pandera:
      schema: ${pa.python:kedro_pandera_tutorial.schemas.ExampleIrisDataSchema}
```

Here you will use the `pa.python` resolver to resolve the Python-based schema class.
