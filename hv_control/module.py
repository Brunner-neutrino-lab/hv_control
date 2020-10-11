# This file is part of Foobar.

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

class Module:
    def __init__(self, name, n_channels, 
                 max_voltage, polarity, max_current):
        self.name = name
        self.n_channels = n_channels
        self.max_voltage = max_voltage
        self.polarity = polarity
        self.max_current = max_current

        self.ip_address = '0.0.0.0'
        self.slot = 0
        self.channels = {}

    def add_channel(self, channel, address):
        self.check_address_in_range(channel, address)
        oid_suffix = 'u{:d}{:02d}'.format(self.slot, address)
        self.check_oid_suffix_free(channel, oid_suffix)
        channel.ip_address = self.ip_address
        channel.oid_suffix = oid_suffix
        self.channels[channel.oid_suffix] = channel

    def check_channel(self, channel, oid_suffix):

        self.check_address_free(channel, oid_suffix)

    def check_address_in_range(self, channel, address):
        if address < 0 or address > self.n_channels-1:
            raise ValueError('Invalid address ({:d}) given. \
The module only has addresses between 0 and {:d}.'.format(
                address, self.n_channels-1))

    def check_oid_suffix_free(self, channel, oid_suffix):
        for c in self.channels:
            if self.channels[c].oid_suffix == oid_suffix:
                raise ValueError('Invalid OID suffix ({:d}) given. \
Channel {:d} is already occupied by \'{}\'.'.format(
                    oid_suffix, oid_suffix, self.channels[c].name)) 

class EHS_F5_30n(Module):
    def __init__(self, name):
        Module.__init__(self, name, n_channels=16, polarity=-1, 
                        max_voltage=3e3, max_current=1e-3)

class EHS_8260p(Module):
    def __init__(self, name):
        Module.__init__(self, name, n_channels=8, polarity=1, 
                        max_voltage=6e3, max_current=1e-3)