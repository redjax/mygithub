from __future__ import annotations

from datetime import datetime
import typing as t

import db_lib
from depends import db_depends
import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import sqlalchemy.orm as so
from sqlalchemy.types import JSON


class GithubStarsAPIResponseModel(db_lib.base.Base):
    __tablename__ = "gh_stars_api_response"

    id: so.Mapped[db_lib.annotated.INT_PK]

    json_data: so.Mapped[list[dict]] = so.mapped_column(JSON, nullable=False)

    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), index=True
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), index=True
    )


class GithubStarredRepositoryModel(db_lib.base.Base):
    __tablename__ = "gh_starred_repo"
    __table_args__ = (sa.UniqueConstraint("node_id", "name", "url"),)

    # id: so.Mapped[db_lib.annotated.INT_PK]

    repo_id: so.Mapped[db_lib.annotated.INT_PK]

    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), index=True
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), index=True
    )

    owner_id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        sa.ForeignKey("gh_repo_owner.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    id: so.Mapped[int] = so.mapped_column(sa.NUMERIC, nullable=False, default=0)
    node_id: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    name: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False, index=True)
    private: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, nullable=True, default=False
    )
    html_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=True)
    fork: so.Mapped[bool] = so.mapped_column(sa.BOOLEAN, nullable=True, default=False)
    url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    forks_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    keys_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    collaborators_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    teams_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    hooks_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    issue_events_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    events_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    assignees_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    branches_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    tags_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    blobs_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    git_tags_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    git_refs_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    trees_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    statuses_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    languages_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    stargazers_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    contributors_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    subscribers_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    subscription_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    commits_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    git_commits_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    comments_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    issue_comment_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    contents_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    compare_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    merges_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    archive_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    downloads_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    issues_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    pulls_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    milestones_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    notifications_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    labels_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    releases_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    deployments_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    pushed_at: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    git_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    ssh_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    clone_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    svn_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False)
    homepage: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=True, default=None)
    size: so.Mapped[int] = so.mapped_column(
        sa.NUMERIC, nullable=False, default=0, index=True
    )
    stargazers_count: so.Mapped[int] = so.mapped_column(
        sa.NUMERIC, nullable=False, default=0, index=True
    )
    watchers_count: so.Mapped[int] = so.mapped_column(
        sa.NUMERIC, nullable=False, default=0, index=True
    )
    language: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=True, index=True)
    has_issues: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, nullable=True, default=False, index=True
    )
    has_projects: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, nullable=True, default=False
    )
    has_downloads: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, nullable=True, default=False, index=True
    )
    has_wiki: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, nullable=True, default=False, index=True
    )
    has_pages: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, nullable=True, default=False, index=True
    )
    has_discussions: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, nullable=True, default=False
    )
    forks_count: so.Mapped[int] = so.mapped_column(
        sa.NUMERIC, nullable=False, default=0, index=True
    )
    mirror_url: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=True, default=None)
    archived: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, nullable=True, default=False, index=True
    )
    disabled: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, nullable=True, default=False, index=True
    )
    open_issues_count: so.Mapped[int] = so.mapped_column(
        sa.NUMERIC, nullable=False, default=0, index=True
    )
    license: so.Mapped[dict] = so.mapped_column(JSON, nullable=True, index=True)
    allow_forking: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, nullable=True, default=False
    )
    is_template: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, nullable=True, default=False, index=True
    )
    web_commit_signoff_required: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, nullable=True, default=False
    )
    ## Storing a list of strings as JSON for cross-database support
    topics: so.Mapped[list[str]] = so.mapped_column(
        ## Store as TEXT in SQLite, JSON elsewhere
        sa.JSON().with_variant(sa.Text, "sqlite"),
        index=True,
    )
    visibility: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False, index=True)
    forks: so.Mapped[int] = so.mapped_column(
        sa.NUMERIC, nullable=False, default=0, index=True
    )
    open_issues: so.Mapped[int] = so.mapped_column(
        sa.NUMERIC, nullable=False, default=0, index=True
    )
    watchers: so.Mapped[int] = so.mapped_column(
        sa.NUMERIC, nullable=False, default=0, index=True
    )
    default_branch: so.Mapped[str] = so.mapped_column(
        sa.TEXT, nullable=False, index=True
    )
    permissions: so.Mapped[dict] = so.mapped_column(JSON, nullable=False)

    ## Relationship: Each repository has one owner
    owner: so.Mapped["GithubRepositoryOwnerModel"] = so.relationship(
        "GithubRepositoryOwnerModel", back_populates="repositories"
    )


class GithubRepositoryOwnerModel(db_lib.base.Base):
    __tablename__ = "gh_repo_owner"

    id: so.Mapped[int] = so.mapped_column(
        sa.Integer, primary_key=True, autoincrement=True
    )
    login: so.Mapped[str] = so.mapped_column(
        sa.String(255), nullable=False, unique=True, index=True
    )
    node_id: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    avatar_url: so.Mapped[str] = so.mapped_column(
        sa.String(255), nullable=True, default=None
    )
    gravatar_id: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, index=True)
    html_url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    followers_url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    following_url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    gists_url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    starred_url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    subscriptions_url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    organizations_url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    repos_url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    events_url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    received_events_url: so.Mapped[str] = so.mapped_column(
        sa.String(255), nullable=False
    )
    type: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, index=True)
    user_view_type: so.Mapped[str] = so.mapped_column(
        sa.String(255), nullable=True, default=None
    )
    site_admin: so.Mapped[bool] = so.mapped_column(
        sa.Boolean, nullable=True, default=False
    )

    # Relationship: One owner has many repositories
    repositories: so.Mapped[list["GithubStarredRepositoryModel"]] = so.relationship(
        "GithubStarredRepositoryModel",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
