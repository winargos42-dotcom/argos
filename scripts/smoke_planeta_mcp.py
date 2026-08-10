#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import os
import sys

import httpx2
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


EXPECTED_TOOLS = {
    "planeta_campaign_status",
    "planeta_campaign_preview",
    "planeta_validate_campaign",
    "planeta_prepare_campaign",
    "planeta_fill_draft",
    "planeta_sync_draft",
    "planeta_request_submit_approval",
    "planeta_submit_for_moderation",
}


def check_health(base_url: str) -> None:
    response = httpx2.get(f"{base_url.rstrip('/')}/health", timeout=20.0, follow_redirects=True)
    response.raise_for_status()
    payload = response.json()
    if payload.get("ok") is not True or payload.get("service") != "planeta-mcp":
        raise RuntimeError(f"Unexpected health payload: {payload}")


async def check_mcp(base_url: str, secret: str) -> set[str]:
    endpoint = f"{base_url.rstrip('/')}/mcp"
    async with httpx2.AsyncClient(
        headers={"Authorization": f"Bearer {secret}"},
        timeout=30.0,
        follow_redirects=True,
    ) as http_client:
        async with streamable_http_client(endpoint, http_client=http_client) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools = await session.list_tools()
                names = {tool.name for tool in tools.tools}
    missing = EXPECTED_TOOLS - names
    if missing:
        raise RuntimeError(f"Missing MCP tools: {sorted(missing)}; discovered={sorted(names)}")
    return names


async def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only smoke check for ARGOS Planeta MCP")
    parser.add_argument("base_url", help="Service base URL, e.g. https://planeta-mcp.up.railway.app")
    args = parser.parse_args()

    secret = os.getenv("PLANETA_MCP_SECRET")
    if not secret:
        print("PLANETA_MCP_SECRET is required in the local environment", file=sys.stderr)
        return 2

    check_health(args.base_url)
    names = await check_mcp(args.base_url, secret)
    print(f"health=ok service=planeta-mcp tools={len(names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
