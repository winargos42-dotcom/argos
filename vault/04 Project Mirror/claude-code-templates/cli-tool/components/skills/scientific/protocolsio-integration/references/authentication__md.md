---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/scientific/protocolsio-integration/references/authentication.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\scientific\protocolsio-integration\references\authentication.md
source_ext: .md
source_sha256: 6d3e684ce9f78edf0bd6f8db4977d48100dd85fc439e140dd7610bb590018812
text_sha256: 227a44f0514f5fdfffa72eeb45eb6edb798a780810ce7f5c8cbf91ded6421215
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:51
---

# authentication.md

- Source: `claude-code-templates/cli-tool/components/skills/scientific/protocolsio-integration/references/authentication.md`
- Extract: `text`
- SHA256: `6d3e684ce9f78edf0bd6f8db4977d48100dd85fc439e140dd7610bb590018812`

## Content

# Protocols.io Authentication

## Overview

The protocols.io API supports two types of access tokens for authentication, enabling access to both public and private content.

## Access Token Types

### 1. CLIENT_ACCESS_TOKEN

- **Purpose**: Enables access to public content and the private content of the client user
- **Use case**: When accessing your own protocols and public protocols
- **Scope**: Limited to the token owner's private content plus all public content

### 2. OAUTH_ACCESS_TOKEN

- **Purpose**: Grants access to specific users' private content plus all public content
- **Use case**: When building applications that need to access other users' content with their permission
- **Scope**: Full access to authorized user's private content plus all public content

## Authentication Header

All API requests must include an Authorization header:

```
Authorization: Bearer [ACCESS_TOKEN]
```

## OAuth Flow

### Step 1: Generate Authorization Link

Direct users to the authorization URL to grant access:

```
GET https://protocols.io/api/v3/oauth/authorize
```

**Parameters:**
- `client_id` (required): Your application's client ID
- `redirect_uri` (required): URL to redirect users after authorization
- `response_type` (required): Set to "code"
- `state` (optional but recommended): Random string to prevent CSRF attacks

**Example:**
```
https://protocols.io/api/v3/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code&state=RANDOM_STRING
```

### Step 2: Exchange Authorization Code for Token

After user authorization, protocols.io redirects to your `redirect_uri` with an authorization code. Exchange this code for an access token:

```
POST https://protocols.io/api/v3/oauth/token
```

**Parameters:**
- `grant_type`: Set to "authorization_code"
- `code`: The authorization code received
- `client_id`: Your application's client ID
- `client_secret`: Your application's client secret
- `redirect_uri`: Must match the redirect_uri used in Step 1

**Response includes:**
- `access_token`: The OAuth access token to use for API requests
- `token_type`: "Bearer"
- `expires_in`: Token lifetime in seconds (typically 1 year)
- `refresh_token`: Token for refreshing the access token

### Step 3: Refresh Access Token

Before the access token expires (typically 1 year), use the refresh token to obtain a new access token:

```
POST https://protocols.io/api/v3/oauth/token
```

**Parameters:**
- `grant_type`: Set to "refresh_token"
- `refresh_token`: The refresh token received in Step 2
- `client_id`: Your application's client ID
- `client_secret`: Your application's client secret

## Rate Limits

Be aware of rate limiting when making API requests:

- **Standard endpoints**: 100 requests per minute per user
- **PDF endpoint** (`/view/[protocol-uri].pdf`):
  - Signed-in users: 5 requests per minute
  - Unsigned users: 3 requests per minute

## Best Practices

1. **Store tokens securely**: Never expose access tokens in client-side code or version control
2. **Handle token expiration**: Implement automatic token refresh before expiration
3. **Respect rate limits**: Implement exponential backoff for rate limit errors
4. **Use state parameter**: Always include a state parameter in OAuth flow for security
5. **Validate redirect_uri**: Ensure redirect URIs match exactly between authorization and token requests

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
