#!/usr/bin/env python3
"""
OSINT Reconnaissance Toolkit — 17 wrappers for internet-wide search engines.

Usage examples:
    import osint_tools as osint
    print(osint.crtsh("google.com"))
    print(osint.urlscan_submit("https://example.com"))
    print(osint.hibp_check("test@example.com"))
    print(osint.greynoise_context("8.8.8.8"))

Policy: passive reconnaissance only.  Read-only, public data.
"""

from __future__ import annotations

import json, os, re, time, urllib.error, urllib.parse, urllib.request
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Common utilities
# ---------------------------------------------------------------------------

_DEFAULT_TIMEOUT = 20
_DEFAULT_RETRY = 2


def _env(key: str) -> Optional[str]:
    """Return env var or None."""
    return os.environ.get(key)


def _http_json(
    url: str,
    data: Optional[bytes] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = _DEFAULT_TIMEOUT,
    method: Optional[str] = None,
) -> Dict[str, Any]:
    """Make HTTP request and return parsed JSON."""
    h = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) OSINT-Toolkit/1.0"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:2048]
        return {"error": f"HTTP {e.code}", "body": body, "url": url}
    except Exception as e:
        return {"error": str(e), "url": url}


def _stub(name: str, env_keys: List[str]) -> Dict[str, Any]:
    """Return a stub for paid tools without credentials."""
    return {
        "tool": name,
        "status": "stub",
        "reason": "API key missing",
        "env_keys_required": env_keys,
        "docs": f"Set {', '.join(env_keys)} to enable",
    }


def _clean_domain(domain: str) -> str:
    """Strip scheme and path from a hostname."""
    domain = domain.strip().lower()
    domain = re.sub(r"^https?://", "", domain, flags=re.I)
    domain = re.split(r"/", domain)[0]
    domain = re.split(r":", domain)[0]
    return domain


# =============================================================================
# 1. Shodan
# =============================================================================
def shodan_api_info() -> Dict[str, Any]:
    """Shodan API info (credits, plan).  Needs SHODAN_API_KEY."""
    key = _env("SHODAN_API_KEY")
    if not key:
        return _stub("shodan_api_info", ["SHODAN_API_KEY"])
    url = f"https://api.shodan.io/api-info?key={urllib.parse.quote(key)}"
    return _http_json(url)


def shodan_host(ip: str) -> Dict[str, Any]:
    """Shodan host search by IP.  Needs SHODAN_API_KEY."""
    key = _env("SHODAN_API_KEY")
    if not key:
        return _stub("shodan_host", ["SHODAN_API_KEY"])
    url = f"https://api.shodan.io/shodan/host/{urllib.parse.quote(ip)}?key={urllib.parse.quote(key)}&minify=True"
    return _http_json(url)


def shodan_search(query: str, page: int = 1) -> Dict[str, Any]:
    """Shodan search query.  Needs SHODAN_API_KEY."""
    key = _env("SHODAN_API_KEY")
    if not key:
        return _stub("shodan_search", ["SHODAN_API_KEY"])
    q = urllib.parse.quote(query)
    url = f"https://api.shodan.io/shodan/host/search?key={urllib.parse.quote(key)}&query={q}&page={page}&minify=True"
    return _http_json(url)


# =============================================================================
# 2. Censys
# =============================================================================
def censys_hosts(query: str, per_page: int = 5) -> Dict[str, Any]:
    """Censys host search.  CENSYS_API_ID + CENSYS_API_SECRET."""
    uid = _env("CENSYS_API_ID")
    secret = _env("CENSYS_API_SECRET")
    if not (uid and secret):
        return _stub("censys_hosts", ["CENSYS_API_ID", "CENSYS_API_SECRET"])
    import base64
    creds = base64.b64encode(f"{uid}:{secret}".encode()).decode()
    url = "https://search.censys.io/api/v2/hosts/search"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {creds}",
    }
    q = urllib.parse.quote(query)
    url = f"{url}?q={q}&per_page={per_page}"
    return _http_json(url, headers=headers)


# =============================================================================
# 3. FOFA
# =============================================================================
def fofa_search(query: str, size: int = 5) -> Dict[str, Any]:
    """FOFA asset search.  FOFA_EMAIL + FOFA_API_KEY required.
    Docs: https://en.fofa.info/api
    """
    email = _env("FOFA_EMAIL")
    key = _env("FOFA_API_KEY")
    if not (email and key):
        return _stub("fofa_search", ["FOFA_EMAIL", "FOFA_API_KEY"])
    import base64
    q = base64.b64encode(query.encode()).decode()
    url = f"https://en.fofa.info/api/v1/search/all?email={urllib.parse.quote(email)}&key={urllib.parse.quote(key)}&qbase64={urllib.parse.quote(q)}&size={size}&fields=host,ip,port,title,header,banner"
    return _http_json(url)


# =============================================================================
# 4. ZoomEye
# =============================================================================
def zoomeye_host(query: str, page: int = 1) -> Dict[str, Any]:
    """ZoomEye host search.  ZOOMEYE_API_KEY."""
    key = _env("ZOOMEYE_API_KEY")
    if not key:
        return _stub("zoomeye_host", ["ZOOMEYE_API_KEY"])
    q = urllib.parse.quote(query)
    url = f"https://api.zoomeye.org/host/search?query={q}&page={page}"
    headers = {"Authorization": f"JWT {key}", "Accept": "application/json"}
    return _http_json(url, headers=headers)


# =============================================================================
# 5. FullHunt
# =============================================================================
def fullhunt_domain(domain: str) -> Dict[str, Any]:
    """FullHunt attack surface for a domain.  FULLHUNT_API_KEY."""
    key = _env("FULLHUNT_API_KEY")
    if not key:
        return _stub("fullhunt_domain", ["FULLHUNT_API_KEY"])
    d = _clean_domain(domain)
    url = f"https://fullhunt.io/api/v1/domain/{urllib.parse.quote(d)}"
    headers = {"X-API-KEY": key, "Accept": "application/json"}
    return _http_json(url, headers=headers)


# =============================================================================
# 6. urlscan.io (free tier, rate-limited)
# =============================================================================
def urlscan_submit(_url: str, public: bool = True) -> Dict[str, Any]:
    """Submit a URL to urlscan sandbox.  Returns UUID ; poll with urlscan_result()."""
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "OSINT-Toolkit/1.0",
    }
    payload = json.dumps({
        "url": _url,
        "public": "on" if public else "off",
    }).encode()
    result = _http_json(
        "https://urlscan.io/api/v1/scan/",
        data=payload,
        headers=headers,
        method="POST",
    )
    return result


def urlscan_result(uuid: str) -> Dict[str, Any]:
    """Poll result by UUID."""
    return _http_json(f"https://urlscan.io/api/v1/result/{urllib.parse.quote(uuid)}/")


# =============================================================================
# 7. Hunter.io
# =============================================================================
def hunter_domain_emails(domain: str, limit: int = 10) -> Dict[str, Any]:
    """Hunter e-mail discovery by domain. HUNTER_API_KEY."""
    key = _env("HUNTER_API_KEY")
    if not key:
        return _stub("hunter_domain_emails", ["HUNTER_API_KEY"])
    d = _clean_domain(domain)
    url = f"https://api.hunter.io/v2/domain-search?domain={urllib.parse.quote(d)}&api_key={urllib.parse.quote(key)}&limit={limit}"
    return _http_json(url)


# =============================================================================
# 8. crt.sh (free, no key)
# =============================================================================
def crtsh(domain: str, exclude_expired: bool = True) -> Dict[str, Any]:
    """Certificate Transparency search for subdomains.
    Returns JSON via crt.sh REST API.
    """
    d = _clean_domain(domain)
    exclude = "expired" if exclude_expired else ""
    url = f"https://crt.sh/?q={urllib.parse.quote(d, safe='')}&output=json&exclude={exclude}"
    # crt.sh sometimes needs a longer timeout
    res = _http_json(url, timeout=30)
    if "error" in res:
        return res
    # Filter unique names
    names = list({
        n.get("name_value", "").strip()
        for n in res if isinstance(n, dict)
    })
    names = sorted(n for n in names if n)
    return {
        "domain": d,
        "cert_count": len(res) if isinstance(res, list) else 0,
        "subdomains": names,
        "raw_first_3": res[:3] if isinstance(res, list) else [],
    }


# =============================================================================
# 9. grep.app (free tier via web scraping)
# =============================================================================
def grepapp_search(query: str, lang: str = "") -> Dict[str, Any]:
    """Search grep.app via its HTTPS search page (no official API).
    Returns first raw result page links; may need HTML parsing for deep use.
    """
    q = urllib.parse.quote(query)
    url = f"https://grep.app/search?q={q}&filter=lang[python]"
    if lang:
        url += urllib.parse.quote(f"&filter=lang[{lang}]")
    # We intentionally return meta-info instead of raw HTML to keep output compact.
    res = _http_json(url, headers={"Accept": "text/html,application/xhtml+xml"}, timeout=15)
    if "error" in res:
        return res
    return {
        "tool": "grep.app",
        "status": "ok",
        "note": "HTML page returned; parse links with dedicated scraper if needed",
        "url": url,
    }


# =============================================================================
# 10. SecurityTrails
# =============================================================================
def securitytrails_domain(domain: str) -> Dict[str, Any]:
    """SecurityTrails current DNS data.  SECURITYTRAILS_API_KEY."""
    key = _env("SECURITYTRAILS_API_KEY")
    if not key:
        return _stub("securitytrails_domain", ["SECURITYTRAILS_API_KEY"])
    d = _clean_domain(domain)
    url = f"https://api.securitytrails.com/v1/domain/{urllib.parse.quote(d)}"
    headers = {"APIKEY": key, "Accept": "application/json"}
    return _http_json(url, headers=headers)


def securitytrails_subdomains(domain: str, limit: int = 50) -> Dict[str, Any]:
    """Subdomain list via SecurityTrails."""
    key = _env("SECURITYTRAILS_API_KEY")
    if not key:
        return _stub("securitytrails_subdomains", ["SECURITYTRAILS_API_KEY"])
    d = _clean_domain(domain)
    url = f"https://api.securitytrails.com/v1/domain/{urllib.parse.quote(d)}/subdomains?children_only=False&limit={limit}"
    headers = {"APIKEY": key, "Accept": "application/json"}
    return _http_json(url, headers=headers)


# =============================================================================
# 11. Intelligence X
# =============================================================================
def intelx_search(term: str, max_results: int = 10) -> Dict[str, Any]:
    """Intelligence X search.  INTELX_API_KEY."""
    key = _env("INTELX_API_KEY")
    if not key:
        return _stub("intelx_search", ["INTELX_API_KEY"])
    q = urllib.parse.quote(term)
    url = f"https://2.intelx.io/intelligent/search?term={q}&maxresults={max_results}"
    headers = {"x-key": key, "Accept": "application/json"}
    return _http_json(url, headers=headers)


# =============================================================================
# 12. Have I Been Pwned (free, rate-limited)
# =============================================================================
def hibp_check(email: str, truncate: bool = True) -> Dict[str, Any]:
    """Check e-mail against HIBP breach database.
    https://haveibeenpwned.com/api/v3/breachedaccount/{account}
    """

    truncated = "true" if truncate else "false"
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(email)}?truncateResponse={truncated}"
    headers = {
        "hibp-api-key": _env("HIBP_API_KEY") or "",
        "user-agent": "OSINT-Toolkit/1.0",
    }
    res = _http_json(url, headers=headers, timeout=10)
    if "error" in res and res.get("error", "").startswith("HTTP 404"):
        return {"email": email, "breaches": [], "status": "not found"}
    if "error" in res:
        return {"email": email, "error": res["error"]}
    return {"email": email, "breaches": res}


# =============================================================================
# 13. LeakIX (free, no key, rate-limited)
# =============================================================================
def leakix_search(query: str, index: str = "leaks") -> Dict[str, Any]:
    """LeakIX open database / host search.
    Index: 'leaks' | 'services'.
    """
    q = urllib.parse.quote(query)
    url = f"https://leakix.net/search?q={q}&scope={index}"
    headers = {"Accept": "application/json"}
    return _http_json(url, headers=headers)


def leakix_host(ip: str) -> Dict[str, Any]:
    """LeakIX single host lookup."""
    url = f"https://leakix.net/host/{urllib.parse.quote(ip)}"
    headers = {"Accept": "application/json"}
    return _http_json(url, headers=headers)


# =============================================================================
# 14. DeHashed
# =============================================================================
def dehashed_search(query: str, page: int = 0) -> Dict[str, Any]:
    """DeHashed compromised-credential search.  DEHASHED_API_KEY."""
    key = _env("DEHASHED_API_KEY")
    if not key:
        return _stub("dehashed_search", ["DEHASHED_API_KEY"])
    q = urllib.parse.quote(query)
    url = f"https://api.dehashed.com/search?query={q}&page={page}"
    import base64
    creds = base64.b64encode(f"{key}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}", "Accept": "application/json"}
    return _http_json(url, headers=headers)


# =============================================================================
# 15. Vulners (free tier, key optional for higher rate)
# =============================================================================
def vulners_search(query: str, size: int = 5) -> Dict[str, Any]:
    """Vulners search for CVEs, exploits, bulletins."""
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = json.dumps({
        "query": {"match": {"_all": query}},
        "sort": {"_score": {"order": "desc"}},
        "size": size,
    }).encode()
    return _http_json(
        "https://vulners.com/api/v3/search/lucene/",
        data=payload,
        headers=headers,
        method="POST",
    )


def vulners_cve_summary(cve: str) -> Dict[str, Any]:
    """Fetch document summary by CVE ID."""
    cve = cve.upper().strip()
    url = f"https://vulners.com/api/v3/search/id/?id={urllib.parse.quote(cve)}&references=True"
    return _http_json(url)


# =============================================================================
# 16. GreyNoise (free tier exists)
# =============================================================================
def greynoise_context(ip: str) -> Dict[str, Any]:
    """GreyNoise context for an IP.  Free tier works without key for some endpoints."""
    key = _env("GREYNOISE_API_KEY")
    headers = {"Accept": "application/json"}
    if key:
        headers["key"] = key
    url = f"https://api.greynoise.io/v3/noise/context/{urllib.parse.quote(ip)}"
    return _http_json(url, headers=headers)


def greynoise_quick(ip: str) -> Dict[str, Any]:
    """GreyNoise quick lookup (free)."""
    url = f"https://api.greynoise.io/v3/community/{urllib.parse.quote(ip)}"
    return _http_json(url)


# =============================================================================
# 17. WiGLE
# =============================================================================
def wigle_search(
    query: Optional[str] = None,
    ssid: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    results_per_page: int = 5,
) -> Dict[str, Any]:
    """WiGLE Wi-Fi / Bluetooth network search.  WIGLE_API_NAME + WIGLE_API_KEY."""
    name = _env("WIGLE_API_NAME")
    key = _env("WIGLE_API_KEY")
    if not (name and key):
        return _stub("wigle_search", ["WIGLE_API_NAME", "WIGLE_API_KEY"])
    import base64
    creds = base64.b64encode(f"{name}:{key}".encode()).decode()
    headers = {
        "Authorization": f"Basic {creds}",
        "Accept": "application/json",
    }
    params: Dict[str, Any] = {"first": 0, "last": results_per_page, "freenet": "false"}
    if ssid:
        params["ssid"] = ssid
    if query:
        params["netid"] = query
    if lat is not None and lon is not None:
        params["latrange1"] = lat - 0.01
        params["latrange2"] = lat + 0.01
        params["longrange1"] = lon - 0.01
        params["longrange2"] = lon + 0.01
    qs = urllib.parse.urlencode(params)
    url = f"https://api.wigle.net/api/v2/network/search?{qs}"
    return _http_json(url, headers=headers)


# =============================================================================
# Batch / helper shortcuts
# =============================================================================
def quick_recon(domain: str) -> Dict[str, Any]:
    """Run crt.sh + urlscan submit + HIBP on domain (e-mail guessed as abuse@domain)."""
    d = _clean_domain(domain)
    return {
        "crtsh": crtsh(d),
        "urlscan": urlscan_submit(f"https://{d}"),
        "hibp": hibp_check(f"abuse@{d}"),
    }


def ip_recon(ip: str) -> Dict[str, Any]:
    """GreyNoise + LeakIX + optional Shodan (if key) for an IP."""
    data = {
        "greynoise_context": greynoise_context(ip),
        "greynoise_quick": greynoise_quick(ip),
        "leakix": leakix_host(ip),
    }
    if _env("SHODAN_API_KEY"):
        data["shodan"] = shodan_host(ip)
    if _env("CENSYS_API_ID"):
        data["censys"] = censys_hosts(f"ip: {ip}")
    return data


if __name__ == "__main__":
    # --- quick smoke test --------------------------------------------------
    print("=== crt.sh ===")
    print(json.dumps(crtsh("cloudflare.com"), indent=2, ensure_ascii=False))
    print("\n=== HIBP ===")
    print(json.dumps(hibp_check("test@example.com"), indent=2, ensure_ascii=False))
    print("\n=== GreyNoise quick ===")
    print(json.dumps(greynoise_quick("8.8.8.8"), indent=2, ensure_ascii=False))
