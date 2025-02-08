# MyGithub <!-- omit in toc -->

A Python app to interact with the Github API using a [Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token).

## Requirements

- [Astral `uv`](https://docs.astral.sh/uv)

## Setup

- Install the project with `uv sync --dev`
  - This will create your `.venv` and install all dependencies
- Copy [configuration files](./config) to `*.local.toml` versions
  - Configurations with `.local` are ignored by git because they may contain secrets or deployment-specific configurations
  - Note: There is a [`nox` session](./noxfile.py) you can use to do this: `nox -s init-clone-setup`.
  - Make sure to edit the values, i.e. in the [`.secrets.local.toml` file](./config/.secrets.toml)

## Usage

### Import into another script

You can `import mygh` to use this package in another script. The [`GithubAPIController` class](./src/mygh/controllers/_controllers.py) and the [`mygh.client`](./src/mygh/client/) packages have most/all of the functionality needed to interact with the Github API.

### Use the CLI

The project includes a [`cli.py` script](./cli.py), which calls the [`mygh.cli.py`](./src/mygh/cli.py) package to expose entrypoints into the application via CLI. You can run `python cli.py --help` to see options and help text.

## Links

- [Github docs: fine-grained Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)
- [Github API docs: get user's starred repositories](https://docs.github.com/en/rest/activity/starring?apiVersion=2022-11-28#list-repositories-starred-by-the-authenticated-user)
