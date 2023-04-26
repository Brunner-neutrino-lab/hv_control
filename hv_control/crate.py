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

from hv_control.dictionary_container import DictionaryContainer
from hv_control.module import Module
from hv_control.oid import OIDAndSuffix, Suffix

class Crate(DictionaryContainer):
    def __init__(self, name, n_slots, ip):
        assert n_slots in range(1,11)
        self.n_slots = n_slots
        DictionaryContainer.__init__(self, name, Module, key_is_valid=lambda key : key in range(0, self.n_slots))
        self.ip = self.parse_ip(ip)

    def add_module(self, module_number, module):
        self.add_value(module_number, module)

    def __call__(self, oid_and_suffix,argument=None, community='guru', dry_run=False):
        if not isinstance(oid_and_suffix, OIDAndSuffix):
            oid_and_suffix = OIDAndSuffix(oid_and_suffix)
        
        return self[oid_and_suffix.suffix.module_number][oid_and_suffix.suffix.channel_number][oid_and_suffix.oid](self.ip, str(oid_and_suffix.suffix), community=community, argument=argument, dry_run=dry_run)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.dictionary[key]
        else:
            suffix = Suffix(key)
            return self.dictionary[suffix.module_number][suffix.channel_number]

    def parse_ip(self, ip):
        if isinstance(ip, IPv4Address):
            return ip
        elif isinstance(ip, str):
            return IPv4Address(ip)
        else:
            raise ValueError('IP address format not recognized. It is recommended to pass an \
IPv4Address object from the Python Standard Library to Crate.__init__().')

class Mpod_Mini(Crate):
    def __init__(self, name, ip):
        Crate.__init__(self, name, 4, ip)