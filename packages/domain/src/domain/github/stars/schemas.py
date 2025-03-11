from __future__ import annotations

from datetime import datetime
import typing as t

from loguru import logger as log
from pydantic import BaseModel, Field, ValidationError, computed_field, field_validator


class GithubStarsAPIResponseBase(BaseModel):
    json_data: t.List[t.Dict[str, t.Any]] = Field(default_factory=[], repr=False)

    @computed_field
    @property
    def stars_count(self) -> int:
        if self.json_data:
            return len(self.json_data)
        else:
            return 0


class GithubStarsAPIResponseIn(GithubStarsAPIResponseBase):
    pass


class GithubStarsAPIResponseOut(GithubStarsAPIResponseBase):
    id: int

    created_at: datetime
    updated_at: datetime


class GithubRepositoryOwnerBase(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    user_view_type: str
    site_admin: bool


class GithubRepositoryOwnerIn(GithubRepositoryOwnerBase):
    pass


class GithubRepositoryOwnerOut(GithubRepositoryOwnerBase):
    repo_owner_id: int


class GithubStarredRepoBase(BaseModel):
    id: int
    node_id: str
    name: str
    private: bool
    owner: GithubRepositoryOwnerBase | None = Field(default=None)
    html_url: str
    description: str | None = Field(default=None)
    fork: bool
    url: str
    forks_url: str
    keys_url: str
    collaborators_url: str
    teams_url: str
    hooks_url: str
    issue_events_url: str
    events_url: str
    assignees_url: str
    branches_url: str
    tags_url: str
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: str
    stargazers_url: str
    contributors_url: str
    subscribers_url: str
    subscription_url: str
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: str
    archive_url: str
    downloads_url: str
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: str
    created_at: str
    updated_at: str
    pushed_at: str
    git_url: str
    ssh_url: str
    clone_url: str
    svn_url: str
    homepage: str | None = Field(default=None)
    size: int
    stargazers_count: int
    watchers_count: int
    language: str | None = Field(default=None)
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    forks_count: int
    mirror_url: str | None = Field(default=None)
    archived: bool
    disabled: bool
    open_issues_count: int
    license: dict | None = Field(default_factory={})
    allow_forking: bool
    is_template: bool
    web_commit_signoff_required: bool
    topics: t.List[str] | str | None = Field(default_factory=[])
    visibility: str
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    permissions: dict


class GithubStarredRepoIn(GithubStarredRepoBase):
    pass


class GithubStarredRepoOut(GithubStarredRepoBase):
    repo_id: int

    created_at: str
    updated_at: str
