# Ecowitt HTTP Push for WeeWX

Receives the HTTP uploads sent by an Ecowitt gateway or console to a custom
server and turns them into WeeWX LOOP packets. Supports the Ecowitt and Weather
Underground upload protocols; Ecowitt carries more sensor fields. Reception is
local: the driver needs no Ecowitt cloud account, and it receives only the
fields the console actually uploads.

This is an own project of the weewx-packages organization. Its field catalog is
generated from Werner Krenn's
[ecowittcustom](https://github.com/WernerKr/Ecowitt-or-DAVIS-stations-and-Season-skin),
which descends from Matthew Wall's `weewx-interceptor`.

## Requirements

* An Ecowitt or Fine Offset gateway or console with **Customized** server
  upload. See the [hardware list](docs/Hardware.md) for gateways, consoles,
  sensors and Fine Offset variants.
* A network path from the console to the WeeWX machine on the listening port.
* No Python packages beyond WeeWX. The driver bundles a listener for WeeWX
  versions that do not provide `weewx.listener`.

## Installation

Install `ecowitt-http-push` from the [WeeWX packages catalog](https://github.com/weewx-packages/catalog/blob/main/packages/ecowitt-http-push.md).
The catalog page lists the current release, its WeeWX and Python
requirements, and the install, update and removal commands.

The installer adds an `[Ecowitt]` section but does not change the active
driver. Select the driver by its module path; the interactive driver list does
not show it:

```sh
weectl station reconfigure --driver=user.ecowitt.driver
```

Then point the console at WeeWX and restart WeeWX, as described in
[Installation and updates](docs/Installation.md).

## Configuration

A minimal station configuration is:

```ini
[Station]
    station_type = Ecowitt

[Ecowitt]
    driver = user.ecowitt.driver
    port = 8000
```

WeeWX records rain only when `rain` is listed under `[[Calculations]]` in
`[StdWXCalculate]`. The installer does not add that line. See
[Rain](docs/Configuration.md#rain). The
[configuration reference](docs/Configuration.md) lists the driver and
listener options with their defaults.

The field catalog covers known sensors; new channels can be inferred. Fields
whose placement is ambiguous, including WN34 probes and WH52 temperatures, wait
for your explicit mapping. The log and the [diagnostic command](docs/Diagnostics.md)
show what to configure. Add database columns for readings outside your schema
before expecting archive history. See [field mapping](docs/Field-map.md) and
[database columns](docs/Database-columns.md).

The [documentation index](docs/Home.md) lists all pages, including
[several consoles](docs/Several-consoles.md),
[network access](docs/Security.md) and
[troubleshooting](docs/Troubleshooting.md).

## Limitations

* A console's `PASSKEY` keeps consoles apart but does not authenticate them.
  The listener speaks plain HTTP. See [Network access](docs/Security.md).
* Some catalog fields use unit groups that WeeWX does not define. With
  `[StdConvert] target_unit` other than `US`, a packet containing one of them
  stops WeeWX. See [Units and archive storage](docs/Field-map.md#units-and-archive-storage).

## Development

```sh
python -m pytest tests -q
```

See [Development](docs/Development.md) for the test environment, catalog
generation and releases.

## License

Copyright (c) 2026 Manuel Hilgert. The generated field catalog also carries
Copyright (c) 2016-2020 Matthew Wall and Copyright (c) 2025-2026 Werner Krenn.
Licensed under the GNU General Public License, version 3. See
[LICENSE](LICENSE). WeeWX is by Tom Keffer and Matthew Wall.
