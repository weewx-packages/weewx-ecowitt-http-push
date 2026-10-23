# Troubleshooting

| Symptom | Check |
|---|---|
| No listener startup message | `station_type = Ecowitt` and `[Ecowitt] driver = user.ecowitt.driver` |
| Nothing reaches the port | Console address, port, protocol, saved settings, firewall and network segment; inspect with `tcpdump` as described in [Diagnostics](Diagnostics.md) |
| Address already in use | Identify the owner with `ss -tlnp`; stop it or change both listener and console ports |
| Uploads stop after a DHCP change | Update `allowed_hosts` or use a stable console address |
| Driver stops after suspend | Check preceding logs and restart WeeWX |
| Queue full warning | Increase `queue_size` or reduce upload frequency; the oldest request is dropped |
| Archive gaps | Ensure uploads arrive during each archive interval; inspect network and queue warnings |
| Implausible units | Packets use US units. Verify report conversion and the unit group of any inferred field |

For firewall rules, permit only the necessary source addresses and TCP port. If
using ufw, its port syntax is `sudo ufw allow 8000/tcp`; choose restrictions that
fit your network.

## HTTP responses

With `curl` installed and WeeWX's listener running on this host, test the
default URL below. Adapt it to any configured path, token and address
restrictions before sending the request. The test body carries no reading.

```sh
curl -s -o /dev/null -w '%{http_code}\n' -X POST -d 'stationtype=test' http://localhost:8000/
```

HTTP 200 confirms listener acceptance, not mapping or archival of every field.
The listener answers before the driver checks the console identity. The test
body carries no `PASSKEY`, so the driver does not adopt it as the station's
console.

| Code | Meaning |
|---|---|
| `200` | Upload accepted by the listener |
| `404` | Path mismatch |
| `400` | Invalid `Content-Length` header |
| `403` | Token or client address rejected |
| `413` | Body exceeds `max_body` |

## A sensor is missing

Check, in order:

1. Does the console show and upload the sensor? Inspect one upload with [Diagnostics](Diagnostics.md).
2. Is the field awaiting an explicit [mapping](Field-map.md), or an unknown field needing a [sensor report](New-sensors.md)?
3. Does the archive have the required [column](Database-columns.md)?
4. Does the skin include the destination observation?

If WH51 and WH52 fields collide, assign separate destinations as described in
[Field mapping](Field-map.md#fields-requiring-a-choice). Readings already mixed
cannot be separated afterwards.

## Rain stays empty

Ecowitt sends counters, and WeeWX derives packet rainfall from `dayRain`. Check
both entries described under [Rain](Configuration.md#rain). The installer adds
them only where they are missing and does not replace `rain = hardware` under
`[[Calculations]]`.

## Report a problem

Include relevant logs with preceding lines, diagnostic output, console model and
firmware, and `weectl --version`. Redact credentials from manually captured uploads.
[Open an issue](https://github.com/weewx-packages/weewx-ecowitt-http-push/issues).
