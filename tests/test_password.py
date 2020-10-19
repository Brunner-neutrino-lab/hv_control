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

# This test shows how to use the getpass module of python to query the community name from a user 
# without ever displaying it one the command line.
# See also test_control.py for more comment on the usage of hv_control.

from getpass import getpass
import pytest
import pytest_subprocess
from unittest.mock import patch

from .test_config import mpod

# @patch('builtins.input')
@patch('getpass.getpass')
def test_password(getpass):
    getpass.return_value = 'guru'

    assert mpod('outputSwitch.u100', argument=1, community=getpass.return_value, dry_run=True) == 'snmpset -v 2c -m +WIENER-CRATE-MIB -c {} {} outputSwitch.u100 i 1'.format(getpass.return_value, mpod.ip)