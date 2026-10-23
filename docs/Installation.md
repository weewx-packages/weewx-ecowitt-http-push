# Installation and updates

Release 0.3.2 requires WeeWX >=5,<6, Python >=3.7 and a gateway or console with
**Customized** server upload. No additional Python packages are required. See [Hardware](Hardware.md).

## Install

Use the `weectl` from your WeeWX Python environment. Add
`--config=/path/to/weewx.conf` to target a specific station.

```sh
weectl extension install https://github.com/weewx-packages/weewx-ecowitt-http-push/releases/download/v0.3.2/weewx-ecowitt-http-push-0.3.2.zip
weectl station reconfigure
```

Select **Ecowitt**. The installer configures `[Ecowitt]`,
`driver = user.ecowitt.driver` and rain calculation. These technical names remain
compatible with earlier versions. A downloaded copy of the same release
archive can replace the URL.

Stock WeeWX 5.5.2 has no extension repository, search or update commands and does
not resolve package IDs. The separately developed
[weewx-package-manager](https://github.com/weewx-packages/weewx-package-manager)
is experimental, unreleased and outside the catalog. It is not required for
this installation. Use the archive commands on this page.

## Configure the hardware

In **WS View Plus → Weather Services → Customized**:

| Field | Value |
|---|---|
| Protocol Type | **Ecowitt**; Wunderground also works but carries fewer fields |
| Server IP / Hostname | WeeWX machine's reachable address |
| Path | `/`, or the configured `path` |
| Port | **8000**, or the configured `port` |
| Upload Interval | **60 seconds**; supported intervals depend on the hardware |

Save and reopen the page to verify the settings. Before starting WeeWX, you can
[inspect one upload](Diagnostics.md) on port 8001, then restore port 8000.

```sh
sudo systemctl restart weewx
sudo journalctl -u weewx -f
```

Within one upload interval, look for `Listening for HTTP requests` and incoming
readings. Resolve fields waiting for a [mapping](Field-map.md), then add any
needed [archive columns](Database-columns.md).

## Update or remove

Read the [changelog](https://github.com/weewx-packages/weewx-ecowitt-http-push/blob/main/CHANGELOG.md)
for changed field placements. Back up your station configuration and database.
Stop WeeWX, install the fixed release URL shown above over the existing
extension, review `[Ecowitt]` and rain calculation settings, then start WeeWX.
The installed extension is named `ecowitt`. For a later release, use that
release's published archive URL. Installation does not restart WeeWX.

To remove the driver, run `weectl extension uninstall ecowitt`, select another
driver with `weectl station reconfigure`, then restart WeeWX. Archive data remains.

<!-- Documentation updated 2026-10-23 by weewx-packages. -->
