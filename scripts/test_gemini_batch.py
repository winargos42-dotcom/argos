#!/usr/bin/env python3
"""Quick smoke test for GeminiBatchClient with GCP proxy auto-detection."""

import asyncio
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from gemini_batch import (
    GeminiBatchClient,
    BatchRequest,
    BatchResult,
    build_veto_audit_requests,
    build_training_requests,
)


def test_proxy_auto_detect():
    with patch.dict(
        os.environ,
        {
            "GEMINI_API_KEY": "test-key-123",
            "ARGOS_GCP_URL": "https://gcp-proxy.example.com",
        },
        clear=True,
    ):
        client = GeminiBatchClient(model="gemini-1.5-flash-001")
        assert client._using_proxy is True
        assert client.gcp_url == "https://gcp-proxy.example.com"
        print("✅ Proxy auto-detect: PASS")


def test_direct_mode():
    with patch.dict(
        os.environ,
        {"GEMINI_API_KEY": "test-key-456"},
        clear=True,
    ):
        client = GeminiBatchClient(model="gemini-1.5-flash-001")
        assert client._using_proxy is False
        assert client.gcp_url == ""
        print("✅ Direct mode: PASS")


def test_build_veto_requests():
    evidence = [
        {
            "id": "ev_001",
            "node_id": "node-a",
            "reason": "unauthorized_access",
            "source_path": "/var/log/auth.log",
            "sha256": "deadbeef",
            "confidence": 0.92,
            "summary": "Suspicious login attempt",
        }
    ]
    reqs = build_veto_audit_requests(evidence)
    assert isinstance(reqs, list)
    assert len(reqs) == 1
    req = reqs[0]
    assert req.key == "ev_001"
    assert "Suspicious login attempt" in req.content
    print("✅ build_veto_audit_requests: PASS")


def test_build_training_requests():
    templates = [
        {
            "id": "t1",
            "instruction": "Explain FPGA",
            "context": "SPR2801",
            "expected_format": "JSON",
        }
    ]
    reqs = build_training_requests(templates)
    assert len(reqs) == 1
    assert "SPR2801" in reqs[0].content
    print("✅ build_training_requests: PASS")


async def main():
    print("Running GeminiBatch smoke tests...")
    test_proxy_auto_detect()
    test_direct_mode()
    test_build_veto_requests()
    test_build_training_requests()
    print("All tests passed.")


if __name__ == "__main__":
    asyncio.run(main())
