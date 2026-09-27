# Tuya recovery assessment

Fresh authenticated HA diagnostics confirm the integration is loaded, polling is enabled, and the Tuya cloud MQTT connection is connected. The installed versions at the check were Home Assistant 2026.9.3, Tuya device-sharing SDK 0.2.15 and device handlers 0.0.27.

There are 14 cloud devices: 12 offline and 2 online. The 26 unavailable HA entities belong to offline cloud devices. Nine of the offline devices are marked as subdevices. The offline set includes two gateway-category devices, including a primary Zigbee gateway; another gateway is itself marked as a subdevice. The other offline direct devices include an infrared controller and a multi-channel controller. The two online devices are standalone devices.

The SDK/HA registry exposes no parent-gateway links for these devices, so exact parent-child assignment cannot be asserted. An unavailable gateway is a plausible common cause for multiple unavailable children, but power versus Wi-Fi/LAN failure versus retired hardware has not been established remotely.

Device metadata timestamps are identical for activation, creation and update in this snapshot. They are not last-seen timestamps and must not be interpreted as the duration of an outage. No Tuya error categories were found in the bounded current container log read; diagnostics are the positive evidence, rather than absence of log entries.

No stale integration endpoint or failing authentication was established. No reload, reset, unpair, reauthentication, device switching or synthetic state publication was performed. The freshly restarted HA had already refetched the same cloud device set.

Home Assistant was subsequently updated to 2026.9.4. Fresh authenticated diagnostics still report the Tuya integration loaded and cloud MQTT connected, with the same 2 online and 12 offline devices. The update preserved all 91 entity IDs and did not restore device connectivity. The release contains a Tuya fan behavior fix, not a stated offline-device connectivity repair.

The next required observation is whether the two Tuya/Zigbee gateways are physically present, powered and connected to the current network, and whether Smart Life also marks them offline. If so, repair of that gateway connection should precede any child-device reconfiguration. If Smart Life instead shows them online, compare a fresh HA diagnostic snapshot to the app before changing account or pairing configuration.

Private raw diagnostics and device registry data are in `inventory-private.json` with mode 0600 under this mode-0700 directory. Only aggregated, identifier-free files are suitable for publication.

Sources:
- https://www.home-assistant.io/integrations/tuya/
- https://github.com/home-assistant/core/releases/tag/2026.9.4
- https://raw.githubusercontent.com/home-assistant/core/2026.9.3/homeassistant/components/tuya/diagnostics.py

## Passive local discovery

A single 25.03-second receive-only window listened on UDP 6666, 6667 and 7000. Zero datagrams were received and zero packets were sent. No local hosts were scanned and no device commands were issued. None of the known IDs were seen, including the two cloud-online devices. This observation does not establish device absence, loss of power, or a broken gateway; broadcast filtering and a different local network are also possible.

The standalone decoder uses the already installed Cryptodome library. Its framing/decryption was checked against the TinyTuya project's own `udp_helper.py`, `message_helper.py` and `header.py`; synthetic plaintext, 55AA AES/CRC, 6699 GCM and corrupted-tag cases passed before capture. No package was installed into HA. Only broadcasts matching the 14 known private IDs could have been retained; the private observation file is empty and mode 0600.
