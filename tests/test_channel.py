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
from hv_control.channel import Channel

def test_channel():
    channel = Channel('channel', max_voltage=1000., max_current=0.1)
    
    assert channel('outputSwitch', 1, dry_run=True) == 'snmpset -v 2c -m +WIENER-CRATE-MIB -c public 0.0.0.0 outputSwitch.u0 i 1'

    with pytest.raises(ValueError):
        channel('outputVoltage', 2000.)
    with pytest.raises(ValueError):
        channel('outputCurrent', 0.2)
    with pytest.raises(ValueError):
        channel('outputSwitch', 20)