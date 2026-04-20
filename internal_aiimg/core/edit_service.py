import asyncio
import json
from collections.abc import Iterable
from pathlib import Path

import aiohttp

from astrbot.api import logger

from .image_manager import ImageManager

EDIT_TASK_TYPES = {"id", "style", "subject", "background", "element"}

_ENDPOINT_SUFFIXES = (
    "/async/images/edits",
    "/async/images/generations",
    "/images/edits",
    "/images/generations",
)


def _normalize_gitee_base_url(raw: str) -> str:
    """只保留 API 根路径，避免把完整 endpoint 再次拼接。"""
    url = str(raw or "").strip().rstrip("/")
    if not url:
        return "https://ai.gitee.com/v1"
    for suffix in _ENDPOINT_SUFFIXES:
        idx = url.find(suffix)
        if idx != -1:
            url = url[:idx]
            break
    task_idx = url.find("/task/")
    if task_idx != -1:
        url = url[:task_idx]
    return url.rstrip("/")


class ImageEditService:
    def __init__(self, config: dict, imgr: ImageManager):
        self.config = config
        self.imgr = imgr

        self.econf = config["edit"]
        raw_base_url = self.econf["base_url"]
        self.base_url = _normalize_gitee_base_url(raw_base_url)
        if str(raw_base_url).strip().rstrip("/") != self.base_url:
            logger.warning(
                "[Gitee] 检测到 base_url 包含完整 endpoint，已自动归一化: %s -> %s",
                raw_base_url,
                self.base_url,
            )

        keys = config["edit"]["api_keys"] or config["draw"]["api_keys"]
        self.api_keys = [str(k).strip() for k in keys if str(k).strip()]
        self._key_index = 0

        self._session: aiohttp.ClientSession | None = None

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def _session_get(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    def _next_key(self) -> str:
        if not self.api_keys:
            raise RuntimeError("没有可用的 edit API Key")
        key = self.api_keys[self._key_index]
        self._key_index = (self._key_index + 1) % len(self.api_keys)
        return key

    async def _create_task(
        self,
        prompt: str,
        images: list[bytes],
        task_types: Iterable[str],
        api_key: str,
    ) -> str:
        session = await self._session_get()
        data = aiohttp.FormData()
        data.add_field("prompt", prompt)
        data.add_field("model", self.econf["model"])
        data.add_field("num_inference_steps", str(self.econf["num_inference_steps"]))
        data.add_field("guidance_scale", str(self.econf["guidance_scale"]))

        for t in task_types:
            if t in EDIT_TASK_TYPES:
                data.add_field("task_types", t)

        for i, img in enumerate(images):
            data.add_field(
                "image",
                img,
                filename=f"image_{i}.jpg",
                content_type="image/jpeg",
            )
        async with session.post(
            f"{self.base_url}/async/images/edits",
            headers={"Authorization": f"Bearer {api_key}"},
            data=data,
        ) as resp:
            body = await resp.text()
            try:
                result = json.loads(body)
            except json.JSONDecodeError:
                result = {"message": body[:300] or f"HTTP {resp.status}"}
            if resp.status != 200:
                raise RuntimeError(result.get("message", result))

            task_id = result.get("task_id")
            if not task_id:
                raise RuntimeError("未返回 task_id")

            return task_id

    async def _poll_task(self, task_id: str, api_key: str) -> str:
        session = await self._session_get()
        url = f"{self.base_url}/task/{task_id}"

        max_rounds = self.econf["poll_timeout"] // self.econf["poll_interval"]

        for i in range(max_rounds):
            async with session.get(
                url,
                headers={"Authorization": f"Bearer {api_key}"},
            ) as resp:
                body = await resp.text()
                try:
                    result = json.loads(body)
                except json.JSONDecodeError:
                    result = {"message": body[:300] or f"HTTP {resp.status}"}

                if resp.status != 200:
                    raise RuntimeError(result.get("message", result))

                status = result.get("status")
                if status == "success":
                    file_url = result.get("output", {}).get("file_url")
                    if not file_url:
                        raise RuntimeError("任务成功但未返回 file_url")
                    return file_url
                if status in {"failed", "cancelled"}:
                    raise RuntimeError(f"任务失败: {status}")
            logger.debug(f"[图生图轮询] 第{i + 1}轮任务状态：{status}")
            await asyncio.sleep(self.econf["poll_interval"])

        raise TimeoutError("图生图任务超时")

    async def edit(
        self,
        prompt: str,
        images: list[bytes],
        task_types: Iterable[str] = ("id",),
    ) -> Path:
        if not images:
            raise ValueError("至少需要一张图片")
        api_key = self._next_key()
        task_id = await self._create_task(prompt, images, task_types, api_key)
        file_url = await self._poll_task(task_id, api_key)
        return await self.imgr.download_image(file_url)
