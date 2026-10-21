# Unknown fields

The driver examines unknown names once per run. Restart it to repeat the messages.

| `infer_unknown` | Behaviour |
|---|---|
| `off` | Log and drop all unknown fields |
| `series` | Accept fields derived from known channel patterns when placement is unambiguous; log other proposals. Default. |
| `all` | Also accept naming-based guesses; units may be wrong. Used by the diagnostic command. |

Explicit [mappings](Field-map.md) override these modes. Catalog fields requiring a
placement decision remain withheld until mapped.

## Derived channels and guesses

A derived channel extends a known series, such as `zz_ch3` when `zz_ch1` and
`zz_ch2` are mapped. Channels beyond the hardware's published limit are reported
as guesses. Families with ambiguous placement wait for a mapping in `series` mode.

Other names suggest a quantity and unit. Guesses use `ecowitt_` plus the raw name
as their field name unless a known series supplies a destination.

| Name pattern | Inferred quantity / unit |
|---|---|
| `rssi`, `_sig` | Signal strength / dB; signal quality / count |
| `batt`, `_time` | Battery; timestamp |
| `barom...in` | Pressure / inHg |
| `rain...in`, `rain...piezo` | Rain / inches |
| `mph`, `winddir...` | Speed / mph; direction / degrees |
| `temp...`, `tf_...`, `soiltemp`, `thermo` | Temperature / °F |
| `humidity`, `moisture`, `_hum` | Percent |
| `pm1`, `pm4`, `pm10`, `pm25` | Concentration / µg/m³ |
| `co2`, `co` | Concentration / ppm |
| `solarradiation`, `radiation` | Radiation / W/m² |
| `uv`, `vpd` | UV index; pressure / kPa |
| `depth_ch`, `air_ch`, `thi_ch` | Distance / mm |

Names with no recognised pattern are logged and dropped even in `all` mode.
[Report new sensors](New-sensors.md) so quantities and units can be verified and
added to the catalog. Accepted fields also need [archive columns](Database-columns.md).
