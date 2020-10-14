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

from hv_control.dictionary_container import DictionaryContainer
from hv_control.channel import Channel

class Module(DictionaryContainer):
    def __init__(self, name, n_channels, polarity, 
                 abs_voltage_limit, abs_current_limit):
        assert n_channels in range(100)
        self.n_channels = n_channels
        DictionaryContainer.__init__(self, name, Channel, 
        key_is_valid=lambda key : key in range(0, self.n_channels))

        self.abs_voltage_limit = abs_voltage_limit
        self.polarity = polarity
        self.abs_current_limit = abs_current_limit

    def add_channel(self, channel_number, channel):
        self.add_value(channel_number, channel)
        if self[channel_number].max_abs_voltage is None:
            self[channel_number].max_abs_voltage = self.abs_voltage_limit
        if self[channel_number].max_abs_current_ramp is None:
            self[channel_number].max_abs_current_ramp = self.abs_current_limit
        if self[channel_number].max_abs_current_standby is None:
            self[channel_number].max_abs_current_standby = self.abs_current_limit

class EHS_8260p(Module):
    def __init__(self, name):
        Module.__init__(self, name, n_channels=8, polarity=1, 
                        abs_voltage_limit=6e3, abs_current_limit=1e-3)

class EHS_F5_30n(Module):
    def __init__(self, name):
        Module.__init__(self, name, n_channels=16, polarity=-1, 
                        abs_voltage_limit=3e3, abs_current_limit=1e-3)
