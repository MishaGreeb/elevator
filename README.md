# Elevator #

### What is elevator? ###

* Easy tool to elevate UBNT units

More info can be found using the following link http://www.cambiumnetworks.com/products/access/epmp-elevate/

# Version 0.1
./elevator.py [--verbose] [--template=sm.json] [--username=ubnt] [--password=ubnt] <ip-address>

* If no options specified default values should be used(eg "sm.json","ubnt","ubnt" and etc)
* Tool copies "sm.json" to "/etc/persistent/.configured_3.3" on the device
* execute "save" command
* Tool should print verbose inoformation, if "verbose" key is specified

# Version 0.2
./elevator.py [--verbose] [--template=<sm.json>] [--update-firmware[=<fimrware.bin>]] [--username=ubnt] [--password=ubnt]  <ip-address>

* If "--firmware" key is specified, then do the following:
** copy firmware.bin to "/tmp/fwupdate.bin" on the device
** execute "/sbin/fwupdate -m" command

# Version 0.4

* Extract version from firmware.bin

# Version 0.3
./elevator.py [--verbose] [--template=<sm.json>] [--update-firmware[=<fimrware.bin>]] [--username=ubnt] [--password=ubnt] <ip-address or network>

* If network is specified, then elevator will go try to elevate all units one by one
