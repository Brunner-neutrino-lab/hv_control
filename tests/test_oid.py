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

import pytest

from hv_control.oid import OIDAndSuffix, Suffix

class TestOID:
    def test_suffix(self):
        # __init__ with module and channel number as pair of int
        suffix = Suffix((1, 2))
        assert suffix.module_number == 1
        assert suffix.channel_number == 2
        assert str(suffix) == 'u102'

        with pytest.raises(ValueError):
            Suffix((10, 2))
        with pytest.raises(ValueError):
            Suffix((1, 200))

        # __init__ with module and channel number in the 'u...' string format
        suffix = Suffix('u304')
        assert suffix.module_number == 3
        assert suffix.channel_number == 4
        assert str(suffix) == 'u304'

        suffix = Suffix('u34')
        assert suffix.module_number == 0
        assert suffix.channel_number == 34
        assert str(suffix) == 'u34'

        suffix = Suffix('u3')
        assert suffix.module_number == 0
        assert suffix.channel_number == 3
        assert str(suffix) == 'u3'

        suffix = Suffix('u0')
        assert suffix.module_number == 0
        assert suffix.channel_number == 0
        assert str(suffix) == 'u0'

        with pytest.raises(ValueError):
            Suffix('u03')
        with pytest.raises(TypeError):
            Suffix(0)
        with pytest.raises(ValueError):
            Suffix('')
        with pytest.raises(ValueError):
            Suffix('u')
        with pytest.raises(ValueError):
            Suffix('a100')
        with pytest.raises(ValueError):
            Suffix('u1000')
        with pytest.raises(ValueError):
            Suffix('u10a')

    def test_oid_and_suffix(self):
        # __init__ with oid and suffix as pair of string and Suffix object
        oid_and_suffix = OIDAndSuffix(('oid', Suffix(module_and_channel=(1, 2))))
        assert oid_and_suffix.oid == 'oid'
        assert oid_and_suffix.suffix == Suffix(module_and_channel=(1, 2))
        assert str(oid_and_suffix) == 'oid.u102'

        with pytest.raises(ValueError):
            OIDAndSuffix((0, Suffix((0,0))))
        with pytest.raises(ValueError):
            OIDAndSuffix(('', Suffix((0,0))))

        # __init__ with oid and suffix as pair of two strings
        oid_and_suffix = OIDAndSuffix(('oid', 'u0'))
        assert oid_and_suffix.oid == 'oid'
        assert oid_and_suffix.suffix == Suffix((0,0))
        assert str(oid_and_suffix) == 'oid.u0'

        # __init__ with oid and suffix in the 'OID.SUFFIX' format
        oid_and_suffix = OIDAndSuffix('oid.u0')
        assert oid_and_suffix.oid == 'oid'
        assert oid_and_suffix.suffix == Suffix((0,0))
        assert str(oid_and_suffix) == 'oid.u0'

        with pytest.raises(ValueError):
            OIDAndSuffix('.u0')
        with pytest.raises(ValueError):
            OIDAndSuffix('oid.')
        with pytest.raises(ValueError):
            OIDAndSuffix('.')