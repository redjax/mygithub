from __future__ import annotations

from contextlib import AbstractContextManager
import json
from pathlib import Path
import typing as t

import core_utils, db_lib, depends, http_lib, settings

from loguru import logger as log

class GithubAPIController(AbstractContextManager):
    def __init__(
        self,
        api_token: str,
        github_api_version: str = "2022-11-28",
        use_cache: bool = True,
        follow_redirects: bool = False,
        cache_ttl: int = 900
    ):
        self.api_token = api_token
        self.github_api_version = github_api_version
        self.use_cache = use_cache
        self.follow_redirects = follow_redirects
        self.cache_ttl = cache_ttl

        self.base_url = "https://api.github.com"
        self.http_controller: http_lib.HttpxController | None = None

    def __enter__(self) -> t.Self:
        self.http_controller = self._get_http_controller()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            log.error(f"({exc_type}) {exc_val}")
            return False

        return True

    def _default_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.api_token}",
            "X-GitHub-Api-Version": self.github_api_version,
            "User-Agent": "mygh-python",
        }
        
    def _get_http_controller(self):
        http_controller: http_lib.HttpxController = http_lib.get_http_controller(use_cache=self.use_cache, follow_redirects=self.follow_redirects, cache_ttl=self.cache_ttl)
        
        return http_controller

    def get_user_stars(self, results_per_page: int = 30, sort_by: str = "created", sort_direction: str = "desc") -> t.Optional[list[dict[str, t.Any]]]:
        """Fetch all starred repositories of the authenticated user, handling pagination."""
        if results_per_page < 1 or results_per_page > 100:
            raise ValueError(f"results_per_page must be between 1 and 100. Default is 30. Got [{results_per_page}]")

        if sort_by not in ["created", "updated"]:
            raise ValueError(f"sort_by must be 'created' or 'updated'. Got [{sort_by}]")

        if sort_direction not in ["asc", "desc"]:
            raise ValueError(f"sort_direction must be 'asc' or 'desc'. Got [{sort_direction}]")

        url: str = f"{self.base_url}/user/starred"
        all_stars = []

        
        headers = self._default_headers()

        params = {"sort": sort_by, "direction": sort_direction, "per_page": results_per_page}

        log.info("Getting user's starred repositories.")

        try:
            with self.http_controller as http_ctl:
                while url:
                    # Only use params for the first request, after that, use direct URLs from pagination
                    req = http_lib.build_request(url=url, headers=headers, params=params if url == f"{self.base_url}/user/starred" else None)
                    res = http_ctl.send_request(req)
                    log.debug(f"Next page links: {res.links}")

                    if res.status_code != 200:
                        log.error(
                            f"Failed to get user's starred repositories. [{res.status_code}: {res.reason_phrase}] {res.text}"
                        )
                        return None

                    try:
                        res_data = http_lib.decode_response(res)
                        all_stars.extend(res_data)
                    except Exception as exc:
                        msg = f"({type(exc)}) Error decoding user's starred repositories. Details: {exc}"
                        log.error(msg)
                        raise exc

                    # Get the next page URL from the response links
                    url = res.links.get("next", {}).get("url")

        except Exception as exc:
            msg = f"({type(exc)}) Error getting user's starred repositories. Details: {exc}"
            log.error(msg)
            raise exc

        return all_stars if all_stars else None
