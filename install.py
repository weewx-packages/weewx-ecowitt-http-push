#
#    Copyright (c) 2026 Manuel Hilgert
#
#    See the file LICENSE for your full rights.
#
"""Installer for the Ecowitt HTTP Push driver."""

from weecfg.extension import ExtensionInstaller

VERSION = '0.3.2'


def loader():
    return EcowittInstaller()


class EcowittInstaller(ExtensionInstaller):
    def __init__(self):
        super(EcowittInstaller, self).__init__(
            version=VERSION,
            name='ecowitt',
            description='Ecowitt HTTP Push driver for custom-server uploads.',
            author="Manuel Hilgert",
            author_email="hilman2@gmail.com",
            # No [Station] station_type here. Installing would not change a value that
            # is already set, but uninstalling removes every option listed here, and
            # would take whichever driver is selected with it. The driver is chosen
            # with 'weectl station reconfigure --driver=user.ecowitt.driver'.
            config={
                # Ecowitt hardware sends rain as running counters, never as the
                # amount since the last upload. WeeWX wants 'rain', the amount in
                # the packet, and StdDelta is what turns one into the other. Without
                # this the station records no rain at all: every counter arrives and
                # 'rain' stays empty. StdWXCalculate computes only the types listed
                # under [[Calculations]], and the stock weewx.conf does not list
                # 'rain', so both entries are needed. Installing adds them only
                # where they are missing.
                'StdWXCalculate': {
                    'Calculations': {
                        'rain': 'prefer_hardware'},
                    'Delta': {
                        'rain': {
                            'input': 'dayRain'}}},
                'Ecowitt': {
                    'driver': 'user.ecowitt.driver',
                    'port': '8000',
                    'infer_unknown': 'series',
                    # 'compat' is deliberately absent. Fields that drivers place
                    # differently stay out until somebody says which placement is
                    # wanted, because the wrong one cannot be undone.
                    'field_map_extensions': {}}},
            files=[
                ('bin/user', ['bin/user/listener.py']),
                # Every module in the package. A test keeps this list complete,
                # because a missing one shows up as an ImportError on somebody else's
                # machine and nowhere earlier.
                ('bin/user/ecowitt', ['bin/user/ecowitt/__init__.py',
                                      'bin/user/ecowitt/__main__.py',
                                      'bin/user/ecowitt/catalog.py',
                                      'bin/user/ecowitt/columns.py',
                                      'bin/user/ecowitt/consoles.py',
                                      'bin/user/ecowitt/driver.py',
                                      'bin/user/ecowitt/infer.py',
                                      'bin/user/ecowitt/mapping.py',
                                      'bin/user/ecowitt/protocol.py',
                                      'bin/user/ecowitt/report.py']),
            ]
        )
