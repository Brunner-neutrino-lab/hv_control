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

from hv_control.channel import Channel
from hv_control.crate import Mpod_Mini
from hv_control.module import EHS_8260p, EHS_F5_30n

mpod = Mpod_Mini('utr-mpod-0', IPv4Address('192.168.0.237'))

mpod.add_module(1, EHS_8260p('germanium_hv'))
mpod[1].add_channel(0, Channel('clover_USNA'))
mpod[1].add_channel(1, Channel('clover_Yale'))

mpod.add_module(3, EHS_F5_30n('cebr_hv'))
mpod[3].add_channel(0, Channel('cebr_0'))
mpod[3].add_channel(1, Channel('cebr_1'))