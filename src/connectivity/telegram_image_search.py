"""Image search results and Telegram photo+source replies for ARGOS.

The configured SearXNG API must be HTTP on loopback. External image URLs are
returned to Telegram only after URL validation. Openverse is the fallback.
"""

from __future__ import annotations

import asyncio
from io import BytesIO
import ipaddress
import json
import os
import re
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen


_IMAGE_WORDS = ("фото", "фотограф", "картин", "изображен", "снимк", "photo", "picture", "image")
_SEARCH_WORDS = ("найди", "найти", "поищи", "покажи", "пришли", "ищи", "search", "find", "show")
_MAX_REPLY = 4


def is_image_search_request(text: str) -> bool:
    if not isinstance(text, str):
        return False
    text = text.casefold()
    return any(w in text for w in _IMAGE_WORDS) and any(w in text for w in _SEARCH_WORDS)


def image_search_query(text: str) -> str:
    query = text.strip()
    query = re.sub(r"(?i)\b(?:найди|найти|поищи|покажи|пришли|ищи|search|find|show)\b", " ", query)
    query = re.sub(r"(?i)\b(?:в интернете|в сети|мне|пожалуйста)\b", " ", query)
    query = re.sub(r"(?i)\b(?:фото(?:графии|графий)?|фотографии|фотографий|картинки|картинок|изображения|изображений|снимки|photo|pictures?|images?)\b", " ", query)
    return " ".join(query.split())[:180] or "фото"


def _safe_url(url: object) -> str:
    if not isinstance(url, str) or len(url) > 800:
        return ""
    try:
        parts = urlsplit(url)
        if parts.scheme not in ("http", "https") or not parts.hostname or parts.username or parts.password:
            return ""
        if any(ord(c) < 33 for c in url):
            return ""
        host = parts.hostname.lower()
        if host == "localhost" or host.endswith((".localhost", ".local", ".internal")):
            return ""
        try:
            if not ipaddress.ip_address(host).is_global:
                return ""
        except ValueError:
            pass
    except ValueError:
        return ""
    return url


def _api_data(url: str, timeout: float = 6) -> dict:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "ARGOS-ImageSearch/1.0"})
    with urlopen(request, timeout=timeout) as response:
        raw = response.read(1_000_001)
    if len(raw) > 1_000_000:
        raise ValueError("Image API response is too large")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("Invalid image API response")
    return data


def _searxng_images(query: str) -> list[dict]:
    base = os.environ.get("ARGOS_SEARXNG_URL", "http://127.0.0.1:8080").rstrip("/")
    parts = urlsplit(base)
    if (parts.scheme != "http" or parts.hostname not in ("127.0.0.1", "localhost", "::1")
            or parts.path not in ("", "/") or parts.username or parts.password or parts.query or parts.fragment):
        return []
    params = urlencode({"q": query, "categories": "images", "format": "json", "safesearch": "0"})
    try:
        data = _api_data(f"{base}/search?{params}")
    except (OSError, ValueError, TimeoutError):
        return []
    results = []
    for row in data.get("results", []):
        if not isinstance(row, dict):
            continue
        image = _safe_url(row.get("img_src"))
        link = _safe_url(row.get("url")) or image
        if image and link:
            results.append({"image": image, "source": link, "title": str(row.get("title", ""))[:120]})
        if len(results) >= _MAX_REPLY:
            break
    return results


def _openverse_images(query: str) -> list[dict]:
    params = urlencode({"q": query, "page_size": _MAX_REPLY})
    try:
        data = _api_data(f"https://api.openverse.org/v1/images/?{params}")
    except (OSError, ValueError, TimeoutError):
        return []
    results = []
    for row in data.get("results", []):
        if not isinstance(row, dict):
            continue
        image = _safe_url(row.get("thumbnail")) or _safe_url(row.get("url"))
        link = _safe_url(row.get("foreign_landing_url")) or image
        if image and link:
            results.append({"image": image, "source": link, "title": str(row.get("title", ""))[:120]})
    return results[:_MAX_REPLY]


def lookup_images(query: str) -> list[dict]:
    rows = _searxng_images(query) or _openverse_images(query)
    if rows:
        return rows
    # A verbose or ungrammatical phrase can return zero results even when its
    # subject is common (e.g. "специфическое красоты"). Try the final term.
    words = query.split()
    if len(words) > 1 and len(words[-1]) >= 3:
        return _searxng_images(words[-1]) or _openverse_images(words[-1])
    return []


def _download_photo(image_url: str) -> BytesIO | None:
    """Fallback when Telegram cannot fetch an image URL by itself."""
    if not _safe_url(image_url):
        return None
    request = Request(image_url, headers={"User-Agent": "ARGOS-ImageSearch/1.0"})
    try:
        with urlopen(request, timeout=5) as response:
            mime = response.headers.get_content_type()
            if mime not in ("image/jpeg", "image/png"):
                return None
            raw = response.read(5_000_001)
    except (OSError, ValueError, TimeoutError):
        return None
    if len(raw) > 5_000_000:
        return None
    if mime == "image/jpeg" and not raw.startswith(b"\xff\xd8\xff"):
        return None
    if mime == "image/png" and not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        return None
    result = BytesIO(raw)
    result.name = "argos_photo.jpg" if mime == "image/jpeg" else "argos_photo.png"
    return result


async def reply_with_images_and_links(message, text: str, *, lookup=lookup_images) -> None:
    query = image_search_query(text)
    try:
        rows = await asyncio.to_thread(lookup, query)
    except Exception:
        rows = []
    if not rows:
        await message.reply_text("❌ Фотографии пока не найдены. Попробуй уточнить запрос.", parse_mode=None)
        return

    sent = 0
    for row in rows[:_MAX_REPLY]:
        image = _safe_url(row.get("image"))
        if not image:
            continue
        try:
            await message.reply_photo(photo=image, caption="🖼 Фото из поиска", parse_mode=None)
            sent += 1
        except Exception:
            # Some CDNs reject Telegram's image proxy. Upload from the bot
            # instead, with a byte cap and a strict image content-type check.
            try:
                photo = await asyncio.to_thread(_download_photo, image)
                if photo is not None:
                    await message.reply_photo(photo=photo, caption="🖼 Фото из поиска", parse_mode=None)
                    sent += 1
            except Exception:
                continue

    links = []
    seen = set()
    for row in rows[:_MAX_REPLY]:
        link = _safe_url(row.get("source"))
        if link and link not in seen:
            seen.add(link)
            links.append(f"{len(links) + 1}. {link}")
    prefix = f"🖼 Отправлено фотографий: {sent}.\n🔗 Источники:\n"
    await message.reply_text(prefix + ("\n".join(links) if links else "Ссылки недоступны."), parse_mode=None)
