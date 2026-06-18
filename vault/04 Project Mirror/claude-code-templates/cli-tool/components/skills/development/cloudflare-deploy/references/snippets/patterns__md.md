---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/snippets/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\snippets\patterns.md
source_ext: .md
source_sha256: 814e9190e5041fa86e249d7254ffe2553534a631a1c0af1f1800fc30ad976752
text_sha256: 2b06454df89a837e16ae554769ad055e8de90d2c6bc19a81b4aeee0fc423029d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/snippets/patterns.md`
- Extract: `text`
- SHA256: `814e9190e5041fa86e249d7254ffe2553534a631a1c0af1f1800fc30ad976752`

## Content

# Snippets Patterns

## Security Headers

```javascript
export default {
  async fetch(request) {
    const response = await fetch(request);
    const newResponse = new Response(response.body, response);
    newResponse.headers.set("X-Frame-Options", "DENY");
    newResponse.headers.set("X-Content-Type-Options", "nosniff");
    newResponse.headers.delete("X-Powered-By");
    return newResponse;
  }
}
```

**Rule:** `true` (all requests)

## Geo-Based Routing

```javascript
export default {
  async fetch(request) {
    const country = request.cf.country;
    if (["GB", "DE", "FR"].includes(country)) {
      const url = new URL(request.url);
      url.hostname = url.hostname.replace(".com", ".eu");
      return Response.redirect(url.toString(), 302);
    }
    return fetch(request);
  }
}
```

## A/B Testing

```javascript
export default {
  async fetch(request) {
    const cookies = request.headers.get("Cookie") || "";
    let variant = cookies.match(/ab_test=([AB])/)?.[1] || (Math.random() < 0.5 ? "A" : "B");
    
    const req = new Request(request);
    req.headers.set("X-Variant", variant);
    const response = await fetch(req);
    
    if (!cookies.includes("ab_test=")) {
      const newResponse = new Response(response.body, response);
      newResponse.headers.append("Set-Cookie", `ab_test=${variant}; Path=/; Secure`);
      return newResponse;
    }
    return response;
  }
}
```

## Bot Detection

```javascript
export default {
  async fetch(request) {
    const botScore = request.cf.botManagement?.score;
    if (botScore && botScore < 30) return new Response("Denied", { status: 403 });
    return fetch(request);
  }
}
```

**Requires:** Bot Management plan

## API Auth Header Injection

```javascript
export default {
  async fetch(request) {
    if (new URL(request.url).pathname.startsWith("/api/")) {
      const req = new Request(request);
      req.headers.set("X-Internal-Auth", "secret_token");
      req.headers.delete("Authorization");
      return fetch(req);
    }
    return fetch(request);
  }
}
```

## CORS Headers

```javascript
export default {
  async fetch(request) {
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
          "Access-Control-Allow-Headers": "Content-Type, Authorization"
        }
      });
    }
    const response = await fetch(request);
    const newResponse = new Response(response.body, response);
    newResponse.headers.set("Access-Control-Allow-Origin", "*");
    return newResponse;
  }
}
```

## Maintenance Mode

```javascript
export default {
  async fetch(request) {
    if (request.headers.get("X-Bypass-Token") === "admin") return fetch(request);
    return new Response("<h1>Maintenance</h1>", {
      status: 503,
      headers: { "Content-Type": "text/html", "Retry-After": "3600" }
    });
  }
}
```

## Pattern Selection

| Pattern | Complexity | Use Case |
|---------|-----------|----------|
| Security Headers | Low | All sites |
| Geo-Routing | Low | Regional content |
| A/B Testing | Medium | Experiments |
| Bot Detection | Medium | Requires Bot Management |
| API Auth | Low | Backend protection |
| CORS | Low | API endpoints |
| Maintenance | Low | Deployments |

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
