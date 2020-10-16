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

# This file shows an example for a crate configuration.
# It is imported in 'tests/test_control.py', which shows how to use it.
# The crate contains two different HV modules, each of which powers two detectors.

# Use the IPv4Address class to check whether the IP address is formally correct.
from ipaddress import IPv4Address

# Import all necessary constituents of the setup.
from hv_control.channel import Channel
from hv_control.crate import Mpod_Mini
from hv_control.module import EHS_8260p, EHS_F5_30n

# Create an Mpod Mini crate
mpod = Mpod_Mini('utr-mpod-0', IPv4Address('192.168.0.237'))

# Add a module for (germanium) semiconductor detectors to the crate in slot 1.
mpod.add_module(1, EHS_8260p('germanium_hv'))
# Create channels 0 and 1 of the module and set detector-specific parameters.
# These channels can be adressed by the OID suffixes 'u100' and 'u101'.
mpod[1].add_channel(0, Channel('clover_USNA', max_abs_voltage=3500., max_abs_current_ramp=1e-6, max_abs_current_standby=1e-8, max_abs_rise_rate=5.))
mpod[1].add_channel(1, Channel('clover_Yale', max_abs_voltage=3000., max_abs_current_ramp=1e-6, max_abs_current_standby=1e-8, max_abs_rise_rate=5.))

# Add a module for (CeBr) scintillation detectors to the crate in slot 3.
mpod.add_module(3, EHS_F5_30n('cebr_hv'))
# Create channels 0 and 1 of the module and set detector-specific parameters.
# These channels can be adressed by the OID suffixes 'u100' and 'u101'.
mpod[3].add_channel(0, Channel('cebr_0', max_abs_voltage=890., max_abs_rise_rate=10.))
mpod[3].add_channel(1, Channel('cebr_1', max_abs_voltage=890., max_abs_rise_rate=10.))