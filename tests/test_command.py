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

import pytest
import pytest_subprocess
from hv_control.command import Command

class TestCommand:
    def test_command_with_argument(self, fake_process):
        name = 'outputSwitch'
        outputSwitch = Command(name, argument_type=int)

        ip_address = '0.0.0.0'
        oid_suffix = 'u0'

        get_cmd_str = outputSwitch.command_string(None)
        get_opt_and_arg_str = outputSwitch.option_and_argument_string(ip_address, oid_suffix)

        assert outputSwitch(ip_address, oid_suffix, dry_run=True) == 'snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public {} {}.{}'.format(ip_address, name, oid_suffix)

        fake_process.register_subprocess(
            '{} {}'.format(get_cmd_str, get_opt_and_arg_str).split()
        )

        outputSwitch(ip_address, oid_suffix)

        set_cmd_str = outputSwitch.command_string(1)
        set_opt_and_arg_str = outputSwitch.option_and_argument_string(ip_address, oid_suffix, argument=1)

        assert outputSwitch(ip_address, oid_suffix, argument=1, dry_run=True) == 'snmpset -v 2c -m +WIENER-CRATE-MIB -c public {} {}.{} i 1'.format(ip_address, name, oid_suffix)

        fake_process.register_subprocess(
            '{} {}'.format(set_cmd_str, set_opt_and_arg_str).split()
        )

        outputSwitch(ip_address, oid_suffix, argument=1)

        with pytest.raises(ValueError):
            outputSwitch(ip_address, oid_suffix, argument=1.)

        outputVoltage = Command('outputVoltage', float)
        outputVoltage(ip_address, oid_suffix, argument=1., dry_run=True)

        boolCommand = Command('boolCommand', bool)
        with pytest.raises(ValueError):
            boolCommand(ip_address, oid_suffix, argument=True)

    def test_command_without_argument(self):
        outputStatus = Command('outputStatus', argument_type=None)

        with pytest.raises(ValueError):
            outputStatus('0.0.0.0', 'u0', argument=0)