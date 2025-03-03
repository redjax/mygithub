from __future__ import annotations

__all__ = [
    "default_allow_credentials",
    "default_allowed_origins",
    "default_allowed_methods",
    "default_allowed_headers",
    "default_openapi_url",
    "default_api_str",
]

default_allow_credentials: bool = True
default_allowed_origins: list[str] = ["*"]
default_allowed_methods: list[str] = ["*"]
default_allowed_headers: list[str] = ["*"]

## Route to openapi docs. This returns the docs site as a JSON object
#  If you set this to the same route as docs (i.e. /docs), you will only
#  get the openapi JSON response, no Swagger docs.
default_openapi_url: str = "/docs/openapi"

default_api_str: str = "/api/v1"
