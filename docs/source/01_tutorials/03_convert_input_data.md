# Convert Input Data
Alongside data validation, we can utilize Pandera schemas to convert the data types of our input dataframe with those defined in the schema.


## Configuration

To ensure conversion of all datasets with a provided pandera schema, a global parameter can be set in the parameters.yml file.
```yaml
pandera:
  convert: True
```

Each dataset can be uniquely configured within the `catalog.yml`. Configurations set at the dataset level take precedence over global settings.

Example:
```yaml
example_iris_data:
  type: pandas.CSVDataset
  filepath: data/01_raw/iris.csv
  metadata:
    pandera:
      schema: ${pa.yaml:_example_iris_data_schema}
      convert: True
```


## Example

In the iris dataset the species column will be converted to object type by default when no data types are provided.

```yaml
example_iris_data:
  type: pandas.CSVDataset
  filepath: data/01_raw/iris.csv
```

Data types in the node without conversion:
```python
example_iris_data.dtypes()
```
output:
```bash
sepal_length    float64
sepal_width     float64
petal_length    float64
petal_width     float64
species          object
dtype: object
```

If we would like to convert the species column to string we can define the data type in the schema:
```yaml
...
  species:
    dtype: string
    nullable: false
...
```

And enable converting in the catalog:
```yaml
example_iris_data:
  type: pandas.CSVDataset
  filepath: data/01_raw/iris.csv
  metadata:
    pandera:
      schema: ${pa.yaml:_example_iris_data_schema}
      convert: True
```

Now the data type in the node will be according to the schema
```python
example_iris_data.dtypes()
```
output:
```bash
sepal_length           float64
sepal_width            float64
petal_length           float64
petal_width            float64
species         string[python]
dtype: object
```
