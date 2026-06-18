#!/usr/bin/env python3
"""
ARGOS Headroom MCP Integration
Wraps MCP tool outputs through compression layer before LLM context.

Usage:
    # Standalone
    python argos_mcp_compression.py --tool hermes_tools --input /tmp/output.json --max-chars 4000

    # As a module
    from argos_mcp_compression import ArgosMCPCompressor
    comp = ArgosMCPCompressor(max_chars=3000)
    result = comp.process_tool_output("read_file", raw_json_string)

    # Via ARGOS MCP command
    # POST to /mcp {"method":"tools/call","params":{"name":"headroom_compress","arguments":{"text":"...","max_chars":3000}}}
"""

import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
from argos_compressor import ArgosCompressor, CompressResult


class ArgosMCPCompressor:
    """Wraps MCP tool calls with headroom compression."""

    def __init__(self, max_chars: int = 4000, preserve_errors: bool = True):
        self.compressor = ArgosCompressor(
            max_chars=max_chars,
            preserve_errors=preserve_errors,
        )

    def process_tool_output(
        self,
        tool_name: str,
        raw_output: str,
        tool_args: dict = None,
        user_query: str = "",
    ) -> dict:
        """
        Compress tool output and return MCP-compatible result.
        
        Returns dict with keys:
          - compressed_text: str
          - stats: dict (savings ratio, strategy, etc)
          - retrieval_marker: optional CCR marker for on-demand original retrieval
        """
        result = self.compressor.compress(raw_output)

        # Build CCR-style retrieval marker (if original was large)
        marker = None
        if result.original_chars > self.compressor.max_chars * 2:
            marker = self._make_ccr_marker(tool_name, tool_args, result)

        return {
            "compressed_text": result.text,
            "original_length": result.original_chars,
            "compressed_length": result.compressed_chars,
            "savings_pct": round(result.savings_pct, 1),
            "strategy": result.strategy,
            "stats": result.stats,
            "retrieval_marker": marker,
        }

    def _make_ccr_marker(self, tool_name: str, tool_args: dict, result: CompressResult) -> str:
        """Create CCR (Contextual Compression Retrieval) marker.
        LLM can "retrieve" original by calling headroom_retrieve with this ID."""
        import hashlib, time
        payload = json.dumps({"tool": tool_name, "args": tool_args or {}, "time": time.time()})
        uid = hashlib.sha256(payload.encode()).hexdigest()[:16]
        return f"[CCR: {tool_name}:{uid} — {result.original_chars} chars compressed to {result.compressed_chars}]"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compress MCP tool output")
    parser.add_argument("--tool", default="generic", help="Tool name")
    parser.add_argument("--input", "-i", required=True, help="Input file or '-' for stdin")
    parser.add_argument("--max-chars", type=int, default=4000, help="Max chars after compression")
    parser.add_argument("--output", "-o", default="-", help="Output file or '-' for stdout")
    args = parser.parse_args()

    if args.input == "-":
        raw = sys.stdin.read()
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            raw = f.read()

    comp = ArgosMCPCompressor(max_chars=args.max_chars)
    result = comp.process_tool_output(args.tool, raw)

    out = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output == "-":
        print(out)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)


if __name__ == "__main__":
    main()
