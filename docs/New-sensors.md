# Reporting a new sensor

When an upload contains inferred or undecided fields, the driver writes a report
at most once per start:

```sh
cat /var/tmp/weewx-ecowitt-report.txt
```

Paste it into a [sensor issue](https://github.com/weewx-packages/weewx-ecowitt-http-push/issues/new/choose).
It includes the raw upload, model and firmware where supplied, mapping proposals
and fields awaiting a decision. Known credentials, including `PASSKEY`, `ID` and
`PASSWORD`, are redacted; review the contents before publishing.

For a new sensor type, also provide its model and the value, unit and time shown
in WS View Plus for the same upload. That comparison identifies what a new raw
field measures. Channel extensions may work through inference; new quantities
need a verified catalog entry in a release.

`report_file` changes the output path; an empty value disables it. If no file
appears, also check the path, write permissions and log. Completely unrecognised
names can be logged without generating this report. Use
[Diagnostics](Diagnostics.md) to capture an upload directly.

For an immediate mapping, add the raw name under `[[field_map_extensions]]` and
ensure its destination has an [archive column](Database-columns.md). Please still
report the sensor so other stations can receive a verified mapping.
