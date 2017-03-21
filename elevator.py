# coding: utf-8
from scp import SCPClient, SCPException
import argparse

import traceback
import paramiko
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))


######################
# Setup              #
######################
parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbose", action="store_true", default=False, help="increase output verbosity")
parser.add_argument("-t", "--template", default=os.path.join(current_dir, "sm.json"), help="template filename to use")
parser.add_argument("-f", "--update-firmware", default=False, help="firmware file image to use for elevation")
parser.add_argument("-u", "--username", default="ubnt", help="ssh username")
parser.add_argument("-p", "--password", default="ubnt", help="ssh password")
parser.add_argument("ip_address", help="IP address")

options = parser.parse_args()

LOGGING = options.verbose


######################
# Options validation #
######################
if not os.path.isfile(os.path.join(current_dir, options.template)):
    parser.error("File '%s' not found" % options.template)

if options.update_firmware:
    if not os.path.isfile(os.path.join(current_dir, options.update_firmware)):
        parser.error("Firmware '%s' not found" % options.update_firmware)


######################
# Connect to device  #
######################
host = options.ip_address
username = options.username
password = options.password
port = 22

if LOGGING:
    print("Connecting to device...")
    print("Host: %s" % host)
    print("Username: %s" % username)
    print("Password: %s" % password)
    print("Port: %s" % port)


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(
        hostname=host, username=username,
        password=password, port=port
    )
except paramiko.ssh_exception.AuthenticationException as error:
    tb = traceback.format_exc()
    print(error)
    sys.exit()


######################
# Main  #
######################
# Copy "sm.json" to "/etc/persistent/.configured_3.3" on the device
scp = SCPClient(client.get_transport())
conf_name = ".configured_3.2"

try:
    scp.put(options.template, "/etc/persistent/mnt/config/%s" % conf_name)
    if LOGGING:
        print("config file copied")
    stdin, stdout, stderr = client.exec_command("/usr/bin/cfgmtd -w")

    if LOGGING:
        for line in stderr:
            print line,
        print("config file saved to flash")

    if options.update_firmware:
        scp.put(options.update_firmware, "/tmp/fwupdate.bin")
        if LOGGING:
            print("Firmware copied")
        stdin, stdout, stderr = client.exec_command("/sbin/fwupdate -m")
        if LOGGING:
            print("Firmware update started")
except (SCPException,paramiko.SSHException)  as error:
    tb = traceback.format_exc()
    print(error)
    sys.exit()

client.close()

print("Elevation complete")
