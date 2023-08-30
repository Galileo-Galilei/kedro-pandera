# DataFrameModel

Alternatively, `pandera` support a class-based `DataFrameModel` schema.

An example of schema look like:
```python
import pandera as pa
from pandera.typing import Series

class ExampleIrisDataSchema(pa.DataFrameModel):
    sepal_length: Series[float] = pa.Field(gt=2000)

```

You should put this in `src/<kedro_pandera_tutorial/schema/example_iris_data.py` and create a `src/kedro_pandera_tutorial/schema/example_iris_data/__init__.py` file.

the `__init__.py` need to import the class.

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
  type: pandas.CSVDataSet
  filepath: data/01_raw/iris.csv
  metadata:
    pandera:
      schema: ${pa.python:kedro_pandera_tutorial.schemas.ExampleIrisDataSchema}
```

Here you will use the `pa.python` resolver to resolve the Python-based schema class.