# Ecowitt HTTP Push for WeeWX

Receives the HTTP uploads sent by an Ecowitt gateway or console to a custom
server and turns them into WeeWX LOOP packets. Supports the Ecowitt and Weather
Underground upload protocols; Ecowitt carries more sensor fields.

Requires WeeWX 5.0+, Python 3.7+ and hardware with **Customized** server upload.
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

With a WeeWX build that supports repositories, the
[shared package catalog](https://github.com/weewx-packages/catalog) also provides
`weectl extension install ecowitt-http-push` and subsequent updates.

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
