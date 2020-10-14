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

class Crate(DictionaryContainer):
    def __init__(self, name, n_slots, ip):
        assert n_slots in range(10)
        self.n_slots = n_slots
        DictionaryContainer.__init__(self, name, Module, key_is_valid=lambda key : key in range(0, self.n_slots))
        self.ip = self.parse_ip(ip)

    def add_module(self, module_number, module):
        self.add_value(module_number, module)

    def __call__(self, oid_with_suffix, community='public', argument=None, dry_run=False):
        oid, suffix = self.parse_oid_with_suffix(oid_with_suffix)
        module_number, channel_number = self.parse_suffix(suffix)

        self[module_number][channel_number][oid](self.ip, suffix, community=community, argument=argument, dry_run=dry_run)

    def parse_ip(self, ip):
        if isinstance(ip, IPv4Address):
            return ip
        elif isinstance(ip, str):
            return IPv4Address(ip)
        else:
            raise ValueError('IP address format not recognized. It is recommended to pass an \
IPv4Address object from the Python Standard Library to Crate.__init__().')

    def parse_oid_with_suffix(self, oid_with_suffix):
        if not isinstance(oid_with_suffix, str) or '.' not in oid_with_suffix:
            raise ValueError('Expected string with the format \'OID.SUFFIX\'.')
        return oid_with_suffix.split('.')

    def parse_suffix(self, suffix):
        if not len(suffix) in range(2,5):
            raise ValueError('Suffix must consist of 2 to 4 symbols.')
        if suffix[0] not in ('u', 'U'):
            raise ValueError('Suffix must start with \'u\' or \'U\'.')
        if len(suffix) < 4:
            return (0, int(suffix[1:]))
        
        return (int(suffix[1]), int(suffix[2:]))

class Mpod_Mini(Crate):
    def __init__(self, name, ip):
        Crate.__init__(self, name, 4, ip)