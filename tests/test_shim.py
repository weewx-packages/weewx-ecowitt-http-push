#
#    Copyright (c) 2026 Manuel Hilgert
#
#    See the file LICENSE for your full rights.
#
"""Check the HTTP listener that ships in bin/user."""

import pytest


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
