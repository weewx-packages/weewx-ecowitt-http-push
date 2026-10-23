# Ecowitt HTTP Push for WeeWX

Receives the HTTP uploads sent by an Ecowitt gateway or console to a custom
server and turns them into WeeWX LOOP packets. Supports the Ecowitt and Weather
Underground upload protocols; Ecowitt carries more sensor fields.

Release 0.3.2 requires WeeWX >=5,<6, Python >=3.7 and hardware with
**Customized** server upload.
See the [hardware list](docs/Hardware.md) for gateways, consoles, sensors and
Fine Offset variants.

## Install

```sh
weectl extension install https://github.com/weewx-packages/weewx-ecowitt-http-push/releases/download/v0.3.2/weewx-ecowitt-http-push-0.3.2.zip
weectl station reconfigure
```

Select **Ecowitt**. In WS View Plus, open *Weather Services → Customized*, select
**Ecowitt**, and set the WeeWX machine's address, port **8000**, path **/** and
an upload interval of **60 seconds**. Restart WeeWX.

Use the `weectl` from your WeeWX Python environment. Add
`--config=/path/to/weewx.conf` to target another station. Stock WeeWX accepts the
fixed URL above or a downloaded archive. For updates, repeat the archive install
as described in [Installation and updates](docs/Installation.md).

A minimal station configuration is:

```ini
[Station]
    station_type = Ecowitt
[Ecowitt]
    driver = user.ecowitt.driver
    port = 8000
```

The installer also configures rainfall calculation from `dayRain`. It bundles a
listener for WeeWX versions that do not provide one. No extra Python packages
are required. This is local HTTP reception; the driver needs no Ecowitt cloud
account. Only fields actually uploaded by the console can reach WeeWX.

## Keep every reading

The field catalog covers known sensors; new channels can be inferred. Fields
whose placement is ambiguous, including WN34 probes and WH52 temperatures, wait
for your explicit mapping. The log and [diagnostic command](docs/Diagnostics.md)
show what to configure. Add database columns for readings outside your schema
before expecting archive history. See [field mapping](docs/Field-map.md) and
[database columns](docs/Database-columns.md).

## Documentation

* [Installation and updates](docs/Installation.md) · [Configuration](docs/Configuration.md)
* [Hardware](docs/Hardware.md) · [Sensor fields](docs/Sensors.md) · [Unknown fields](docs/Unknown-fields.md)
* [Several consoles](docs/Several-consoles.md) · [Network access](docs/Security.md)
* [Troubleshooting](docs/Troubleshooting.md) · [Report a sensor](docs/New-sensors.md)
* [Development](docs/Development.md) · [Changelog](CHANGELOG.md)

## Credits and licence

GPLv3. The field catalog is generated from Werner Krenn's
[ecowittcustom](https://github.com/WernerKr/Ecowitt-or-DAVIS-stations-and-Season-skin),
which descends from Matthew Wall's `weewx-interceptor`. WeeWX is by Tom Keffer
and Matthew Wall. See [Development](docs/Development.md) for catalog generation.

<!-- Documentation updated 2026-10-23 by weewx-packages. -->
