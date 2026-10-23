# Network access

The listener accepts HTTP weather uploads. A console's `PASSKEY` identifies it
and prevents accidental mixing, but does not prove who sent a request. See
[console identities](Several-consoles.md).

Restrict access to the station's network and use the controls that your hardware
can send:

| Control | Example | Effect |
|---|---|---|
| `address` | `192.168.1.10` | Listen on that interface only |
| `path` | `/a8f3c1e0-4b2d/report` | Other paths receive HTTP 404 |
| `allowed_hosts` | `192.168.1.42, 192.168.1.43` | Other addresses receive HTTP 403; keep DHCP assignments stable |
| `token` | A private random value | Require query parameter `token`, `X-Auth-Token`, or `Authorization: Bearer`; mismatch receives HTTP 403 |

Most consoles can configure a path but not custom headers. Generate a private path:

```sh
python -c "import secrets; print('/%s/report' % secrets.token_hex(8))"
```

These settings do not encrypt the connection or prevent forged readings from
someone who knows the credentials. For uploads across untrusted networks, use a
VPN or an HTTPS-capable relay. A TLS reverse proxy cannot encrypt the connection
from a console that sends plain HTTP.

## Behind a trusted local proxy

```ini
[Ecowitt]
    address = localhost
    port = 8000
    path = /a8f3c1e0-4b2d/report
    trust_proxy = true
```

For nginx:

```nginx
location /a8f3c1e0-4b2d/report {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header X-Forwarded-For $remote_addr;
}
```

For Caddy, inside the site's configuration:

```caddy
handle /a8f3c1e0-4b2d/report {
    reverse_proxy 127.0.0.1:8000
}
```

Enable `trust_proxy` only when the listener is reachable solely through a proxy
you control. It makes `allowed_hosts` check the forwarded client address;
otherwise it would see the proxy's address. The listener takes the last
address in `X-Forwarded-For`, the one the proxy added. Earlier entries come from
the client and are ignored. This assumes a single proxy in front of the
listener.

The default body limit is 65536 bytes; larger uploads receive HTTP 413. Restart
WeeWX after changes and update the console to match, or uploads will be rejected.
