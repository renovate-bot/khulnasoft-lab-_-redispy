from os import environ
from typing import Any, List, Type, Union

from requests import Session

from upstash_redis.commands import Commands
from upstash_redis.format import FORMATTERS
from upstash_redis.http import make_headers, sync_execute
from upstash_redis.typing import RESTEncoding, RESTResult


class Redis(Commands):
    def __init__(
        self,
        url: str,
        token: str,
        rest_encoding: RESTEncoding = "base64",
        rest_retries: int = 1,
        rest_retry_interval: float = 3,  # Seconds.
        format_return: bool = True,
        allow_telemetry: bool = True,
    ):
        """
        :param url: UPSTASH_REDIS_REST_URL in the console
        :param token: UPSTASH_REDIS_REST_TOKEN in the console
        :param rest_encoding: the encoding that can be used by the REST API to parse the response before sending it
        :param rest_retries: how many times an HTTP request will be retried if it fails
        :param rest_retry_interval: how many seconds will be waited between each retry
        :param format_return: whether the raw, RESP2 result or a formatted response will be returned
        :param allow_telemetry: whether anonymous telemetry can be collected
        """

        self._url = url
        self._token = token

        self._allow_telemetry = allow_telemetry

        self._format_return = format_return

        self._rest_encoding = rest_encoding
        self._rest_retries = rest_retries
        self._rest_retry_interval = rest_retry_interval

        self._headers = make_headers(token, rest_encoding, allow_telemetry)
        self._session = Session()

    @classmethod
    def from_env(
        cls,
        rest_encoding: RESTEncoding = "base64",
        rest_retries: int = 1,
        rest_retry_interval: float = 3,
        format_return: bool = True,
        allow_telemetry: bool = True,
    ):
        """
        Load the credentials from environment.

        :param rest_encoding: the encoding that can be used by the REST API to parse the response before sending it
        :param rest_retries: how many times an HTTP request will be retried if it fails
        :param rest_retry_interval: how many seconds will be waited between each retry
        :param format_return: whether the raw, RESP2 result or a formatted response will be returned
        :param allow_telemetry: whether anonymous telemetry can be collected
        """

        return cls(
            environ["UPSTASH_REDIS_REST_URL"],
            environ["UPSTASH_REDIS_REST_TOKEN"],
            rest_encoding,
            rest_retries,
            rest_retry_interval,
            format_return,
            allow_telemetry,
        )

    def __enter__(self) -> "Redis":
        return self

    def __exit__(
        self,
        exc_type: Union[Type[BaseException], None],
        exc_val: Union[BaseException, None],
        exc_tb: Any,
    ) -> None:
        self.close()

    def close(self):
        """
        Closes the resources associated with the client.
        """
        self._session.close()

    def run(self, command: List) -> RESTResult:
        """
        Specify the http options and execute the command.
        """

        res = sync_execute(
            session=self._session,
            url=self._url,
            headers=self._headers,
            encoding=self._rest_encoding,
            retries=self._rest_retries,
            retry_interval=self._rest_retry_interval,
            command=command,
        )

        main_command = command[0]
        if len(command) > 1 and (main_command == "PUBSUB" or main_command == "SCRIPT"):
            main_command = f"{main_command} {command[1]}"

        if (
            self._format_return
            or main_command == "HSCAN"
            or main_command == "SMEMBERS"
            or main_command == "SDIFF"
            or main_command == "SINTER"
            or main_command == "SSCAN"
            or main_command == "SUNION"
            or main_command == "ZSCAN"
        ) and (main_command in FORMATTERS):
            return FORMATTERS[main_command](res, command)

        return res
