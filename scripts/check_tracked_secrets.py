#!/usr/bin/env python3
"""Fail CI on selected high-confidence secrets in currently tracked files.

Only scans the checked-out tree, NOT historical commits; never prints secret values.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

PRIVATE_KEY_HEADER = re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----")
SENSITIVE_EXTENSIONS = {".pem", ".key", ".p8", ".p12", ".pfx", ".jks", ".keystore"}
ALLOWED_ENV_TEMPLATES = {".env.example", ".env.sample", ".env.template"}


def tracked_paths():
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    return [Path(s.decode("utf-8", errors="surrogateescape"))
            for s in result.stdout.split(b"\x00") if s]


def scan():
    problems = []
    for path in tracked_paths():
        if not path.is_file() or path.is_symlink():
            continue
        basename = path.name.lower()
        if (basename == ".env" or
                (basename.startswith(".env.") and basename not in ALLOWED_ENV_TEMPLATES)):
            problems.append((path, "committed environment file"))
            continue
        if path.suffix.lower() in SENSITIVE_EXTENSIONS:
            problems.append((path, "committed private credential file type"))
            continue
        if "service-account" in basename or "service_account" in basename:
            problems.append((path, "credential-like filename"))
            continue
        try:
            if path.stat().st_size > 2_000_000:
                continue
            content = path.read_bytes()
        except OSError:
            problems.append((path, "unreadable tracked file"))
            continue
        if PRIVATE_KEY_HEADER.search(content):
            problems.append((path, "PEM private key header"))
        if path.suffix.lower() == ".json":
            try:
                obj = json.loads(content)
            except (UnicodeDecodeError, ValueError):
                continue
            if (isinstance(obj, dict) and obj.get("type") == "service_account"
                    and isinstance(obj.get("private_key"), str)
                    and obj["private_key"].strip()):
                problems.append((path, "Google service-account private key"))
    return problems


if __name__ == "__main__":
    findings = scan()
    for path, reason in findings:
        print(f"SECRET_CHECK_FAILED: {path} ({reason})")
    if findings:
        print(f"Found {len(findings)} tracked-file issue(s). No secret values printed.")
        sys.exit(1)
    print("Tracked-file secret check passed (current tree only, limited patterns).")
