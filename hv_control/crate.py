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

from hv_control.module import Module

class Crate:
    def __init__(self, name, ip_address, n_slots):
        self.ip_address = ip_address
        self.n_slots = n_slots

        self.modules = {}

    def add_module(self, module, slot):
        assert isinstance(module, Module)
        self.check_slot(module, slot)
        module.ip_address = self.ip_address
        module.slot = slot
        self.modules[str(slot)] = module
        
    def check_slot(self, module, slot):
        self.check_slot_in_range(module, slot)
        self.check_slot_free(module, slot)
        
    def check_slot_in_range(self, module, slot):
        if slot < 0 or slot > self.n_slots - 1:
            raise ValueError('Invalid slot ({:d}) given. \
The crate only has slots between 0 and {:d}.'.format(
                slot, self.n_slots-1))
    def check_slot_free(self, module, slot):
        for m in self.modules:
            if self.modules[m].slot == slot:
                raise ValueError('Invalid slot ({:d}) given. \
Slot {:d} is already occupied by \'{}\'.'.format(
                    slot, slot, self.modules[m].name))        

class Mpod_Mini(Crate):
    def __init__(self, name, ip_address):
        Crate.__init__(self, name, ip_address, 4)