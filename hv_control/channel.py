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

from hv_control.command import Command

class Channel:
    def __init__(self, name, max_voltage=None, max_current=None):
        self.name = name
        self.max_voltage = max_voltage
        self.max_current = max_current

        self.ip_address = '0.0.0.0'
        self.oid_suffix = 'u0'

        self.commands = {
            'outputCurrent':
            Command('outputCurrent', (float, ), lambda argument : argument >= 0. and argument <= max_current),
            'outputMeasurementSenseVoltage':
            Command('outputMeasurementSenseVoltage', None),
            'outputStatus':
            Command('outputStatus', None),
            'outputSwitch':
            Command('outputSwitch', (int, ), lambda argument : argument in (0, 1, 10)),
            'outputVoltageRiseRate':
            Command('outputVoltageRiseRate', (int, float)),
            'outputVoltage':
            Command('outputVoltage', (int, float), lambda argument : argument >= 0. and argument <= max_voltage),
        }

    def __call__(self, command_name, argument=None, community='public', dry_run=False):
        return self.commands[command_name](self.ip_address, self.oid_suffix, argument=argument, community=community, dry_run=dry_run)
