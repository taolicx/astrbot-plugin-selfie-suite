from __future__ import annotations

from typing import Any, Protocol


class PluginConfig(Protocol):
    """给 internal_qzone 底层 session/client/api 使用的最小配置协议。"""

    cookies_str: str
    timeout: int
    client: Any | None

    def update_cookies(self, cookies_str: str) -> None:
        ...
