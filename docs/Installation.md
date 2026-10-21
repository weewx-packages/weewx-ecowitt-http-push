# Installation and updates

Requires WeeWX 5.0+, Python 3.7+ and a gateway or console with **Customized**
server upload. No additional Python packages are required. See [Hardware](Hardware.md).

## Install

```sh
weectl extension install https://github.com/weewx-packages/weewx-ecowitt-http-push/releases/download/v0.3.2/weewx-ecowitt-http-push-0.3.2.zip
weectl station reconfigure
```

Select **Ecowitt**. The installer configures `[Ecowitt]`,
`driver = user.ecowitt.driver` and rain calculation. These technical names remain
compatible with earlier versions. To install a checkout, pass its directory to
`weectl extension install` instead.

With a repository-enabled WeeWX build, register the shared catalog once:

```sh
weectl extension repo add packages https://raw.githubusercontent.com/weewx-packages/catalog/main/repository.json
weectl extension install ecowitt-http-push
weectl station reconfigure
```

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
for changed field placements. Install the new release over the existing one, or
run `weectl extension update ecowitt` when using the catalog. The installed
extension is named `ecowitt`. Existing
`[Ecowitt]` settings are retained. Restart WeeWX afterwards.

To remove the driver, run `weectl extension uninstall ecowitt`, select another
driver with `weectl station reconfigure`, then restart WeeWX. Archive data remains.
