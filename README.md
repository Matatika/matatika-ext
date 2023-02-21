# MatatikaLab

MatatikaLab is a Meltano utility extension for the Matatika Lab

## Installing this extension for local development

1. Install the project dependencies with `poetry install`:

```shell
cd path/to/your/project
poetry install
```

2. Verify that you can invoke the extension:

```shell
poetry run matatika-lab_extension --help
poetry run matatika-lab_extension describe --format=yaml
poetry run matatika-lab_invoker --help # if you have are wrapping another tool
```
