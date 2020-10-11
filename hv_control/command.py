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

class GetCommand:
    def __init__(self, name, snmp_command='snmpget',
                 special_options='-Oqv'):
        self.name = name
        self.general_options = '-v 2c -M +WIENER-CRATE-MIB'
        self.prefix = '{}{}{} {}'.format(
            snmp_command, '' if special_options == '' else ' ', 
            special_options, self.general_options)

    def __call__(self, ip_address, oid_suffix, 
                 community='public'):
        print(self.command_string_without_argument(
            ip_address, oid_suffix, community))

    def command_string_without_argument(
        self, ip_address, oid_suffix, community='public'):
        return '{} -c {} {} {}.{}'.format(
            self.prefix, community, ip_address, self.name, 
            oid_suffix
        )

class SetCommand(GetCommand):
    def __init__(self, name, argument_type):
        GetCommand.__init__(self, name, snmp_command='snmpset',
                            special_options='')
        self.argument_type = argument_type
        if self.argument_type == int:
            self.argument_type_string = 'i'
        elif self.argument_type == float:
            self.argument_type_string = 'f'
        else:
            raise ValueError('No string representation for argument \
of type {} defined'.format(self.argument_type))

    def __call__(self, ip_address, oid_suffix, argument, 
                 community='public'):
        print(self.command_string_with_argument(ip_address, oid_suffix, argument, 
                          community))

    def argument_type_string(self):
        if self.argument_type == int:
            return 'i'
        elif self.argument_type == float:
            return 'f'
        else:
            raise ValueError('No string representation for argument \
of type {} defined'.format(self.argument_type))

    def command_string_with_argument(
        self, ip_address, oid_suffix, argument, community='public'):
        return '{} {} {}'.format(
            self.command_string_without_argument(
                ip_address, oid_suffix, community),
            argument_type_string(self.argument_type),
            str(argument)
        )

class GetSetCommand(SetCommand):
    def __init__(self, name, argument_type):
        SetCommand.__init__(self, name, argument_type)
        self.get_command=GetCommand(name)
        self.set_command=SetCommand(name, argument_type)
        
    def __call__(self, ip_address, oid_suffix,
                 community='public', argument=None):
        if argument is None:
            self.get_command(ip_address, oid_suffix, community)
        else:
            self.set_command(ip_address, oid_suffix,
                             argument, community)