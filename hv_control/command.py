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
    def __init__(self, name, argument_type=None, 
    argument_is_valid=lambda argument : True):
        self.name = name
        self.argument_type = argument_type
        self.argument_is_valid = argument_is_valid

    def __call__(self, ip_address, oid_suffix, community='public', argument=None, dry_run=False):
        
        com_str = self.command_string(argument)
        opt_and_arg_str = self.option_and_argument_string(
            ip_address, oid_suffix, community=community, argument=argument
        )
        com_opt_arg_str = '{} {}'.format(com_str, opt_and_arg_str)	

        if dry_run:
            return com_opt_arg_str
        else:
            subprocess.run(com_opt_arg_str.split())

    def argument_type_string(self):
        if float in self.argument_type:
            return 'F'
        elif int in self.argument_type:
            return 'i'
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
            '-v 2c -m +WIENER-CRATE-MIB',
            community, ip_address, self.name, 
            oid_suffix
        )

    def argument_string(self, argument):
        if argument is not None:
            if not self.argument_is_valid(argument):
                raise ValueError('Invalid argument for command')
            if self.argument_type is None:
                raise ValueError('Command does not take arguments')
            if not isinstance(argument, self.argument_type):
                raise ValueError('Argument must be of type \'\''.format(str(self.argument_type)))
            return '{} {}'.format(self.argument_type_string(), str(argument))
        return ''
