# Changelog

## [Unreleased]

## [0.1.0] - 2023-09-02

### Added

-   :sparkles: Add a CLI command to infer the schema of a dataset and persist it to a file ([#4](https://github.com/Galileo-Galilei/kedro-pandera/pull/4))
-   :sparkles: Automatically register customer resolvers `pa.dict`, `pa.yaml` to make schema declaration easier in the catalog  ([#13](https://github.com/Galileo-Galilei/kedro-pandera/pull/13))
-  :sparkles: Automatically register customer resolver `pa.python` to enable schema declaration in the catalog from a ``DataframeModel`` class ([#32](https://github.com/Galileo-Galilei/kedro-pandera/pull/32))
-   :sparkles: Add runtime validation : before running each node, data is validated against the schema declared in the catalog ([#13](https://github.com/Galileo-Galilei/kedro-pandera/pull/13))
-   :loud_sound: `kedro-pandera` logs defaults is set to `INFO` so it is visible by default in the kedro logs ([#13](https://github.com/Galileo-Galilei/kedro-pandera/pull/13))
-   :memo: Add a tutorial for using `kedro-pandera` ([#5](https://github.com/Galileo-Galilei/kedro-pandera/pull/5))

[Unreleased]: https://github.com/Galileo-Galilei/kedro-pandera/compare/0.1.0...HEAD

[0.1.0]: https://github.com/Galileo-Galilei/kedro-pandera/compare/dcba7c128e5187c1a9b26430cddb274064ac96a4...0.1.0
