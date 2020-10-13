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

from hv_control.crate import Crate, Mpod_Mini
from hv_control.module import EHS_8260p

def test_crate():
    crate = Mpod_Mini('crate', IPv4Address('0.0.0.0'))
    crate = Mpod_Mini('crate', '0.0.0.0')
    with pytest.raises(ValueError):
        crate = Mpod_Mini('crate', 1)

    crate.add_module(0, EHS_8260p('module'))
    with pytest.raises(ValueError):
        crate.add_module(crate.n_slots, EHS_8260p('module'))
    with pytest.raises(ValueError):
        crate.add_module(0, EHS_8260p('module'))
    with pytest.raises(AssertionError):
        crate.add_module(1, 0)

    with pytest.raises(AssertionError):
        crate = Crate('crate', 10, IPv4Address('0.0.0.0'))
