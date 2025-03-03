from __future__ import annotations

import typing as t

from .models import (
    GithubRepositoryOwnerModel,
    GithubStarredRepositoryModel,
    GithubStarsAPIResponseModel,
)

import db_lib
from loguru import logger as log
import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import sqlalchemy.orm as so


class GithubStarsAPIResponseRepository(
    db_lib.base.BaseRepository[GithubStarsAPIResponseModel]
):
    def __init__(self, session: so.Session):
        super().__init__(session, GithubStarsAPIResponseModel)


class GithubStarredRepositoryDBRepository(
    db_lib.base.BaseRepository[GithubStarredRepositoryModel]
):
    def __init__(self, session: so.Session):
        super().__init__(session, GithubStarredRepositoryModel)

    def create_or_get_repo(
        self,
        github_repo: GithubStarredRepositoryModel,
        repo_owner: GithubRepositoryOwnerModel,
    ) -> GithubStarredRepositoryModel:
        """Creates a new repository and owner if they don't exist.
        If a repository already exists, return it.
        If an owner exists but the repository does not, update the owner.
        """
        try:
            ## Check if repository already exists
            existing_repo: GithubStarredRepositoryModel | None = (
                self.session.query(GithubStarredRepositoryModel)
                .filter(GithubStarredRepositoryModel.repo_id == github_repo.repo_id)
                .one_or_none()
            )

            if existing_repo:
                log.debug(
                    f"Existing repository found with repo_id '{github_repo.repo_id}'. Returning model"
                )
                return existing_repo

            ## Check if owner exists
            existing_repo_owner: GithubRepositoryOwnerModel | None = (
                self.session.query(GithubRepositoryOwnerModel)
                .filter(GithubRepositoryOwnerModel.id == repo_owner.id)
                .one_or_none()
            )

            if existing_repo_owner:
                log.info(
                    f"Existing owner found with owner_id '{repo_owner.id}'. Checking if repository '{github_repo.repo_id}' is already linked to this owner"
                )

                ## Check if repository exists in owner's .repositories
                for repo in existing_repo_owner.repositories:
                    if repo.repo_id == github_repo.repo_id:
                        log.info(
                            f"Repository '{github_repo.repo_id}' is already linked to owner '{repo_owner.id}'. Returning existing repository."
                        )
                        return repo  # Return if the repo is already linked

                ## Repository does not exist, add it to the owner's repositories
                log.info(
                    f"Repository '{github_repo.repo_id}' not found under owner '{repo_owner.id}', linking repository to owner."
                )
                existing_repo_owner.repositories.append(github_repo)
                self.session.add(existing_repo_owner)

            else:
                ## Owner does not exist, create new owner and repository
                log.info(
                    f"Owner '{repo_owner.id}' not found, creating new owner and linking repository."
                )
                github_repo.owner = repo_owner
                self.session.add(repo_owner)
                self.session.add(github_repo)

            ## Commit transaction and return new or updated repository
            self.session.commit()
            self.session.refresh(github_repo)

            return github_repo

        except Exception as exc:
            msg = f"({type(exc)}) Unhandled exception. Details: {exc}"
            log.error(msg)
            self.session.rollback()  # Rollback in case of failure
            raise exc

    def delete_repo(self, repo_id: int) -> None:
        """Deletes a repository if it exists."""
        repo = self.session.get(GithubStarredRepositoryModel, repo_id)
        if repo:
            self.session.delete(repo)
            self.session.commit()
