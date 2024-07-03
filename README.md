# Database Entity Relationship diagram (ERD) as Mermaid format

## Dev setup (using mise)

Install [mise](https://github.com/jdx/mise) and activate it.

```sh
mise activate
```

It will install the required tools in *.mise.toml* namely poetry and python.

Now you can run the following commands

```sh
poetry env use 3.11.9
poetry install --all-extras --with dev
poetry shell
```

## Run tests

Pytest is a dev dependency of this project.

```sh
poetry run pytest
```

The tests leverages [testcontainers](https://github.com/testcontainers/testcontainers-python) to you would need docker to be installed on your systeM

## Dev Container

A [dev container](.devcontainer.Dockerfile) is provided for ci purpose, it's an alternative to setup your dev environment.

## Github action

[ga_test.yaml](.github/workflows/ga_test.yaml) provides an example of how the github action can be used

You would need to add to your existing github worklow the following.

```yaml
- name: ERD action step
  uses: ndesaunais/erd-ga@master
  id: erd
  with:
    url: postgresql://user:passwd@host:port/db_name
    output: out.mmd

```

This github action requires:

- **url**, a database url in the format `postgresql://user:passwd@host:port/db_name` that enables connection to a running datbase
- **output**, a filepath where to generate the mermaid file

[ga_test.yaml](.github/workflows/ga_test.yaml) provides an example of how to run a database as a github action service and how to provide the correct url

The **output** can be used by the ci to generate a commit and dump the new updated schema. To access the content of the file in the following step, you can use `${{ github.workspace }}/out.mmd`.

## Todos

- [ ] Generate a docker image to prevent checkout
- [ ] Use an appropriate mermaid generator
