from typing import Any, List, Literal, Optional, TypedDict

import aiohttp
from aiohttp import ClientSession
from tqdm.asyncio import tqdm

from ..common.utils import extract_books, extract_download_link


class SearchOptions(TypedDict, total=True):
    column: Literal["author", "title", "publisher", "year"]


class Client:
    def __init__(self):
        self.session: Optional[ClientSession] = None

    async def __aenter__(self) -> "Client":
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self, exc_type: Optional[type], exc: Optional[Exception], tb: Any
    ) -> None:
        if self.session:
            await self.session.close()

    async def search(self, query: str, opts: SearchOptions) -> str:
        if not self.session or self.session.closed:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "http://libgen.rs/search.php", params={"req": query, **opts}
                ) as resp:
                    return extract_books(await resp.text())
        else:
            async with self.session.get(
                "http://libgen.rs/search.php", params={"req": query, **opts}
            ) as resp:
                return extract_books(await resp.text())

    async def download(self, mirrors: List[str], save_path: str) -> None:
        for mirror in mirrors:
            try:
                if not self.session or self.session.closed:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(mirror) as resp:
                            download_link = extract_download_link(await resp.text())
                            async with session.get(download_link) as resp:
                                total = int(resp.headers.get("content-length", 0))
                                with tqdm(
                                    total=total,
                                    unit="iB",
                                    unit_scale=True,
                                    desc="Downloading",
                                ) as progress:
                                    with open(save_path, "wb") as f:
                                        async for chunk in resp.content.iter_chunked(
                                            1024
                                        ):
                                            f.write(chunk)
                                            progress.update(len(chunk))
                else:
                    async with self.session.get(mirror) as resp:
                        download_link = extract_download_link(await resp.text())
                        async with self.session.get(download_link) as resp:
                            total = int(resp.headers.get("content-length", 0))
                            with tqdm(
                                total=total,
                                unit="iB",
                                unit_scale=True,
                                desc="Downloading",
                            ) as progress:
                                with open(save_path, "wb") as f:
                                    async for chunk in resp.content.iter_chunked(1024):
                                        f.write(chunk)
                                        progress.update(len(chunk))
                break
            except Exception as e:
                print(f"Failed to download from {mirror}. Error: {e}")
                continue
