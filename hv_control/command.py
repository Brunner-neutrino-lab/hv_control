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

import subprocess

class Command:
    def __init__(self, name, argument_type=None):
        self.name = name
        self.argument_type = argument_type

    def __call__(self, ip_address, oid_suffix, community='public', argument=None, dry_run=False):
        
        com_str = self.command_string(argument)
        opt_and_arg_str = self.option_and_argument_string(
            ip_address, oid_suffix, community=community, argument=argument
        )

        if dry_run:
            return '{} {}'.format(com_str, opt_and_arg_str)
        else:
            subprocess.run([com_str, opt_and_arg_str])

    def argument_type_string(self):
        if self.argument_type == int:
            return 'i'
        elif self.argument_type == float:
            return 'f'
        else:
            raise ValueError('No string representation for argument \
of type {} defined'.format(self.argument_type))

    def command_string(self, argument):
        if argument is not None:
            return 'snmpset'
        return 'snmpget'

    def special_options(self, argument):
        if argument is not None:
            return ''
        return '-Oqv'

    def option_and_argument_string(self, ip_address, oid_suffix, community='public', argument=None):
        return '{}{}{}'.format(
            self.option_string(ip_address, oid_suffix, community=community, argument=argument),
            '' if argument is None else ' ',
            self.argument_string(argument)
        )

    def option_string(self, ip_address, oid_suffix, community, argument=None):
        return '{}{}{} -c {} {} {}.{}'.format(
            self.special_options(argument),
            '' if self.special_options(argument) == '' else ' ', 
            '-v 2c -M +WIENER-CRATE-MIB',
            community, ip_address, self.name, 
            oid_suffix
        )

    def argument_string(self, argument):
        if argument is not None:
            if self.argument_type is None:
                raise ValueError('Command does not take arguments')
            if not isinstance(argument, self.argument_type):
                raise ValueError('Argument must be of type \'\''.format(str(self.argument_type)))
            return '{} {}'.format(self.argument_type_string(), str(argument))
        return ''