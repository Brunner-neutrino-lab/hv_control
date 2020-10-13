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

from hv_control.module import Module

class Crate:
    def __init__(self, name, ip, n_slots):
        self.ip = self.parse_ip(ip)
        self.n_slots = n_slots

        self.modules = {}

    def add_module(self, module, module_number):
        assert isinstance(module, Module)
        self.check_module_number(module_number)
        self.modules[module_number] = module

    def check_module_number(self, module_number):
        self.check_module_number_in_range(module_number)
        self.check_module_number_free(module_number)

    def check_module_number_in_range(self, module_number):
        if module_number not in range(0, self.n_slots):
            raise ValueError('Invalid module number. The crate has {:d} slots, i.e. module numbers may range from {:d} to {:d}.'.format(self.n_slots, 0, self.n_slots-1))

    def check_module_number_free(self, module_number):
        if module_number in self.modules:
            raise ValueError('Module number {:d} is already occupied.'.format(module_number))

    def parse_ip(self, ip):
        if isinstance(ip, IPv4Address):
            return ip
        elif isinstance(ip, str):
            return IPv4Address(ip)
        else:
            raise ValueError('IP address format not recognized. It is recommended to pass an IPv4Address object from the Python Standard Library to Crate.__init__().')

class Mpod_Mini(Crate):
    def __init__(self, name, ip_address):
        Crate.__init__(self, name, ip_address, 4)