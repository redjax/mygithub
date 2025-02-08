from __future__ import annotations

import json
from pathlib import Path
import typing as t

from loguru import logger as log

from mygh.libs.depends import db_depends
from mygh.domain.github import stars as stars_domain


def save_github_stars(starred_repos: list[dict]) -> list[stars_domain.GithubStarredRepositoryModel]:
    session_pool = db_depends.get_session_pool()
    
    saved_repos: list[stars_domain.GithubStarredRepositoryModel] = []
    
    with session_pool() as session:
        api_response_repo = stars_domain.GithubStarsAPIResponseRepository(session)
        gh_repository_repo = stars_domain.GithubStarredRepositoryDBRepository(session)
        
        db_api_response_model = stars_domain.GithubStarsAPIResponseModel(json_data=starred_repos)
        
        try:
            db_api_response_model = api_response_repo.create(db_api_response_model)
        except Exception as e:
            msg = f"({type(e)}) Unhandled exception saving API response. Details: {e}"
            log.error(msg)            
            raise
        
        log.info(f"Saved API response [{db_api_response_model.id}] to database")
        
        log.info("Extracting repositories and owners from API response")
        for repo_data in starred_repos:
            repo_owner_data = repo_data["owner"]
            
            ## Create owner model
            repo_owner = stars_domain.GithubRepositoryOwnerModel(
                id=repo_owner_data["id"],
                login=repo_owner_data["login"],
                node_id=repo_owner_data["node_id"],
                avatar_url=repo_owner_data["avatar_url"],
                gravatar_id=repo_owner_data.get("gravatar_id"),  # Nullable field
                url=repo_owner_data["url"],
                html_url=repo_owner_data["html_url"],
                followers_url=repo_owner_data["followers_url"],
                following_url=repo_owner_data["following_url"],
                gists_url=repo_owner_data["gists_url"],
                starred_url=repo_owner_data["starred_url"],
                subscriptions_url=repo_owner_data["subscriptions_url"],
                organizations_url=repo_owner_data["organizations_url"],
                repos_url=repo_owner_data["repos_url"],
                events_url=repo_owner_data["events_url"],
                received_events_url=repo_owner_data["received_events_url"],
                type=repo_owner_data["type"],
                user_view_type=repo_owner_data.get("user_view_type", "User"),  # Fallback value
                site_admin=repo_owner_data["site_admin"],
            )
            
            ## Create Repository Model instance
            github_repo = stars_domain.GithubStarredRepositoryModel(
            repo_id=repo_data["id"],
            node_id=repo_data["node_id"],  # Ensure you have this key
            name=repo_data["name"],
            description=repo_data["description"],
            html_url=repo_data["html_url"],
            stargazers_count=repo_data["stargazers_count"],
            language=repo_data.get("language", ""),  # Default to empty string if no language
            private=repo_data.get("private", False),  # Default to False if not provided
            fork=repo_data.get("fork", False),  # Default to False if not provided
            url=repo_data["url"],
            forks_url=repo_data["forks_url"],
            keys_url=repo_data["keys_url"],
            collaborators_url=repo_data["collaborators_url"],
            teams_url=repo_data["teams_url"],
            hooks_url=repo_data["hooks_url"],
            issue_events_url=repo_data["issue_events_url"],
            events_url=repo_data["events_url"],
            assignees_url=repo_data["assignees_url"],
            branches_url=repo_data["branches_url"],
            tags_url=repo_data["tags_url"],
            blobs_url=repo_data["blobs_url"],
            git_tags_url=repo_data["git_tags_url"],
            git_refs_url=repo_data["git_refs_url"],
            trees_url=repo_data["trees_url"],
            statuses_url=repo_data["statuses_url"],
            languages_url=repo_data["languages_url"],
            stargazers_url=repo_data["stargazers_url"],
            contributors_url=repo_data["contributors_url"],
            subscribers_url=repo_data["subscribers_url"],
            subscription_url=repo_data["subscription_url"],
            commits_url=repo_data["commits_url"],
            git_commits_url=repo_data["git_commits_url"],
            comments_url=repo_data["comments_url"],
            issue_comment_url=repo_data["issue_comment_url"],
            contents_url=repo_data["contents_url"],
            compare_url=repo_data["compare_url"],
            merges_url=repo_data["merges_url"],
            archive_url=repo_data["archive_url"],
            downloads_url=repo_data["downloads_url"],
            issues_url=repo_data["issues_url"],
            pulls_url=repo_data["pulls_url"],
            milestones_url=repo_data["milestones_url"],
            notifications_url=repo_data["notifications_url"],
            labels_url=repo_data["labels_url"],
            releases_url=repo_data["releases_url"],
            deployments_url=repo_data["deployments_url"],
            created_at=repo_data["created_at"],
            updated_at=repo_data["updated_at"],
            pushed_at=repo_data["pushed_at"],
            git_url=repo_data["git_url"],
            ssh_url=repo_data["ssh_url"],
            clone_url=repo_data["clone_url"],
            svn_url=repo_data["svn_url"],
            homepage=repo_data["homepage"],
            size=repo_data["size"],
            forks_count=repo_data["forks_count"],
            open_issues_count=repo_data["open_issues_count"],
            license=repo_data["license"],
            allow_forking=repo_data.get("allow_forking", False),  # Default to False if not provided
            is_template=repo_data.get("is_template", False),  # Default to False if not provided
            web_commit_signoff_required=repo_data.get("web_commit_signoff_required", False),  # Default to False
            topics=json.dumps(repo_data.get("topics", [])),  # Default to empty list if not provided
            visibility=repo_data["visibility"],
            forks=repo_data["forks"],
            open_issues=repo_data["open_issues"],
            watchers=repo_data["watchers"],
            default_branch=repo_data["default_branch"],
            permissions=repo_data.get("permissions", {}),  # Default to empty dictionary if not provided
            owner_id=repo_owner.id  # Correctly reference owner_id
        )
            
            ## Save to database using the repository class
            try:
                saved_repo: stars_domain.GithubStarredRepositoryModel = gh_repository_repo.create_or_get_repo(github_repo, repo_owner)
                saved_repos.append(saved_repo)
            except Exception as exc:
                msg = f"({type(exc)}) Unhandled exception saving repository. Details: {exc}"
                log.error(msg)
                raise

            log.info(f"Processed repository: {saved_repo.name} (ID: {saved_repo.repo_id})")
        
                
    return saved_repos
    