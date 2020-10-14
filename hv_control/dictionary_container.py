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

class DictionaryContainer:
    def __init__(self, name, value_type, key_is_valid=lambda key : True):
        self.name = name
        self.value_type = value_type
        self.key_is_valid = key_is_valid

        self.dictionary = {}

    def add_value(self, key, value):
        assert isinstance(value, self.value_type)
        self.check_key(key)
        self.dictionary[key] = value

    def check_key(self, key):
        if not self.key_is_valid(key):
            raise ValueError('Invalid key.')
        self.key_is_free(key)

    def __getitem__(self, key):
        return self.dictionary[key]

    def key_is_free(self, key):
        if key in self.dictionary:
            raise ValueError('Key is already in use.')