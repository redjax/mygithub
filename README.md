# MyGithub <!-- omit in toc -->

A Python app to interact with the Github API using a [Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token).

## Table of Contents <!-- omit in toc -->

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
  - [Import into another script](#import-into-another-script)
  - [Use the CLI](#use-the-cli)
- [Supported Operations](#supported-operations)
- [Links](#links)

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

## Supported Operations

| Operation                                                                                                                                                                                  | Supported | Description                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------- | ------------------------------------------------------------------------------------------------ |
| [Get authenticated user's starred repositories](https://docs.github.com/en/rest/activity/starring?apiVersion=2022-11-28#list-repositories-starred-by-the-authenticated-user)               | `True`    | List repositories the authenticated user has starred.                                            |
| [Get a Github user's starred repositories](https://docs.github.com/en/rest/activity/starring?apiVersion=2022-11-28#list-repositories-starred-by-a-user)                                    | `False`   | List repositories starred by a specified user.                                                   |
| [Un-star a Github repository on behalf of authenticated user](https://docs.github.com/en/rest/activity/starring?apiVersion=2022-11-28#unstar-a-repository-for-the-authenticated-user)      | `False`   | Remove a repository from authenticated user's stars.                                             |
| [Star a Github repository on behalf of authenticated user](https://docs.github.com/en/rest/activity/starring?apiVersion=2022-11-28#star-a-repository-for-the-authenticated-user)           | `False`   | Add a repository to authenticated user's stars.                                                  |
| [Check if repository is starred by authenticated user](https://docs.github.com/en/rest/activity/starring?apiVersion=2022-11-28#check-if-a-repository-is-starred-by-the-authenticated-user) | `False`   | Check if a repository is in the authenticated user's list of stars.                              |
| [Get list of user's who have starred a repository](https://docs.github.com/en/rest/activity/starring?apiVersion=2022-11-28#list-stargazers)                                                | `False`   | List Github users who have starred a specified repository.                                       |
| [Get list of feeds available to authenticated user](https://docs.github.com/en/rest/activity/feeds?apiVersion=2022-11-28#get-feeds)                                                        | `False`   | List the feeds available to an authenticated user.                                               |
| [Get list of authenticated user's notifications](https://docs.github.com/en/rest/activity/notifications?apiVersion=2022-11-28#list-notifications-for-the-authenticated-user)               | `False`   | List the authenticated user's notifications.                                                     |
| [Mark notification as 'read' on behalf of user's notifications](https://docs.github.com/en/rest/activity/notifications?apiVersion=2022-11-28#mark-notifications-as-read)                   | `False`   | Mark a notification in the authenticated user's inbox as `read`.                                 |
| [Get information about a specific notification thread](https://docs.github.com/en/rest/activity/notifications?apiVersion=2022-11-28#get-a-thread)                                          | `False`   | Show information about a specified notification thread in the authenticated user's notification. |
| [Mark a thread as 'done'](https://docs.github.com/en/rest/activity/notifications?apiVersion=2022-11-28#mark-a-thread-as-done)                                                              | `False`   | Mark a specificied notification thread in a user's inbox as `done` (equivalent to `read`).       |
| [Check if a user is subscribed to a thread](https://docs.github.com/en/rest/activity/notifications?apiVersion=2022-11-28#get-a-thread-subscription-for-the-authenticated-user)             | `False`   | Check if authenticated user is subscribed to a specified notification thread.                    |
| [List branches of a repository](https://docs.github.com/en/rest/branches/branches?apiVersion=2022-11-28#list-branches)                                                                     | `False`   | List the branches of a repository.                                                               |
| [Get information about a repository's branch](https://docs.github.com/en/rest/branches/branches?apiVersion=2022-11-28#get-a-branch)                                                        | `False`   | Get information about a specific branch in a specified repository.                               |
| [Rename a repository's branch](https://docs.github.com/en/rest/branches/branches?apiVersion=2022-11-28#rename-a-branch)                                                                    | `False`   | Rename a specific branch  in a specified repository.                                             |
| [Sync a forked branch with upstream repository](https://docs.github.com/en/rest/branches/branches?apiVersion=2022-11-28#sync-a-fork-branch-with-the-upstream-repository)                   | `False`   | Sync a branch of a forked repository to keep it up to date with the upstream repository.         |
| [Merge a branch in a repository](9https://docs.github.com/en/rest/branches/branches?apiVersion=2022-11-28#merge-a-branch)                                                                  | `False`   | Merge a branch into another branch in a remote repository.                                       |
| [Get list of commits in repository](https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#list-commits)                                                                    | `False`   | Get a list of commits in a remote repository.                                                    |

## Links

- [Github docs: fine-grained Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)
- [Github API docs: get user's starred repositories](https://docs.github.com/en/rest/activity/starring?apiVersion=2022-11-28#list-repositories-starred-by-the-authenticated-user)
