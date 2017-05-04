# Elevator #
# Easy command line tool to Elevate wireless equipment

More info about ePMP Elevate can be found using the following link http://www.cambiumnetworks.com/products/access/epmp-elevate/

# Installation for macOS or Linux
* git clone https://github.com/m0sia/elevator.git
* cd elevator
* pip install -r requirements.txt

# Windows version with simple GUI
* https://app.box.com/s/fc2qzgk2l0azejvg2q5m8u9enmo3roid

# Usage
```
usage: elevator.py [-h] [-v] [-t TEMPLATE] [-n FIRMWARE_VERSION]
                   [-f UPDATE_FIRMWARE] [-u USERNAME] [-p PASSWORD]
                   ip_address

positional arguments:
  ip_address            IP address

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -t TEMPLATE, --template TEMPLATE
                        template filename to use
  -n FIRMWARE_VERSION, --firmware-version FIRMWARE_VERSION
                        firmware version(3.3 is the default)
  -f UPDATE_FIRMWARE, --update-firmware UPDATE_FIRMWARE
                        firmware file image to use for elevation
  -u USERNAME, --username USERNAME
                        ssh username
  -p PASSWORD, --password PASSWORD
                        ssh password
```
# Example

* Modify sm.json the way you like
* Elevate with the following command
  * Without fimrware update
    - python elevator.py -u ubnt -p password -t sm.json -n 3.3 -v 192.168.1.39
  * With firwmare update:
    - python elevator.py -v -u ubnt -p password -t sm.json -n 3.3 -f UBNTXW-ubntxw-squashfs-factory-3.3.bin 192.168.1.20
