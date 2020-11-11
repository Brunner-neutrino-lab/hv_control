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

# This test shows how an existing crate configuration can be imported, and how parameters for each channel can be set.

import pytest
# pytest_subprocess is imported to be able to test the code without actually executing the SNMP
# commands.
# Instead of executing the commands on the command line, python_subprocess catches all subprocess 
# commands and compares them to user-defined fake processes.
# If subprocess issues a command that has not been defined as a fake process, the test will fail.
# This way, it can be checked whether the code generates the correct command-line instructions.
import pytest_subprocess

# Import the crate configuration from 'tests/test_config.py'.
from .test_config import mpod
# A new module with a new channel will be added to the imported configuration below for 
# illustration purposes, therefore the following two import statements are needed.
from hv_control.channel import Channel
from hv_control.module import EHS_8260p
from hv_control.oid import OIDAndSuffix, Suffix

def test_control(fake_process):
    # Test a command which takes no arguments ('outputStatus')
    # First, create a fake process which contains the correct command-line instructions.
    # This is what should be return by the call of outputStatus
    fake_process.register_subprocess(
        'snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public {} outputStatus.u100'.format(mpod.ip).split()
    )

    # Get the 'outputStatus' of channel 'u100'.
    # This is done by calling the crate with the OID 'outputStatus' and the corresponding suffix.
    mpod('outputStatus.u100')
    # The following commands show alternative ways of passing a combination of OID and suffix \
    # to the crate by using an `OIDAndSuffix` object.
    # The `OIDAndSuffix` object is used internally by `hv_control` to enforce a correct format of the OID and the suffix.
    fake_process.register_subprocess(
        'snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public {} outputStatus.u100'.format(mpod.ip).split()
    )
    mpod(OIDAndSuffix('outputStatus.u100'))
    fake_process.register_subprocess(
        'snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public {} outputStatus.u100'.format(mpod.ip).split()
    )
    mpod(OIDAndSuffix(('outputStatus', 'u100')))
    fake_process.register_subprocess(
        'snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public {} outputStatus.u100'.format(mpod.ip).split()
    )
    mpod(OIDAndSuffix(('outputStatus', Suffix((1, 0)))))
    fake_process.register_subprocess(
        'snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public {} outputStatus.u100'.format(mpod.ip).split()
    )
    mpod(OIDAndSuffix(('outputStatus', Suffix('u100'))))

    # It is not possible to get the 'outputStatus' of channels that are not defined.
    with pytest.raises(KeyError):
        mpod('outputStatus.u102')
    
    # In addition, all the instructions below raise errors, because they give the OID and/or the
    # suffix in a wrong format.

    # Error: Argument must be a string.
    with pytest.raises(TypeError):
        mpod(0)
    # Error: Argument must contain a '.'
    with pytest.raises(ValueError):
        mpod('a')
    # Error: Suffix must contain at least two symbols.
    with pytest.raises(ValueError):
        mpod('outputSwitch.u')
    # Error: Suffix must start with 'u' or 'U'
    with pytest.raises(ValueError):
        mpod('outputSwitch.a100')
    # Error: Suffix may contain at most 4 symbols.
    with pytest.raises(ValueError):
        mpod('outputSwitch.u1000')
    # Error: Suffix must start with 'u' or 'U' and contain only numbers otherswise.
    with pytest.raises(ValueError):
        mpod('outputSwitch.u10a')

    # Add a new module in slot 0 and create its channel 0.
    # This module-channel combination has the lowest possible OID suffix 'u0'.
    mpod.add_module(0, EHS_8260p('germanium_hv_2'))
    mpod[0].add_channel(0, Channel('clover_Yale_2'))
    # Create the fake process for 'u0'
    fake_process.register_subprocess(
        'snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public {} outputStatus.u0'.format(mpod.ip).split()
    )
    # Get the 'outputStatus' of channel 'u100'.
    mpod('outputStatus.u0')
    
    # Test a command which takes an integer argument ('outputSwitch').
    # 'outputSwitch' can take integers from 0 to 10, which have different meanings.
    # The following two lines show what a command with an integer argument looks like and how it 
    # the parameter is set in hv_control. 
    fake_process.register_subprocess(
        'snmpset -v 2c -m +WIENER-CRATE-MIB -c public {} outputSwitch.u100 i 0'.format(mpod.ip).split()
    )
    mpod('outputSwitch.u100', argument=0)

    # In a real application, it would turn out that the syntax of the command is correct, but the
    # community 'public', which is chosen by default by the crate, does not have the permission
    # to switch the channel off (i.e. set 'outputSwitch' to 0).
    # The following two lines show how to set the community to 'guru'.
    fake_process.register_subprocess(
        'snmpset -v 2c -m +WIENER-CRATE-MIB -c guru {} outputSwitch.u100 i 0'.format(mpod.ip).split()
    )
    mpod('outputSwitch.u100', argument=0, community='guru')
    # (In reality, a responsible administrator will have renamed the 'guru' community to prevent
    # unauthorized access, so this command may not work as well.)

    # Test a command which takes a float argument.
    # As can be seen below, that does not mean that the actual number that is entered must have
    # a decimal point.

    fake_process.register_subprocess(
        'snmpset -v 2c -m +WIENER-CRATE-MIB -c public {} outputVoltage.u100 F 0.0'.format(mpod.ip).split()
    )
    mpod('outputVoltage.u100', argument=0.)

    # Commands that take arguments allow the user to set limits on their values.
    # For the 'outputVoltage' and 'outputCurrent' parameters, the constructor of the 'Channel' 
    # class provides the additional arguments 
    #
    # max_abs_voltage
    # max_abs_current_ramp
    # max_abs_current_standby
    #
    # to set an upper limit for the allowed absolute value of the voltage and the current.
    # For the current, an additional distinction is made between the allowed current during
    # the ramp-up/down process and on standby.
    # To prevent a user from entering the wrong sign for an expression, the 
    # Command.argument_is_valid() method should be implemented accordingly.
    #
    # When the parameter 'outputCurrent' is set, the limit for the ramp-up/down process will be 
    # applied.
    # If these parameters are not set explicitly when a 'Channel' object is constructed, adding
    # it to a module via the 'Module.add_channel()' method will set the limits to the factory 
    # limits of that module.
    # As the examples below show, it is not possible to execute commands the would require output 
    # beyond the limits.
    # The current limits can be accessed as member variables of the 'Module' and 'Channel' classes, i.e.
    assert mpod['u100'].max_abs_current_ramp == 1e-6
    # The following two commands show an alternative way of passing a channel address to the \
    # crate by using a `Suffix` object.
    # The `Suffix` object is used internally by `hv_control` to enforce a correct format of the suffix.
    assert mpod[Suffix((1,0))].max_abs_current_ramp == 1e-6
    assert mpod[Suffix(('u100'))].max_abs_current_ramp == 1e-6

    assert mpod['u100'].max_abs_current_standby == 1e-8
    assert mpod['u300'].max_abs_voltage == 890.
    assert mpod['u100'].max_abs_rise_rate == 5.
    assert mpod[1].abs_voltage_limit == 6e3
    assert mpod[3].abs_voltage_limit == 3e3

    # Error: Maximum voltage of channel 'u101' is only 3000 V, and the maximum rise rate is 5 V/s.
    with pytest.raises(ValueError):
        mpod('outputVoltage.u101', argument=3500)
    with pytest.raises(ValueError):
        mpod('outputVoltage.u101', argument=2*mpod['u101'].max_abs_voltage)
    with pytest.raises(ValueError):
        mpod('outputVoltageRiseRate.u101', argument=1.1*mpod['u101'].max_abs_rise_rate)
    # The example above also works for channels that have a negative rise rate.
    with pytest.raises(ValueError):
        mpod('outputVoltageRiseRate.u301', argument=1.1*mpod['u301'].max_abs_rise_rate)
    # Error: There is actually also a lower limit for the voltage (0 V).
    # Please note that, by design of the modules, it is actually impossible to apply a voltage 
    # with an adverse polarity to a detector.
    with pytest.raises(ValueError):
        mpod('outputVoltage.u101', argument=-1500)
    # Error: No limit for the current on channel 'u300' was set explicitly, so the factory limit 
    # of the module applies.
    # This example also shows how the limits can be accessed.
    with pytest.raises(ValueError):
        mpod('outputCurrent.u300', argument=2*mpod[3].abs_current_limit)