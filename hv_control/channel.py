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

from hv_control.dictionary_container import DictionaryContainer
from hv_control.command import Command

class Channel(DictionaryContainer):
    def __init__(self, name, polarity=None, max_abs_voltage=None, max_abs_current_ramp=None, max_abs_current_standby=None, max_abs_rise_rate=None):
        DictionaryContainer.__init__(self, name, Command)

        self.polarity = polarity
        self.max_abs_voltage = max_abs_voltage
        self.max_abs_current_ramp = max_abs_current_ramp
        self.max_abs_current_standby = max_abs_current_standby
        self.max_abs_rise_rate = max_abs_rise_rate

        self.add_value('outputCurrent', Command('outputCurrent', (float, ), lambda argument : argument >= 0. and argument <= self.max_abs_current_ramp))
        self.add_value('outputMeasurementSenseVoltage', Command('outputMeasurementSenseVoltage', None))
        self.add_value('outputStatus', Command('outputStatus', None)),
        self.add_value('outputSwitch', Command('outputSwitch', (int, ), lambda argument : argument in (0, 1, 10)))
        self.add_value('outputVoltageRiseRate', Command('outputVoltageRiseRate', (int, float), lambda argument : abs(argument) <= abs(self.max_abs_rise_rate)))
        self.add_value('outputVoltage', Command('outputVoltage', (int, float), lambda argument : argument >= 0. and argument <= self.max_abs_voltage))
