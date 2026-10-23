# Field mapping

A console's raw field becomes a WeeWX observation, then an archive column.
Mapping priority is:

1. Your `field_map_extensions`.
2. The built-in [sensor catalog](Sensors.md).
3. [Inference](Unknown-fields.md) for unknown fields.

```ini
[Ecowitt]
    [[field_map_extensions]]
        tf_ch1 = soilTemp5
        soilmoisture1 = soilMoist1
```

The left side is the uploaded name; the right side is your chosen WeeWX field.
The driver does not validate whether that placement fits your physical sensor.

## Fields requiring a choice

Some fields are withheld until explicitly mapped. WN34 S/L/D probes send the same
names for soil, water and other temperatures. Other fields have competing
placements in earlier drivers. Choose a destination consistent with your sensor
and its existing history; two sensors mixed in one column cannot be separated
later. `python -m user.ecowitt --port 8001` prints candidate mappings.

| Sensor | Raw field | Catalog placement |
|---|---|---|
| WH31 and relatives | `temp1f`, `humidity1` | `extraTemp1..8`, `extraHumid1..8` |
| WN34 S/L/D | `tf_ch1..8` | `extraTemp9..16`, requires explicit mapping |
| WN35 | `leafwetness_ch1..8` | `leafWet1..8` |
| WH51 / WH52 moisture | `soilmoisture1..16` / `soil_ec_hum1..16` | `soilMoist1..16` |
| WH52 temperature | `soil_ec_temp1..16` | `soilTemp1..16`, requires explicit mapping |
| WH52 conductivity | `soil_ec1..16` | `soilEC1..16` |
| WH41 / WH43 | `pm25_ch1..4` | `pm25_1..4` |
| WH55 | `leak_ch1..4` | `leak_1..4` |
| WH57 | `lightning`, `lightning_num` | `lightning_distance`, `lightning_num` |
| WH54 / LDS01 | `air_ch1..4`, `depth_ch1..4` | Same names |

WH51 and WH52 share a pool of 16 channels. If `soilmoisture3` and `soil_ec_hum3`
arrive together, the driver warns about their shared destination. Map one elsewhere,
for example `soil_ec_hum3 = soilMoist11`, before combining their histories.

## Units and archive storage

The catalog supplies unit groups; the driver registers only fields WeeWX does not
already know. LOOP packets use US units: °F, inHg, inches and mph. WeeWX handles
subsequent unit conversion and report formatting.

The driver adds five unit groups that WeeWX does not define, with the units of
the ecowittcustom driver:

| Group | Fields | US | METRIC, METRICWX |
|---|---|---|---|
| `group_dbm` | `_rssi` fields | dBm | dBm |
| `group_lengthmm` | `air_ch1..4`, `depth_ch1..4`, `thi_ch1..4` | mm | mm |
| `group_pressurevpd` | `vpd` | inHg | kPa |
| `group_sunhours` | `fsunhours` | h | h |
| `group_usiecm` | `soilEC1..16` | µS/cm | µS/cm |

A group that WeeWX or another extension has already defined when the driver
loads keeps that definition.

Use [Diagnostics](Diagnostics.md) to inspect mappings, and
[Database columns](Database-columns.md) to retain readings outside your schema.
