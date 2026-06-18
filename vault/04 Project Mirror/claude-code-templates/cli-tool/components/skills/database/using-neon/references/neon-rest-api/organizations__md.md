---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/database/using-neon/references/neon-rest-api/organizations.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\database\using-neon\references\neon-rest-api\organizations.md
source_ext: .md
source_sha256: ac6437387a904e462073e52c5a9853bf98afd80184c228e93ba6f9c250c38a22
text_sha256: 39308ddcdf9ec2e7d6860434fbd90838ee9c410467e5d67f383aecbfd537faa7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# organizations.md

- Source: `claude-code-templates/cli-tool/components/skills/database/using-neon/references/neon-rest-api/organizations.md`
- Extract: `text`
- SHA256: `ac6437387a904e462073e52c5a9853bf98afd80184c228e93ba6f9c250c38a22`

## Content

## Overview

This section provides rules for managing organizations, their members, invitations, and organization API keys. Organizations allow multiple users to collaborate on projects and share resources within Neon.

## Manage organizations

### Retrieve organization details

1.  Action: Retrieves detailed information about a specific organization.
2.  Endpoint: `GET /organizations/{org_id}`
3.  Path Parameters:
    - `org_id` (string, required): The unique identifier of the organization.

Example Request:

```bash
curl 'https://console.neon.tech/api/v2/organizations/{org_id}' \
  -H 'Accept: application/json' \
  -H "Authorization: Bearer $NEON_API_KEY"
```

### List organization members

1.  Action: Retrieves a list of all members belonging to the specified organization.
2.  Endpoint: `GET /organizations/{org_id}/members`
3.  Path Parameters:
    - `org_id` (string, required): The unique identifier of the organization.

Example Request:

```bash
curl 'https://console.neon.tech/api/v2/organizations/{org_id}/members' \
  -H 'Accept: application/json' \
  -H "Authorization: Bearer $NEON_API_KEY"
```

### Retrieve organization member details

1.  Action: Retrieves information about a specific member of an organization.
2.  Endpoint: `GET /organizations/{org_id}/members/{member_id}`
3.  Path Parameters:
    - `org_id` (string, required): The unique identifier of the organization.
    - `member_id` (UUID, required): The unique identifier of the organization member.

Example Request:

```bash
curl 'https://console.neon.tech/api/v2/organizations/{org_id}/members/{member_id}' \
  -H 'Accept: application/json' \
  -H "Authorization: Bearer $NEON_API_KEY"
```

### Update role for organization member

1.  Action: Updates the role of a specified member within an organization.
2.  Prerequisite: This action can only be performed by an organization `admin`.
3.  Endpoint: `PATCH /organizations/{org_id}/members/{member_id}`
4.  Path Parameters:
    - `org_id` (string, required): The unique identifier of the organization.
    - `member_id` (UUID, required): The unique identifier of the organization member.
5.  Body Parameters:
    - `role` (string, required): The new role for the member. Allowed values: `admin`, `member`.

Example: Change a member's role to admin

```bash
curl -X 'PATCH' \
  'https://console.neon.tech/api/v2/organizations/{org_id}/members/{member_id}' \
  -H 'Accept: application/json' \
  -H "Authorization: Bearer $NEON_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"role": "admin"}'
```

### Remove member from organization

1.  Action: Removes a specified member from an organization.
2.  Prerequisites:
    - This action can only be performed by an organization `admin`.
    - An admin cannot be removed if they are the only admin left in the organization.
3.  Endpoint: `DELETE /organizations/{org_id}/members/{member_id}`
4.  Path Parameters:
    - `org_id` (string, required): The unique identifier of the organization.
    - `member_id` (UUID, required): The unique identifier of the organization member to remove.

Example Request:

```bash
curl -X 'DELETE' \
  'https://console.neon.tech/api/v2/organizations/{org_id}/members/{member_id}' \
  -H 'Accept: application/json' \
  -H "Authorization: Bearer $NEON_API_KEY"
```

### Create organization invitations

1.  Action: Creates and sends one or more email invitations for users to join a specific organization.
2.  Endpoint: `POST /organizations/{org_id}/invitations`
3.  Path Parameters:
    - `org_id` (string, required): The unique identifier of the organization.
4.  Body Parameters:
    `invitations` (array of objects, required): A list of invitations to create.
    - `email` (string, required): The email address of the user to invite.
    - `role` (string, required): The role the invited user will have. Allowed values: `admin`, `member`.

Example: Invite two users with different roles

```bash
curl -X 'POST' \
  'https://console.neon.tech/api/v2/organizations/{org_id}/invitations' \
  -H 'Accept: application/json' \
  -H "Authorization: Bearer $NEON_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
  "invitations": [
    {
      "email": "developer@example.com",
      "role": "member"
    },
    {
      "email": "manager@example.com",
      "role": "admin"
    }
  ]
}'
```

### List organization invitations

1.  Action: Retrieves information about outstanding invitations for the specified organization.
2.  Endpoint: `GET /organizations/{org_id}/invitations`
3.  Path Parameters:
    - `org_id` (string, required): The unique identifier of the organization.

Example Request:

```bash
curl 'https://console.neon.tech/api/v2/organizations/{org_id}/invitations' \
  -H 'Accept: application/json' \
  -H "Authorization: Bearer $NEON_API_KEY"
```

### Create organization API key

1.  Action: Creates a new API key for the specified organization. The key can be scoped to the entire organization or limited to a single project within it.
2.  Endpoint: `POST /organizations/{org_id}/api_keys`
3.  Path Parameters:
    - `org_id` (string, required): The unique identifier of the organization.
4.  Body Parameters:
    - `key_name` (string, required): A user-specified name for the API key (max 64 characters).
    - `project_id` (string, optional): If provided, the API key's access will be restricted to only this project.
5.  Authorization: Use a Personal API Key of an organization `admin` to create organization API keys.

Example: Create a project-scoped API key

```bash
curl -X 'POST' \
  'https://console.neon.tech/api/v2/organizations/{org_id}/api_keys' \
  -H 'Accept: application/json' \
  -H "Authorization: Bearer $PERSONAL_API_KEY_OF_ADMIN" \
  -H 'Content-Type: application/json' \
  -d '{
  "key_name": "ci-pipeline-key-for-project-x",
  "project_id": "project-id-123"
}'
```

### List organization API keys

1.  Action: Retrieves a list of all API keys created for the specified organization.
2.  Endpoint: `GET /organizations/{org_id}/api_keys`
3.  Note: The response includes metadata about the keys (like `id` and `name`) but does not include the secret key tokens themselves. Tokens are only visible upon creation.
4.  Path Parameters:
    - `org_id` (string, required): The unique identifier of the organization.

Example Request:

```bash
curl 'https://console.neon.tech/api/v2/organizations/{org_id}/api_keys' \
  -H 'Accept: application/json' \
  -H "Authorization: Bearer $NEON_API_KEY"
```

### Revoke organization API key

1.  Action: Permanently revokes the specified organization API key.
2.  Endpoint: `DELETE /organizations/{org_id}/api_keys/{key_id}`
3.  Path Parameters:
    - `org_id` (string, required): The unique identifier of the organization.
    - `key_id` (integer, required): The unique identifier of the API key to revoke. You can obtain this ID by listing the organization's API keys.

Example Request:

```bash
curl -X 'DELETE' \
  'https://console.neon.tech/api/v2/organizations/{org_id}/api_keys/{key_id}' \
  -H 'Accept: application/json' \
  -H "Authorization: Bearer $NEON_API_KEY"
```

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
