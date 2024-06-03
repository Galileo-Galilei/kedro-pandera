# Changelog

## [Unreleased]

## [0.2.2] - 2024-06-03

### Added

-   :sparkles: Validate output datasets  ([#20](https://github.com/Galileo-Galilei/kedro-pandera/issues/20), [#69](https://github.com/Galileo-Galilei/kedro-pandera/issues/69))

### Fixed

-   :bug: Fix `AttributeError` in datasets with missing `metadata` parameter ([#67](https://github.com/Galileo-Galilei/kedro-pandera/issues/67))

## [0.2.1] - 2024-05-06

### Fixed

-   :bug: Fix dataset reference in hook for kedro >= 0.19.0

## [0.2.0] - 2024-04-19

### Changed

-   :boom: :sparkles: :arrow_up: Drop support for `kedro==0.18.x` and add support for `kedro==0.19.x` ([#46](https://github.com/Galileo-Galilei/kedro-pandera/issues/46))

## [0.1.0] - 2023-09-02

### Added

-   :sparkles: Add a CLI command to infer the schema of a dataset and persist it to a file ([#4](https://github.com/Galileo-Galilei/kedro-pandera/pull/4))
-   :sparkles: Automatically register customer resolvers `pa.dict`, `pa.yaml` to make schema declaration easier in the catalog  ([#13](https://github.com/Galileo-Galilei/kedro-pandera/pull/13))
-   :sparkles: Automatically register customer resolver `pa.python` to enable schema declaration in the catalog from a `DataframeModel` class ([#32](https://github.com/Galileo-Galilei/kedro-pandera/pull/32))
-   :sparkles: Add runtime validation : before running each node, data is validated against the schema declared in the catalog ([#13](https://github.com/Galileo-Galilei/kedro-pandera/pull/13))
-   :loud_sound: `kedro-pandera` logs defaults is set to `INFO` so it is visible by default in the kedro logs ([#13](https://github.com/Galileo-Galilei/kedro-pandera/pull/13))
-   :memo: Add a tutorial for using `kedro-pandera` ([#5](https://github.com/Galileo-Galilei/kedro-pandera/pull/5))

[Unreleased]: https://github.com/Galileo-Galilei/kedro-pandera/compare/0.2.2...HEAD

[0.2.2]: https://github.com/Galileo-Galilei/kedro-pandera/compare/0.2.1...0.2.2

[0.2.1]: https://github.com/Galileo-Galilei/kedro-pandera/compare/0.2.0...0.2.1

[0.2.0]: https://github.com/Galileo-Galilei/kedro-pandera/compare/0.1.0...0.2.0

[0.1.0]: https://github.com/Galileo-Galilei/kedro-pandera/compare/dcba7c128e5187c1a9b26430cddb274064ac96a4...0.1.0
