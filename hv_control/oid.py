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

class OIDAndSuffix:
    def __init__(self, oid_and_suffix):
        if isinstance(oid_and_suffix, str):
            self.oid, self.suffix = self.parse_oid_and_suffix_string(oid_and_suffix)
        else:
            if not isinstance(oid_and_suffix[0], str):
                raise ValueError('OID must be a string.')
            if len(oid_and_suffix[0]) == 0:
                raise ValueError('OID must be a string with at least one character.')
            self.oid = oid_and_suffix[0]
            self.suffix = Suffix(oid_and_suffix[1])

    def __str__(self):
        return '{}.{}'.format(self.oid, self.suffix)

    def parse_oid_and_suffix_string(self, oid_and_suffix_string):
        if not isinstance(oid_and_suffix_string, str) or '.' not in oid_and_suffix_string[1:-2]:
            raise ValueError('Expected string with the format \'OID.SUFFIX\', where OID has at \
least one, and SUFFIX at least two characters.')

        dot_index = oid_and_suffix_string.find('.')
        return (
            oid_and_suffix_string[:dot_index],
            Suffix(oid_and_suffix_string[dot_index+1:])
        )

class Suffix:
    def __init__(self, module_and_channel):
        if isinstance(module_and_channel, str):
            self.__init__(self.parse_suffix_string(module_and_channel))
        elif isinstance(module_and_channel, Suffix):
            self.module_number = module_and_channel.module_number
            self.channel_number = module_and_channel.channel_number
        else:
            if module_and_channel[0] not in range(10):
                raise ValueError('Module number must be an integer number between 0 and 9')
            self.module_number = module_and_channel[0]
            if module_and_channel[1] not in range(100):
                raise ValueError('Channel number must be an integer number between 0 and 99')
            self.channel_number = module_and_channel[1]

    def parse_suffix_string(self, suffix_string):
        if not len(suffix_string) in range(2,5):
            raise ValueError('Suffix must consist of 2 to 4 symbols.')
        if suffix_string[0] not in ('u', 'U'):
            raise ValueError('Suffix must start with \'u\' or \'U\'.')
        if suffix_string[1] == '0' and suffix_string != 'u0':
            raise ValueError('The only suffix where \'u\' is followed by \'0\' is \'u0\'.')
        if len(suffix_string) < 4:
            return (0, int(suffix_string[1:]))
        
        return (int(suffix_string[1]), int(suffix_string[2:]))

    def __eq__(self, other):
        return self.module_number == other.module_number and self.channel_number == other.channel_number

    def __str__(self):
        if self.module_number == 0:
            return 'u{:d}'.format(self.channel_number)
        return 'u{:d}{:02d}'.format(self.module_number, self.channel_number)