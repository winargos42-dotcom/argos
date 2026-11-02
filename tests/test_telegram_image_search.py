"""Offline tests for Telegram image+source replies."""

import asyncio
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from src.connectivity import telegram_image_search as mod
except ModuleNotFoundError:
    import telegram_image_search as mod


class FakeMessage:
    def __init__(self, fail_photo=False):
        self.photos = []
        self.texts = []
        self.fail_photo = fail_photo

    async def reply_photo(self, photo, caption, **kwargs):
        if self.fail_photo:
            raise RuntimeError("Telegram failed")
        self.photos.append((photo, caption))

    async def reply_text(self, text, **kwargs):
        self.texts.append(text)


class ImageSearchTests(unittest.TestCase):
    def test_detects_user_image_request(self):
        self.assertTrue(mod.is_image_search_request("Найди в интернете фото красоты"))
        self.assertTrue(mod.is_image_search_request("Найди в интернете Фото специфическое красоты"))
        self.assertTrue(mod.is_image_search_request("Покажи картинки носорога"))
        self.assertFalse(mod.is_image_search_request("Найди статью про носорога"))
        self.assertFalse(mod.is_image_search_request("Сфотографируй меня"))

    def test_removes_search_instructions_from_query(self):
        self.assertEqual(mod.image_search_query("Найди в интернете фото красивого носорога"), "красивого носорога")
        self.assertEqual(mod.image_search_query("Найди в интернете Фото специфическое красоты"), "специфическое красоты")

    def test_searxng_image_request(self):
        rows = {"results": [
            {"title": "Rhino", "img_src": "https://cdn.example.org/rhino.jpg", "url": "https://example.org/rhino"},
            {"title": "Bad", "img_src": "http://127.0.0.1/internal", "url": "https://example.org/bad"},
        ]}
        with patch.object(mod, "_api_data", return_value=rows) as api:
            found = mod._searxng_images("носорог")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["source"], "https://example.org/rhino")
        parsed = urlsplit(api.call_args.args[0])
        self.assertEqual(parse_qs(parsed.query)["categories"], ["images"])
        self.assertEqual(parse_qs(parsed.query)["format"], ["json"])

    def test_openverse_fallback(self):
        with patch.object(mod, "_searxng_images", return_value=[]), patch.object(
            mod, "_openverse_images", return_value=[{"image":"https://example.org/photo.jpg","source":"https://example.org/","title":"Photo"}]
        ):
            self.assertEqual(len(mod.lookup_images("природа")), 1)

    def test_simplifies_empty_image_search(self):
        with patch.object(mod, "_searxng_images", side_effect=[[], []]) as searx, patch.object(
            mod, "_openverse_images", side_effect=[[], [{"image": "https://example.org/a.jpg", "source": "https://example.org/a"}]]
        ) as openverse:
            self.assertEqual(len(mod.lookup_images("специфическое красоты")), 1)
            self.assertEqual([call.args[0] for call in searx.call_args_list], ["специфическое красоты", "красоты"])
            self.assertEqual([call.args[0] for call in openverse.call_args_list], ["специфическое красоты", "красоты"])

    def test_openverse_uses_current_api_host(self):
        with patch.object(mod, "_api_data", return_value={"results": []}) as api:
            mod._openverse_images("красота")
            self.assertEqual(urlsplit(api.call_args.args[0]).hostname, "api.openverse.org")

    def test_invalid_searxng_endpoint_does_not_send_request(self):
        with patch.dict(mod.os.environ, {"ARGOS_SEARXNG_URL": "http://example.org:8080"}), patch.object(mod, "_api_data") as api:
            self.assertEqual(mod._searxng_images("x"), [])
        api.assert_not_called()


class ImageReplyTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        async def inline_to_thread(fn, *args):
            return fn(*args)
        self.patcher = patch.object(mod.asyncio, "to_thread", new=inline_to_thread)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    async def test_sends_photos_then_links(self):
        msg = FakeMessage()
        rows = [
            {"image": "https://cdn.example.org/one.jpg", "source": "https://example.org/one", "title": "One"},
            {"image": "https://cdn.example.org/two.jpg", "source": "https://example.org/two", "title": "Two"},
        ]
        await mod.reply_with_images_and_links(msg, "Найди фото носорога", lookup=lambda _: rows)
        self.assertEqual(len(msg.photos), 2)
        self.assertIn("https://example.org/one", msg.texts[0])
        self.assertIn("https://example.org/two", msg.texts[0])

    async def test_photo_send_failures_still_send_links(self):
        msg = FakeMessage(fail_photo=True)
        rows = [{"image": "https://example.org/a.jpg", "source": "https://example.org/a", "title": "A"}]
        await mod.reply_with_images_and_links(msg, "Покажи картинки", lookup=lambda _: rows)
        self.assertEqual(msg.photos, [])
        self.assertIn("Отправлено фотографий: 0", msg.texts[0])
        self.assertIn("https://example.org/a", msg.texts[0])

    async def test_empty_result_is_explicit(self):
        msg = FakeMessage()
        await mod.reply_with_images_and_links(msg, "Найди фото красоты", lookup=lambda _: [])
        self.assertIn("не найдены", msg.texts[0])

    async def test_retries_telegram_photo_failure_with_downloaded_bytes(self):
        class FallbackMessage(FakeMessage):
            async def reply_photo(self, photo, caption, **kwargs):
                if isinstance(photo, str):
                    raise RuntimeError("Telegram couldn't fetch URL")
                self.photos.append((photo, caption))

        msg = FallbackMessage()
        with patch.object(mod, "_download_photo", return_value=mod.BytesIO(b"test")) as download:
            await mod.reply_with_images_and_links(msg, "Найди фото красоты", lookup=lambda _: [
                {"image": "https://cdn.example.org/one.jpg", "source": "https://example.org/one"}
            ])
        self.assertEqual(len(msg.photos), 1)
        self.assertIn("Отправлено фотографий: 1", msg.texts[0])
        download.assert_called_once()


if __name__ == "__main__":
    unittest.main()
