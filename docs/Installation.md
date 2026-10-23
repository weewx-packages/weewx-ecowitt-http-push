# Installation and updates

The driver needs a gateway or console with **Customized** server upload and no
additional Python packages. See [Hardware](Hardware.md).

## Install

Install `ecowitt-http-push` from the [WeeWX packages catalog](https://github.com/weewx-packages/catalog/blob/main/packages/ecowitt-http-push.md).
The catalog page lists the current release, its WeeWX and Python
requirements, and the install, update and removal commands.

The installer adds an `[Ecowitt]` section with `driver = user.ecowitt.driver`,
`port = 8000` and `infer_unknown = series`, and a `[[Delta]]` entry for rain.
It adds only settings that are missing and leaves the active driver unchanged.
Select the driver by its module path; the interactive driver list of
`weectl station reconfigure` does not show it:

```sh
weectl station reconfigure --driver=user.ecowitt.driver
```

Add `--config=/path/to/weewx.conf` to target a specific station. Then complete
the [rain configuration](Configuration.md#rain).

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

At startup the log shows `Listening for HTTP requests`. On a new installation,
the first upload is logged with the console that the driver now answers to; see
[console identities](Several-consoles.md). Resolve fields waiting for a
[mapping](Field-map.md), then add any needed [archive columns](Database-columns.md).

## Update or remove

The catalog page lists the update and removal commands. The installed extension
is named `ecowitt`.

Before an update, read the [changelog](https://github.com/weewx-packages/weewx-ecowitt-http-push/blob/main/CHANGELOG.md)
for changed field placements and back up your station configuration and
database. Stop WeeWX, update, review `[Ecowitt]` and the rain settings, then
start WeeWX. An update adds missing settings and leaves existing ones
unchanged. Installation does not restart WeeWX.

Removal deletes `station_type` from `[Station]`, whichever driver it names,
together with the options the installer adds to `[Ecowitt]` and `[[Delta]]`,
even if you changed their values. Select
another driver with `weectl station reconfigure`, then restart WeeWX. Archive
data remains.
