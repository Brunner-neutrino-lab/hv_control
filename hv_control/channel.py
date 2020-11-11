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

        self.add_value('outputCurrent', Command('outputCurrent', argument_type=(float, ), argument_is_valid=lambda argument : argument >= 0. and argument <= self.max_abs_current_ramp))
        self.add_value('outputMeasurementSenseVoltage', Command('outputMeasurementSenseVoltage', argument_type=None))
        self.add_value('outputStatus', Command('outputStatus', argument_type=None)),
        self.add_value('outputSwitch', Command('outputSwitch', argument_type=(int, ), argument_is_valid=lambda argument : argument in (0, 1, 10)))
        self.add_value('outputVoltageRiseRate', Command('outputVoltageRiseRate', argument_type=(int, float), argument_is_valid=lambda argument : argument >= min(0., self.polarity*self.max_abs_rise_rate) and argument <= max(0., self.polarity*self.max_abs_rise_rate)))
        self.add_value('outputVoltage', Command('outputVoltage', argument_type=(int, float), argument_is_valid=lambda argument : argument >= min(0., self.polarity*self.max_abs_voltage) and argument <= max(0., self.polarity*self.max_abs_voltage)))
