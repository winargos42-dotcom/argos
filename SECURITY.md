# Security Policy / Политика безопасности

ARGOS Universal OS is an experimental research project. Do not treat public demos,
prototypes, or automation as security-reviewed production software.

## Reporting vulnerabilities / Сообщение об уязвимости

Do **not** post credentials, exploit details, personal data, or active access tokens
in public issues, discussions, or pull requests.

Please contact the repository maintainer privately, or use GitHub's private
vulnerability reporting if it is enabled for this repository.
Include the affected commit, a concise reproduction, and impact without
disclosing real credentials. No response-time SLA is promised.

Не публикуйте секреты и уязвимости с работающими токенами в открытых issue.
Свяжитесь с владельцем репозитория приватно.

## Secret handling / Секреты

- Keep real service-account JSON, private keys, `.env` and API tokens outside Git.
- Use local environment variables or an appropriate secrets manager.
- Use least-privilege and short-lived credentials where possible.
- A secret exposed in **any** public commit must be revoked/rotated. Deleting
  the file from `main` or adding `.gitignore` is insufficient: Git history
  and previously downloaded clones may still contain the secret.
- Verify revocation in the provider's console; automatic blocking must not be assumed.
- Before any history rewrite, coordinate with contributors and preserve an
  incident record. Do not force-push shared branches without an explicit plan.

## Scope of automated checks

The repository's tracked-file scanner catches some high-confidence accidental
credential disclosures. It does **not** prove the codebase or its history is
free of secrets or vulnerabilities.
