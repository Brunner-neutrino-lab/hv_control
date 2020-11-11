# This file is part of hv_control.

# hv_control is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# hv_control is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with hv_control.  If not, see <https://www.gnu.org/licenses/>.

from ipaddress import IPv4Address

import pytest
import pytest_subprocess
from hv_control.command import Command

class TestCommand:
    def test_command_without_argument(self, fake_process):
        outputStatus = Command('outputStatus', argument_type=None)

        command_string = 'snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public 0.0.0.0 outputStatus.u0'
        fake_process.register_subprocess(command_string.split())
        outputStatus(IPv4Address('0.0.0.0'), 'u0')

        assert outputStatus(IPv4Address('0.0.0.0'), 'u0', dry_run=True) == command_string

        with pytest.raises(ValueError):
            outputStatus(IPv4Address('0.0.0.0'), 'u0', argument=0)

    def test_command_with_integer_argument(self, fake_process):
        outputSwitch = Command('outputSwitch', argument_type=(int, ), argument_is_valid=lambda argument : argument in (0, 1, 10))

        get_command_string = 'snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public 0.0.0.0 outputSwitch.u0'
        fake_process.register_subprocess(get_command_string.split())
        outputSwitch(IPv4Address('0.0.0.0'), 'u0')

        set_command_string = 'snmpset -v 2c -m +WIENER-CRATE-MIB -c public 0.0.0.0 outputSwitch.u0 i 0'
        fake_process.register_subprocess(set_command_string.split())
        outputSwitch(IPv4Address('0.0.0.0'), 'u0', argument=0)

        assert outputSwitch(IPv4Address('0.0.0.0'), 'u0', argument=0, dry_run=True) == set_command_string

        with pytest.raises(ValueError):
            outputSwitch(IPv4Address('0.0.0.0'), 'u0', argument=2)
        with pytest.raises(ValueError):
            outputSwitch(IPv4Address('0.0.0.0'), 'u0', argument=1.)

    def test_command_with_float_argument(self, fake_process):
        outputVoltage = Command('outputVoltage', argument_type=(int, float), argument_is_valid=lambda argument : argument >= 0. and argument <= 1000.)

        get_command_string = 'snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public 0.0.0.0 outputVoltage.u0'
        fake_process.register_subprocess(get_command_string.split())
        outputVoltage(IPv4Address('0.0.0.0'), 'u0')

        set_command_string = 'snmpset -v 2c -m +WIENER-CRATE-MIB -c public 0.0.0.0 outputVoltage.u0 F 0.0'
        fake_process.register_subprocess(set_command_string.split())
        outputVoltage(IPv4Address('0.0.0.0'), 'u0', argument=0.)

        assert outputVoltage(IPv4Address('0.0.0.0'), 'u0', argument=0.0, dry_run=True) == set_command_string

        set_command_string = 'snmpset -v 2c -m +WIENER-CRATE-MIB -c public 0.0.0.0 outputVoltage.u0 F 0'
        fake_process.register_subprocess(set_command_string.split())
        outputVoltage(IPv4Address('0.0.0.0'), 'u0', argument=0)
        
        assert outputVoltage(IPv4Address('0.0.0.0'), 'u0', argument=0, dry_run=True) == set_command_string

        with pytest.raises(ValueError):
            outputVoltage(IPv4Address('0.0.0.0'), 'u0', argument=1500.)
        with pytest.raises(ValueError):
            outputVoltage(IPv4Address('0.0.0.0'), 'u0', argument='a')

    def test_command_with_unknown_argument(self):
        unknownCommand = Command('unknownCommand', (bool, ))

        with pytest.raises(ValueError):
            unknownCommand(IPv4Address('0.0.0.0'), 'u0', argument=True)