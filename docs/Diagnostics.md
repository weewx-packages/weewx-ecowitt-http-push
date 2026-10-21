# Diagnostics

## Inspect one upload

Run with the station's `bin` directory on Python's import path. For a package
installation:

```sh
export PYTHONPATH=/etc/weewx/bin${PYTHONPATH:+:$PYTHONPATH}
python -m user.ecowitt --port 8001 --config /etc/weewx/weewx.conf
```

For a pip installation, substitute your station paths, commonly
`~/weewx-data/bin` and `~/weewx-data/weewx.conf`. Use the Python interpreter
from the WeeWX virtual environment when one is in use.

Temporarily point the console at port 8001, wait for an upload, then restore its
original port. WeeWX can keep running on its own port. The command changes no
configuration or data. It shows mapped readings, inferred fields, proposed
placements, suggested column commands and existing column history.

The column suggestions compare against the standard schema; check your actual
columns before applying them. See [Database columns](Database-columns.md).

| Option | Default | Meaning |
|---|---|---|
| `--port` | `8000` | Listening port |
| `--address` | All interfaces | Bind address |
| `--path` | Every path | Accept this path only |
| `--samples` | `1` | Uploads to collect |
| `--timeout` | `300` | Seconds to wait for each upload |
| `--config` | `/etc/weewx/weewx.conf` | History-check database and path in printed commands |
| `--infer-unknown` | `all` | Mapping mode: `off`, `series` or `all` |
| `--no-database` | Off | Skip the existing-history check |

The diagnostic uses its own mapping, not `field_map_extensions` from `--config`.
Its proposals therefore show the defaults and outstanding placement decisions.

## Read the automatic sensor report

```sh
cat /var/tmp/weewx-ecowitt-report.txt
```

The driver writes this when fields need attention. See [New sensors](New-sensors.md)
for its contents and how to report them.

## Inspect traffic and logs

* `ss -tlnp | grep 8000` identifies the process holding the port.
* `sudo tcpdump -i any -n port 8000` shows whether uploads reach the machine.
* To log raw bodies, set `log_raw = true` under `[Ecowitt]` and `debug = 1` at
  the top level, then restart WeeWX. Disable both afterwards; raw logs grow
  quickly and may contain identifiers or credentials. Redact them before sharing.

See [Troubleshooting](Troubleshooting.md) for response codes and missing readings.
