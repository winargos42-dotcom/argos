# Home Assistant 2026.9.4 update receipt

The running Home Assistant container was updated from **2026.9.3 to pinned 2026.9.4** on 2026-09-27. The authenticated `/api/config` response confirms the new version. The stop, consistent backup, recreate and API-ready sequence took 26.64 seconds. Only the Compose image was changed; mounts, networking, restart policy, environment, devices and the checked container settings were preserved.

## Verified outcome

- Configuration validation passed in the new image with no network and a copied configuration, before stopping the live service.
- All 91 state IDs and all 91 entity-registry IDs are unchanged. Only hashes and counts are included here.
- After startup: 49 available, 26 unavailable, 16 unknown. These are state counts, not device counts.
- Tuya is loaded and its cloud MQTT connection is active. Its 14 devices remain 2 online / 12 offline. The patch did not resolve their offline status. The official [2026.9.4 changelog](https://www.home-assistant.io/changelogs/core-2026.9/) lists a Tuya fan-at-zero fix; this receipt does not claim a connectivity fix.
- Actual signed Coral GET, retained MQTT state, a fresh non-retained MQTT update and eight owned HA diagnostics passed. X230 diagnostics and ARGOS health were also healthy. Coral readiness means authenticated status, not an inference test.
- A first diagnostics read during integration startup returned 404; the completed post-startup observation is loaded/connected. This transient is not treated as a successful check.

## Backup and rollback

The stopped service exited cleanly. Its complete configuration and SQLite database were archived privately (7,334,709 bytes, mode 0600). SQLite integrity passed both before archiving and after an independent extraction; critical configuration hashes matched. The original image remains local. The backup hash and both image IDs are in `deployment.json`.

The local guarded rollback script is `/root/argos-ha-update-20260927/rollback.py`. It verifies the archive and allowed image/Compose identities, stops only Home Assistant, preserves the post-update configuration under a separate private directory, restores the tested archive, and recreates with the exact previous image ID. It has not been executed against the live service because the update succeeded. Database restoration was tested; a full production rollback was not rehearsed. Coordinate any later rollback with concurrent configuration edits, including the separately managed LAN bridge.

Private raw Docker inspection, credentials, full configuration, actual entity IDs, database backups and browser screenshots are excluded from this bundle. The public evidence is an operational receipt, not a portable installer.

## ARGOS API and browser boundary

The authenticated ARGOS `/api/ha` registry-consumer check passed after the update: its Home Assistant endpoint matches the actual fresh registry, its 91 entity IDs and availability counts match HA, and no entity attributes are leaked. Unauthenticated requests return 401. The registry was already fresh, so no discovery refresh was required and no registry state was manually changed. See `argos-api-after.json`.

LAN bridge changes and native/static browser navigation belong to the separately coordinated LAN follow-up. This bundle does not claim that those browser checks have passed.

## Evidence allowlist

`inventory.json`, `before-api.json`, `preflight.json`, `image-compatibility.json`, `deployment.json`, `after-api.json`, `live-chain-proof.json`, `argos-api-after.json`, `validation-status.json`, this README and `manifest.sha256.json`. The manifest hashes every other allowed file and excludes itself.
