from __future__ import annotations

import json

from .models import (
    GithubRepositoryOwnerModel,
    GithubStarredRepositoryModel,
    GithubStarsAPIResponseModel,
)
from .schemas import (
    GithubRepositoryOwnerIn,
    GithubRepositoryOwnerOut,
    GithubStarredRepoIn,
    GithubStarredRepoOut,
    GithubStarsAPIResponseIn,
    GithubStarsAPIResponseOut,
)

import db_lib
from depends import db_depends
from loguru import logger as log
import settings


def convert_github_stars_api_response_schema_to_db_model(
    api_response: GithubStarsAPIResponseIn,
) -> GithubStarsAPIResponseModel:
    api_response_model: GithubStarsAPIResponseModel = GithubStarsAPIResponseModel(
        json_data=api_response.json_data
    )

    return api_response_model


def convert_github_stars_api_response_db_model_to_schema(
    api_response_model: GithubStarsAPIResponseModel,
) -> GithubStarsAPIResponseOut:
    api_response: GithubStarsAPIResponseOut = GithubStarsAPIResponseOut.model_validate(
        api_response_model.__dict__
    )

    return api_response


def convert_github_starred_repo_schema_to_db_model(
    starred_repo: GithubStarredRepoIn,
) -> GithubStarredRepositoryModel:
    starred_repo_model: GithubStarredRepositoryModel = GithubStarredRepositoryModel(
        repo_id=starred_repo.id,
        node_id=starred_repo.node_id,
        name=starred_repo.name,
        description=starred_repo.description,
        html_url=starred_repo.html_url,
        stargazers_count=starred_repo.stargazers_count,
        language=starred_repo.language,
        private=starred_repo.private,
        fork=starred_repo.fork,
        url=starred_repo.url,
        forks_url=starred_repo.forks_url,
        keys_url=starred_repo.keys_url,
        collaborators_url=starred_repo.collaborators_url,
        teams_url=starred_repo.teams_url,
        hooks_url=starred_repo.hooks_url,
        issue_events_url=starred_repo.issue_events_url,
        events_url=starred_repo.events_url,
        assignees_url=starred_repo.assignees_url,
        branches_url=starred_repo.branches_url,
        tags_url=starred_repo.tags_url,
        blobs_url=starred_repo.blobs_url,
        git_tags_url=starred_repo.git_tags_url,
        git_refs_url=starred_repo.git_refs_url,
        trees_url=starred_repo.trees_url,
        statuses_url=starred_repo.statuses_url,
        languages_url=starred_repo.languages_url,
        stargazers_url=starred_repo.stargazers_url,
        contributors_url=starred_repo.contributors_url,
        subscribers_url=starred_repo.subscribers_url,
        subscription_url=starred_repo.subscription_url,
        commits_url=starred_repo.commits_url,
        git_commits_url=starred_repo.git_commits_url,
        comments_url=starred_repo.comments_url,
        issue_comment_url=starred_repo.issue_comment_url,
        contents_url=starred_repo.contents_url,
        compare_url=starred_repo.compare_url,
        merges_url=starred_repo.merges_url,
        archive_url=starred_repo.archive_url,
        downloads_url=starred_repo.downloads_url,
        issues_url=starred_repo.issues_url,
        pulls_url=starred_repo.pulls_url,
        milestones_url=starred_repo.milestones_url,
        notifications_url=starred_repo.notifications_url,
        labels_url=starred_repo.labels_url,
        releases_url=starred_repo.releases_url,
        deployments_url=starred_repo.deployments_url,
        created_at=starred_repo.created_at,
        updated_at=starred_repo.updated_at,
        pushed_at=starred_repo.pushed_at,
        git_url=starred_repo.git_url,
        has_issues=starred_repo.has_issues,
        ssh_url=starred_repo.ssh_url,
        clone_url=starred_repo.clone_url,
        svn_url=starred_repo.svn_url,
        homepage=starred_repo.homepage,
        size=starred_repo.size,
        forks_count=starred_repo.forks_count,
        open_issues_count=starred_repo.open_issues_count,
        license=starred_repo.license,
        allow_forking=starred_repo.allow_forking,
        is_template=starred_repo.is_template,
        web_commit_signoff_required=starred_repo.web_commit_signoff_required,
        topics=json.dumps(starred_repo.topics),
        visibility=starred_repo.visibility,
        forks=starred_repo.forks,
        open_issues=starred_repo.open_issues,
        watchers=starred_repo.watchers,
        default_branch=starred_repo.default_branch,
        permissions=starred_repo.permissions,
    )

    return starred_repo_model


def convert_github_starred_repo_db_model_to_schema(
    starred_repo_model: GithubStarredRepositoryModel,
) -> GithubStarredRepoOut:
    starred_repo: GithubStarredRepoOut = GithubStarredRepoOut.model_validate(
        starred_repo_model.__dict__
    )

    return starred_repo


def convert_github_repository_owner_schema_to_db_model(
    owner: GithubRepositoryOwnerIn,
) -> GithubRepositoryOwnerModel:
    owner_model: GithubRepositoryOwnerModel = GithubRepositoryOwnerModel(
        id=owner.id,
        login=owner.login,
        node_id=owner.node_id,
        avatar_url=owner.avatar_url,
        gravatar_id=owner.gravatar_id,
        url=owner.url,
        html_url=owner.html_url,
        followers_url=owner.followers_url,
        following_url=owner.following_url,
        gists_url=owner.gists_url,
        starred_url=owner.starred_url,
        subscriptions_url=owner.subscriptions_url,
        organizations_url=owner.organizations_url,
        repos_url=owner.repos_url,
        events_url=owner.events_url,
        received_events_url=owner.received_events_url,
        type=owner.type,
        site_admin=owner.site_admin,
    )

    return owner_model


def convert_github_repository_owner_db_model_to_schema(
    owner_model: GithubRepositoryOwnerModel,
) -> GithubRepositoryOwnerOut:
    owner: GithubRepositoryOwnerOut = GithubRepositoryOwnerOut.model_validate(
        owner_model.__dict__
    )

    return owner
