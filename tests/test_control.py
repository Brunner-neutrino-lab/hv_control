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

from .test_config import mpod
from hv_control.channel import Channel
from hv_control.module import EHS_8260p

def test_control(fake_process):
    fake_process.register_subprocess(
        'snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public {} outputStatus.u100'.format(mpod.ip).split()
    )

    mpod('outputStatus.u100')

    fake_process.register_subprocess(
        'snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public {} outputStatus.u0'.format(mpod.ip).split()
    )

    mpod.add_module(0, EHS_8260p('germanium_hv_2'))
    mpod[0].add_channel(0, Channel('clover_Yale_2'))
    mpod('outputStatus.u0')
    
    fake_process.register_subprocess(
        'snmpset -v 2c -m +WIENER-CRATE-MIB -c public {} outputSwitch.u100 i 0'.format(mpod.ip).split()
    )

    mpod('outputSwitch.u100', argument=0)

    with pytest.raises(ValueError):
        mpod(0)
    with pytest.raises(ValueError):
        mpod('a')
    with pytest.raises(ValueError):
        mpod('outputSwitch.u')
    with pytest.raises(ValueError):
        mpod('outputSwitch.a100')
    with pytest.raises(ValueError):
        mpod('outputSwitch.u1000')