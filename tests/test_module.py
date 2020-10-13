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
from hv_control.module import EHS_8260p, EHS_F5_30n, Module

def test_module():
    module = EHS_F5_30n('module')
    module = EHS_8260p('module')

    module.add_channel(0, Channel('channel_0'))
    with pytest.raises(ValueError):
        module.add_channel(0, Channel('channel_1'))
    with pytest.raises(ValueError):
        module.add_channel(module.n_channels, Channel('channel_1'))

    with pytest.raises(AssertionError):
        module = Module('module', 100, 1, 0., 0.)