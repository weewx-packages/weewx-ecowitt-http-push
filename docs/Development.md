# Development

| Path | Purpose |
|---|---|
| `bin/user/ecowitt/protocol.py` | Parse uploads and console timestamps |
| `catalog.py`, `infer.py`, `mapping.py` | Generated fields, inference and packet mapping |
| `columns.py`, `consoles.py`, `report.py` | Archive checks, console identities and sensor reports |
| `driver.py`, `__main__.py` | WeeWX driver and diagnostic command |
| `bin/user/listener.py` | HTTP listener that receives the uploads |
| `tools/`, `tests/fixtures/` | Generators and redacted captured uploads |

## Tests

Clone this repository and enter its root before running development commands.
Use a separate development virtual environment:

```sh
git clone https://github.com/weewx-packages/weewx-ecowitt-http-push.git
cd weewx-ecowitt-http-push
python -m venv .venv
. .venv/bin/activate
```

```sh
python -m pip install weewx pytest
python -m pytest tests -q
```

The command above includes WeeWX integration tests. `.github/workflows/ci.yml`
runs the tests on several Python versions, with and without WeeWX, and checks
syntax compatibility with vermin. The listener in `bin/user/listener.py`
belongs to this project.

## Catalog and references

Run these commands from the checkout above. Obtain the source
`ecowittcustom.py` and WeeWX's `schemas/wview_extended.py` before importing a
catalog, and replace the placeholder paths with those files.

```sh
python tools/import_catalog.py path/to/ecowittcustom.py \
    --schema path/to/weewx/schemas/wview_extended.py
python tools/build_reference.py
python tools/build_hardware.py
```

Edit the generator's `CHANNELS`, `REMAP` and `OVERRIDES`, then regenerate.
`CONTESTED` derives from those placement decisions. Review reported collisions,
alternative destinations and raw names without targets. Give new observations a
unit group, add a channel family and count where needed, and capture a redacted
payload with an expected-output test.

`Sensors.md` and `Hardware.md` are generated. Change their generators, not the
output. Hardware descriptions live in `tools/build_hardware.py`; its field lists
come from the catalog and its final section lists unidentified fields.

`python tools/check_against_ecowitt.py` compares channel counts with Ecowitt's
published API. It cannot verify custom-upload names, which differ from cloud API
names. See [New sensors](New-sensors.md) for payload evidence.

## Releases and wiki

Update `VERSION` in `install.py` and `bin/user/ecowitt/__init__.py`, add a
changelog entry, run tests, then push a matching `vX.Y.Z` tag. The release workflow
checks both versions and publishes the ZIP. Register its URL and SHA-256 in the
[shared catalog](https://github.com/weewx-packages/catalog), following that
project's contribution guide. Keep the existing installer name `ecowitt` and
module path `user.ecowitt.driver` stable.

The wiki mirrors `docs/`. Publish the same pages to the wiki checkout, removing
`.md` from local page links there; keep the source links intact for GitHub browsing.
