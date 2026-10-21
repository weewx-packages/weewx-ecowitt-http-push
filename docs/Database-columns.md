# Database columns

A reading needs an archive column to retain history. Without one it may appear as
a current value, but is not archived. The standard extended schema includes:

| Observation series | Channels |
|---|---|
| `extraTemp`, `extraHumid`, `batteryStatus`, `signal` | 1..8 |
| `soilTemp`, `soilMoist` | 1..4 |
| `leafTemp`, `leafWet` | 1..2 |

Higher channels and families such as `air_ch`, `depth_ch`, `soilEC`, `pm25_` and
`leak_` require additional columns or a custom schema.

## Find and add columns

Run the [diagnostic command](Diagnostics.md#inspect-one-upload) with your
`--config` path, send one upload to its port, then restore the console's port.
The command compares mapped readings with WeeWX's standard schema and prints `weectl database add-column`
commands. Check your actual schema before running them; existing custom columns may
already cover the readings. `--config` selects the database for the history check
and the configuration path included in the printed commands.

Back up before changing columns; adding a column can rewrite the archive table.
For SQLite, stop WeeWX and copy the actual database, for example:

```sh
sudo systemctl stop weewx
cp /var/lib/weewx/weewx.sdb /var/lib/weewx/weewx.sdb.backup
weectl database add-column soilEC1 --type REAL --config /etc/weewx/weewx.conf -y
sudo systemctl start weewx
```

The diagnostic chooses `INTEGER` for `group_count`, `group_time`, `group_boolean`
and `group_data`; measured quantities use `REAL`.

## Preserve existing history

The diagnostic also reports populated columns and their latest timestamps. Reuse a
column only for the same physical sensor. If an earlier driver used another
placement, rename the column while WeeWX is stopped and adjust the mapping:

```sh
weectl database rename-column soilTemp1 extraTemp9 --config /etc/weewx/weewx.conf -y
```

Renaming retains history; changing only the mapping starts a separate series.
For new stations, a custom schema can include the additional columns from the
outset. Configure it through `[DataBindings]` as described in WeeWX's database guide.
