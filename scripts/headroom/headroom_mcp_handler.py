"""
Headroom MCP Handler for ARGOS
Перехватывает MCP tool calls → сжимает output → передаёт LLM.

Usage in ARGOS:
    from headroom_mcp_handler import headroom_mcp_handler

    # В обработчике MCP tools/call
    if tool_name in COMPRESSION_ELIGIBLE_TOOLS:
        raw_output = call_upstream_tool(tool_name, tool_args)
        compressed = headroom_mcp_handler(tool_name, raw_output, tool_args)
        return compressed
"""

import json, os, sys
from typing import Any, Dict

# Adjust path if running standalone
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from argos_compressor import ArgosCompressor


# Tools whose outputs are typically large and compressible
COMPRESSION_ELIGIBLE_TOOLS = {
    "providers", "skills", "limits", "status",
    "terminal", "read_file", "search_files", "osint_recon",
    "grep.app", "crtsh", "shodan_search", "censys_hosts",
}

_compressor = ArgosCompressor(max_chars=4000)


def headroom_mcp_handler(tool_name: str, raw_output: str, tool_args: Dict[str, Any] = None) -> str:
    """
    Entry point: returns compressed text if savings > 20%, else passthrough.
    """
    if tool_name not in COMPRESSION_ELIGIBLE_TOOLS:
        return raw_output

    # Skip if already small
    if len(raw_output) < 800:
        return raw_output

    try:
        result = _compressor.compress(raw_output)
    except Exception:
        # Safety: on any error, return original
        return raw_output

    # Only compress if meaningful savings
    if result.savings_pct < 20:
        return raw_output

    # Prepend compression header for LLM context
    header = f"[🗜️ Compressed {result.savings_pct:.0f}% via {result.strategy}]\n"
    if result.stats.get("original_chars"):
        header += f"[Original: {result.stats['original_chars']} chars → {result.compressed_chars}]\n"

    return header + result.text


def headroom_tool_compress(text: str, max_chars: int = 4000) -> Dict[str, Any]:
    """Direct tool entry for MCP `headroom_compress`."""
    old_max = _compressor.max_chars
    try:
        _compressor.max_chars = max_chars
        result = _compressor.compress(text)
        return {
            "compressed_text": result.text,
            "strategy": result.strategy,
            "original_chars": result.original_chars,
            "compressed_chars": result.compressed_chars,
            "savings_pct": round(result.savings_pct, 1),
        }
    finally:
        _compressor.max_chars = old_max


if __name__ == "__main__":
    # CLI: echo '{"big":"json"...}' | python headroom_mcp_handler.py --tool read_file
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", required=True)
    parser.add_argument("--max-chars", type=int, default=4000)
    args = parser.parse_args()

    raw = sys.stdin.read()
    out = headroom_mcp_handler(args.tool, raw)
    print(out)
