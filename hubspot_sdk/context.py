from __future__ import annotations
from beartype.typing import TYPE_CHECKING, Literal
from types import TracebackType

import requests
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase
from requests_toolbelt import sessions
from urllib3.util.retry import Retry

if TYPE_CHECKING:
    from requests import Request


class HubSpotAuth(AuthBase):

    def __init__(self, access_token: str) -> None:
        """
        Authorization class extending `requests.auth.AuthBase`, consumed by an
        instance of `requests.Session`.
        Pass in a HubSpot private app access token to validate the connection.
        Parameters
        ----------
        access_token
            HubSpot Private App access token
        """
        self._token = access_token

    def __call__(self, request: Request) -> Request:
        request.headers['Content-Type'] = 'application/json'
        request.headers['Authorization'] = f'Bearer {self._token}'
        return request


class HubSpotContext:

    def __init__(self, token: str = "") -> None:
        """
        HubSpot Session context manager.
        On enter, returns the session context.
        On exit, tears down the created context.
        Pass in a Private App access token to be consumed by a class that
        extends `requests.auth.AuthBase` to validate the connection.
        Parameters
        ----------
        token, optional
            HubSpot Private App access token, by default ""
        """
        self._base = 'https://api.hubapi.com'
        self._base_ctx = sessions.BaseUrlSession(base_url=self._base)
        self._base_ctx.auth = HubSpotAuth(token)
        self._base_ctx.mount(
            prefix=self._base,
            adapter=HTTPAdapter(
                max_retries=Retry(backoff_factor=1)
            )
        )

    def __enter__(self) -> requests.Session:
        return self._base_ctx

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType
    ) -> bool:
        if exc_type is not None:
            print("Exception occurred:", exc_type, exc_val, exc_tb)
        self._base_ctx.close()
        return False
