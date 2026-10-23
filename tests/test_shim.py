#
#    Copyright (c) 2026 Manuel Hilgert
#
#    See the file LICENSE for your full rights.
#
"""Keep the bundled listener identical to the one in WeeWX.

The copy in bin/user exists so that this driver runs on WeeWX older than 5.6, which
does not carry weewx.listener yet. It is the same file, and it has to stay the same
file. A copy that drifts is a fork, which is the thing this whole exercise is meant to
get rid of.
"""

import hashlib
import os.path

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
SHIM = os.path.join(os.path.dirname(HERE), 'bin', 'user', 'listener.py')


def digest(path):
    with open(path, 'rb') as fd:
        return hashlib.sha256(fd.read().replace(b'\r\n', b'\n')).hexdigest()


def test_the_bundled_listener_matches_weewx():
    weewx_listener = pytest.importorskip(
        'weewx.listener', reason="WeeWX with a listener is not installed")

    assert digest(SHIM) == digest(weewx_listener.__file__)


def test_the_bundled_listener_is_importable():
    """However old the WeeWX, the bundled copy has to work."""
    pytest.importorskip('weeutil', reason="WeeWX is not installed")
    import user.listener as bundled

    assert hasattr(bundled, 'HTTPListener')
    assert hasattr(bundled, 'UDPListener')


def test_a_proxy_is_trusted_for_the_address_it_added():
    """A client can send X-Forwarded-For itself, and a proxy appends to it."""
    import http.client

    pytest.importorskip('weeutil', reason="WeeWX is not installed")
    import user.listener as bundled

    listener = bundled.HTTPListener(port=0, address='127.0.0.1', trust_proxy=True,
                                    allowed_hosts='192.168.1.42')

    def status(forwarded):
        connection = http.client.HTTPConnection('127.0.0.1', listener.port, timeout=5)
        try:
            connection.request('POST', '/', 'tempf=1', {'X-Forwarded-For': forwarded})
            return connection.getresponse().status
        finally:
            connection.close()

    try:
        assert status('192.168.1.42, 203.0.113.9') == 403
        assert status('203.0.113.9, 192.168.1.42') == 200
    finally:
        listener.close()
