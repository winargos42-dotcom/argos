from __future__ import annotations

import asyncio
import contextlib
from urllib.parse import urlsplit

from fastapi import WebSocket


async def direct_vnc_relay(websocket: WebSocket, target: str) -> None:
    """Relay noVNC WebSocket frames directly to loopback x11vnc TCP.

    The target is intentionally restricted to tcp://127.0.0.1:5900 so this
    cannot become a generic SSRF/tunnelling primitive.
    """

    parsed = urlsplit(target)
    if parsed.scheme != "tcp" or parsed.hostname != "127.0.0.1" or parsed.port != 5900:
        await websocket.close(code=4403)
        return

    try:
        reader, writer = await asyncio.open_connection("127.0.0.1", 5900)
    except OSError:
        await websocket.close(code=1013)
        return

    await websocket.accept()

    async def client_to_vnc() -> None:
        while True:
            message = await websocket.receive()
            if message["type"] == "websocket.disconnect":
                return
            payload = message.get("bytes")
            if payload is None and message.get("text") is not None:
                payload = message["text"].encode("latin-1")
            if payload:
                writer.write(payload)
                await writer.drain()

    async def vnc_to_client() -> None:
        while True:
            payload = await reader.read(65536)
            if not payload:
                return
            await websocket.send_bytes(payload)

    tasks = {
        asyncio.create_task(client_to_vnc()),
        asyncio.create_task(vnc_to_client()),
    }
    try:
        _done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
    finally:
        writer.close()
        with contextlib.suppress(Exception):
            await writer.wait_closed()
        with contextlib.suppress(Exception):
            await websocket.close(code=1000)
