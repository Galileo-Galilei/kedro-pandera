# Changelog

## [Unreleased]

### Added

- :sparkles: Add a CLI command to infer the schema of a dataset and persist it to a file ([#4](https://github.com/Galileo-Galilei/kedro-pandera/pull/4))
- :sparkles: Automatically register customer resolvers ``pa.dict`` and ``pa.yaml`` to make schema declaration easier in the catalog  ([#13](https://github.com/Galileo-Galilei/kedro-pandera/pull/13))
- :sparkles: Add runtime validation : before running each node, data is validated against the schema declared in the catalog ([#13](https://github.com/Galileo-Galilei/kedro-pandera/pull/13))
- :loud_sound: ``kedro-pandera`` logs defaults is set to ``INFO`` so it is visible by default in the kedro logs ([#13](https://github.com/Galileo-Galilei/kedro-pandera/pull/13))
