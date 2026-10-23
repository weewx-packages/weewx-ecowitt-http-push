# Configuration

Options belong in `[Ecowitt]` in `weewx.conf`. A minimal station uses:

```ini
[Station]
    station_type = Ecowitt

[Ecowitt]
    driver = user.ecowitt.driver
    port = 8000
```

Restart WeeWX after changes. Set the console's address, port and path to match;
see [Installation](Installation.md).

## Driver options

| Option | Default | Meaning |
|---|---|---|
| `driver` | Required | `user.ecowitt.driver` |
| `model` | `Ecowitt` | Station name shown in reports, for example `HP2561AE Pro` |
| `infer_unknown` | `series` | Accept known channel patterns; `off` drops unknowns and `all` also accepts guesses. See [Unknown fields](Unknown-fields.md). |
| `field_map_extensions` | Empty subsection | Raw field → WeeWX field, overriding the catalog. See [Field map](Field-map.md). |
| `report_file` | `/var/tmp/weewx-ecowitt-report.txt` | Diagnostic upload report; empty disables it. See [New sensors](New-sensors.md). |
| `max_behind` | `3600` | Maximum age in seconds of a console's timestamp |
| `max_ahead` | `60` | Maximum number of seconds its clock may be ahead |
| `passkey` | Learned from first console | Accept this console's `PASSKEY`, or Wunderground `ID` |
| `console_file` | Automatic fallback path | File used when the console list cannot be stored in the database |
| `data_binding` | `wx_binding` | Database binding used to retain console identities |
| `stations` | Empty subsection | Console-specific identities and mappings. See [Several consoles](Several-consoles.md). |

The driver uses the console's UTC `dateutc` within the configured clock window;
missing, invalid or out-of-range timestamps use arrival time. Out-of-range times
produce a warning. The driver does not decide whether WeeWX can revise an archive
record for a late packet. If your WeeWX installation cannot revise archived
intervals, use a smaller `max_behind`, such as `90`.

## Rain

Ecowitt sends rain as running counters such as `dailyrainin`, which the driver
maps to `dayRain`. WeeWX derives the packet's `rain` from such a counter with
its `Delta` type, and it computes `rain` only when it is listed under
`[[Calculations]]`. Both entries are needed:

```ini
[StdWXCalculate]
    [[Calculations]]
        rain = prefer_hardware
    [[Delta]]
        [[[rain]]]
            input = dayRain
```

The installer adds both entries where they are missing. A `rain` line you have
already set under `[[Calculations]]` stays as it is. With `rain = hardware`,
WeeWX does not derive `rain` and it stays empty.

When the daily counter resets at midnight, WeeWX logs a counter reset and
records no rain for that one packet.

## Listener options

| Option | Default | Meaning |
|---|---|---|
| `port` | `80`; installer sets `8000` | Listening port; ports below 1024 may require elevated privileges |
| `address` | All interfaces | Bind address; use `localhost` behind a local proxy |
| `path` | Every path | Accept only this path; other paths receive HTTP 404 |
| `token` | None | Require query parameter `token`, header `X-Auth-Token` or an `Authorization: Bearer` token |
| `allowed_hosts` | Any address | Comma-separated client addresses; rejected clients receive HTTP 403 |
| `trust_proxy` | `False` | Use `X-Forwarded-For` as client address; enable only behind a trusted proxy |
| `max_body` | `65536` | Maximum upload size in bytes; larger requests receive HTTP 413 |
| `socket_timeout` | `20` | Idle connection timeout in seconds |
| `queue_size` | `10` | Maximum queued uploads; a full queue drops the oldest and logs a warning |
| `log_raw` | `False` | Log upload bodies at debug level; may expose station identifiers |

See [Security](Security.md) for access restrictions and a proxy example.
For two independent weather stations, run separate WeeWX instances with distinct
configurations, databases and ports. A web server can share the machine on another
port. To combine consoles in one instance, use [Several consoles](Several-consoles.md).
