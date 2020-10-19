# hv_control

Object-oriented python library to make the remote control of a MPOD Power Supply System simple and safe.

## Contents

 * [Description](#description)
 * [Implementation](#implementation)
 * [Installation](#installation)
   
   * [Prerequisites](#prerequisites)
   * [Procedure](#procedure)
   * [Testing](#testing)
 * [Usage](#usage)
 * [License](#license)
 * [References](#references)

## Description

MPOD crates for the control of high-voltage (HV) power supply modules, manufactured by the company WIENER [1,2], can be mounted on a network via DHCP and remote controlled using the Simple Network Management Protocol (SNMP, see, e.g., Ref. [3]).
Parameters of single channels of a module can be retrieved ('get') and 'set' using command-line instructions like [2]:

```
snmpget OPTIONS -v 2c -M MIB_PATH -m +WIENER-CRATE-MIB -c COMMUNITY_GROUP IP_ADDRESS OID.SUFFIX
snmpset OPTIONS -v 2c -M MIB_PATH -m +WIENER-CRATE-MIB -c COMMUNITY_GROUP IP_ADDRESS OID.SUFFIX FORMAT VALUE
```

In the two examples above, `-v 2c` specifies the SNMP version.
This command is not listed with the other optional `OPTIONS` because the manual implies that only this version can be used.
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
For example, a real crate contains several modules, so a virtual crate should be a container class for module objects.
The repetitiveness and verbosity was reduced through the use of multiple dispatch: A single object represents both the respective 'get'- and 'set' command, and it returns the desired command depending on the number of arguments (no argument means: this parameter should be read).

## Implementation

Several python classes have been implemented that reflect the hierarchy and modularity of the actual setup.
From top to bottom in the hierarchy, the following base classes exist:

 * `Crate`
 * `Module`
 * `Channel`
 * `Command`

Any class `A`, which is on top of a class `B`, is also a container class for objects of type `B`.
For example, a crate may contain a set of modules.
While the base classes put no constraints on their properties, derived classes exist that represent actual models.
For example, the `Crate` class has the property `n_slots` which indicates how many modules fit into the crate.
In the `Mpod_Mini` class, which is derived from `Crate`, `n_slots` is set to 4 in its overriden `__init__()` method, because a WIENER Mpod Mini has exactly 4 slots.

Objects of type `B` are stored within `A` as a python dictionary.
This allows one to address the stored objects by an arbitrary identifier instead of an integer index.
This way, it is possible to be in accordance with the 'u*' nomenclature in the SNMP commands for the module channels.
New objects should be added using the respective `add_*` methods of the container class, because they perform some checks before actually creating a new dictionary entry.
For example, the `Crate.add_module()` method prevents the user from inserting two modules into the same slot.

At the moment, there are no derived classes from the base classes `Channel` and `Command`, and the available commands for each channel are initialized automatically.
They are stored in a dictionary as well, where the key is the OID of the respective SNMP command.
Each channel has almost all the commands listed as 'commonly needed' in the WIENER manual [2].
Commands for a channel are intended to be executed by calling (`__call__(SUFFIX, argument=VALUE)`) the crate that contains it with the corresponding suffix and, potentially, an argument.
For an example of how to create a setup and channels, see the [Usage](#usage) section.

Every command has a required argument type, which is determined on initialization.
Pure get commands have the argument type `None`.
The 'community' argument defines the SNMP community, as described above.
It should be avoided to write down the community names anywhere in scripts, because they serve as a password protection for the HV control.
Making 'community' an argument of every single command call supports this philosophy by discouraging a global setting of the community.
For example, the community could have been implemented as a property of the `Crate` class, which might allow anyone with the correct config file (see below) to run commands with high privileges.
The script `tests/test_password.py` shows how to use python's built-in `getpass` module to query a password from the user without having to display it anywhere.
By default, a command is transmitted to the command line using the `subprocess` module of python.
In order to test the commands, one could execute them as a member of the 'public' community, which will not allow any potentially harmful 'set' commands.
Since this procedure prints error messages on the command line as well, `Channel.__call__()` also provides a 'dry_run' flag.
If activated, the command will not be executed, but its string will be returned.

## Installation

### Prerequisites

 * [python3](https://www.python.org/)

The following packages are required to run self-tests:

 * [pytest](https://docs.pytest.org/)
 * [pytest-cov](https://pytest-cov.readthedocs.io/)
 * [pytest-subprocess](https://pytest-subprocess.readthedocs.io)
 * [tox](https://tox.readthedocs.io/)

### Procedure

In order to make the `hv_control` libraries available on your system, execute 

```
python setup.py install
``` 

in the directory where the `setup.py` file is located.

### Testing

A self-test of `hv_control` can be run by executing

```
tox
```

in the same directory.

## Usage

For HV systems, it can be assumed that the parameters of the channels are modified more often than the actual physical configuration is changed.
Therefore, it is recommended to create one file that contains the setup (called 'config.py' here).
This configuration can be imported by scripts that set the parameters.
Below, you can find a minimal example that constructs a crate that contains a single module, which in turn has a single active channel:

```
# Content of 'config.py'

from ipaddress import IPv4Address

from hv_control.channel import Channel
from hv_control.crate import Mpod_Mini
from hv_control.module import EHS_8260p

mpod = Mpod_Mini('utr-mpod-0', IPv4Address('192.168.0.237')) # (a)
mpod.add_module(1, EHS_8260p('germanium_hv'))                # (b)
mpod[1].add_channel(0, Channel('clover_USNA',                # (c)
    max_abs_voltage=3500., max_abs_current_ramp=1e-6, max_abs_current_standby=1e-8)
)
```

In (a), the crate is created.
It has an arbitrary name and an IP address.
Using the `add_module` method, a module with an arbitrary name is inserted in the crate at slot 0 (b).
In (c), channel 0 of the module is made available, and voltage and current limits are set.

The example script below first sets the output voltage of a channel and the voltage rise rate. 
After that, it switches the channel on, thereby starting the ramp-up process.
During the ramp-up process, the sense voltage is printed every 5 seconds.

```
# Content of 'u100_ramp_up.py'

from time import sleep

from config import crate

# Set output voltage to 3500 V
mpod('outputVoltage.u100', 3500)
# Set rise rate to 10 V/s
mpod('outputVoltageRiseRate.u100', 10)
# Switch channel on
mpod('outputSwitch.u100', 1)

while True:
    mpod('outputMeasurementSenseVoltage.u100')
    sleep(5)
```

Note that the ramp-up process starts as soon as the 'outputSwitch' is turned on, and that it cannot be stopped by stopping the execution of the script.
The preferred way to interrupt an ongoing ramp-up process is to execute another SNMP command that sets the 'outputSwitch' parameter to 0 or modifies the 'outputVoltage'.
This behavior is intentional, since it largely decouples the HV crate from the server that controls it.

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
