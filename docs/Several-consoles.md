# Console identities and several consoles

Each console numbers its channels from one. Accepting two consoles into the same
fields would mix their histories, so the driver accepts known identities and
ignores other consoles, with one warning per unknown identity.

## One console

Without a configured identity, the first upload establishes the console. The
identity persists across restarts, in this order:

1. `passkey` or `[[stations]]` in `weewx.conf`.
2. The archive binding's daily-summary metadata, under `ecowitt_consoles`.
3. A text file when the database is unavailable.

The fallback file is `ecowitt-consoles.txt` in the first writable existing
directory among `SQLITE_ROOT` and `WEEWX_ROOT`, otherwise
`/var/tmp/weewx-ecowitt-consoles.txt`. A relative `SQLITE_ROOT`, such as
`archive` in a pip installation, is relative to `WEEWX_ROOT`, as for the
database. `console_file` overrides that path. If
neither database nor file can be written, learning is temporary; another console
could be adopted after a restart. A configured identity avoids that dependency:

```ini
[Ecowitt]
    passkey = YOUR_CONSOLE_PASSKEY
```

Find the value in an upload using [Diagnostics](Diagnostics.md), or in the
fallback file if used. Keep it out of public reports. Wunderground's `ID` is used
in place of `PASSKEY`. An upload with neither has no distinguishable identity:
while no console is known it is read but not learned, and once a console is
known it is ignored.
An identity prevents accidental mixing; it does not authenticate the hardware.

## Several consoles in one instance

Give every console a name, identity and mapping:

```ini
[Ecowitt]
    driver = user.ecowitt.driver
    port = 8000

    [[stations]]
        [[[garden]]]
            passkey = FIRST_PASSKEY
            [[[[field_map_extensions]]]]
                tf_ch1 = soilTemp1

        [[[roof]]]
            passkey = SECOND_PASSKEY
            [[[[field_map_extensions]]]]
                tf_ch1 = extraTemp12
```

Restart WeeWX. Each console has its own mapper; each packet includes its
configured name as `station`. Console subsections can override `infer_unknown`.
Explicit maps must account for any fields the consoles would otherwise share,
including common observations such as `outTemp`. There is no automatic namespace
for them; the example only separates the probes shown.

For independent stations with separate standard observations and archives, run
[separate WeeWX instances](Configuration.md).

## Replace a console or gateway

Sensors moved to another gateway acquire that gateway's identity. Update the
configured `passkey` or `[[stations]]` entry and restart WeeWX. To reset automatic
learning, clear the recorded identity from the storage actually in use. Deleting
only the fallback file does not clear an identity held in database metadata.
Do not add a second console by editing the fallback file; configure its identity
and mapping under `[[stations]]`.
