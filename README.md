# hv_control

Object-oriented python library to make the remote control of a MPOD Power Supply System simple and safe.

## Description

MPOD crates for the control of power supply modules, manufactured by the company WIENER [1,2], can be mounted on a network via DHCP and remote controlled using the Simple Network Management Protocol (SNMP, see, e.g., Ref. [3]).
Parameters of single channels of a module can be retrieved ('get') and 'set' using command-line instructions like [2]:

```
snmpget -v 2c -M MIB_PATH -m +WIENER-CRATE-MIB -c COMMUNITY_GROUP IP_ADDRESS OID.SUFFIX
snmpset -v 2c -M MIB_PATH -m +WIENER-CRATE-MIB -c COMMUNITY_GROUP IP_ADDRESS OID.SUFFIX FORMAT VALUE
```

In the two examples above, `-v 2c` specifies the SNMP version.
The variable `MIB_PATH` is the path to the management information base (MIB) file.
This MIB file '+WIENER-CRATE-MIB' contains a list of all available instructions of the crate.
In order to regulate access to parameters of the power supply system, different community groups ('public', 'private', 'admin', 'guru') exist with different permissions.
The parameter `COMMUNITY_GROUP` may not be identical to one of the aforementioned communities, because they can be renamed to create a password-like protection.
A specific crate is identified by its IP address (`IP_ADDRESS`), and a specific channel by a suffix (`SUFFIX`) of the general form 'uMCC'.
In the channel suffix, 'u' is a prefix, 'M' is the single-digit address of the module in the crate, and 'CC' is the two-digit channel number in the module (note that leading zeros are omitted in the channel suffix, i.e. the very first channel in module 0 would be called 'u0').
The parameter `OID` is an object identifier of the parameter that is read or modified.
In the case that a parameter is modified, the data type (`FORMAT`) and the new value (`VALUE`) are specified in the command as well.

It is obvious that the bare SNMP commands are very verbose and repetitive, so any frequent user will write some kind of script to simplify the remote control.
Due to the hierarchic and modular structure of the problem, it was chosen here to represent crates, modules, channels, and the actions that any of these entities may execute, as python classes.
For example, a crate contains several modules, so a virtual crate should be a container for module objects.
The repetitiveness and verbosity was reduced through the use of inheritance.
For example, a set command has many elements in common with a get command, but in addition it takes an argument as an input.
There is no need to repeat all the code that produces the command string, but it can simply be inherited from the get command.

## Installation

In order to make the hv_control libraries available on your system, execute 

```
python setup.py install
``` 

in the directory where the `setup.py` file is located.

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Copyright (C) 2020 Udo Friman-Gayer (ufg@email.unc.edu)

## References

[1] [http://www.wiener-d.com/sc/power-supplies/mpod--lvhv/](http://www.wiener-d.com/sc/power-supplies/mpod--lvhv/)
[2] WIENER Power Electronics GmbH, 'MPOD HV & LV Power Supply System Technical Manual  Version 3.2' (2020)[https://file.wiener-d.com/documentation/MPOD/](https://file.wiener-d.com/documentation/MPOD/)
[3] [http://www.net-snmp.org/](http://www.net-snmp.org/)