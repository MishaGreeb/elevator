# Elevator #

### What is elevator? ###

# Easy command line tool to Elevate wireless equipment

More info can be found using the following link http://www.cambiumnetworks.com/products/access/epmp-elevate/

# Installation 
* git clone https://github.com/m0sia/elevator.git
* cd elevator
* pip install -r requirements.txt

# Usage
usage: elevator.py [-h] [-v] [-t TEMPLATE] [-f UPDATE_FIRMWARE] [-u USERNAME]
                   [-p PASSWORD]
                   ip_address

positional arguments:
  ip_address            IP address

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -t TEMPLATE, --template TEMPLATE
                        template filename to use
  -f UPDATE_FIRMWARE, --update-firmware UPDATE_FIRMWARE
                        firmware file image to use for elevation
  -u USERNAME, --username USERNAME
                        ssh username
  -p PASSWORD, --password PASSWORD
                        ssh password

# Example

* Modify sm.json the way you like
* Elevate:
python elevator.py -u ubnt -p password -t sm.json -v 192.168.1.39
