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
parser.add_argument("-c", "--cambium-id", default=os.path.join(current_dir, "cambium_id"), help="template filename to use")
parser.add_argument("-n", "--firmware-version", default="3.3", help="firmware version(3.3 is the default)")
parser.add_argument("-f", "--update-firmware", default=False, help="firmware file image to use for elevation")
parser.add_argument("-u", "--username", default="ubnt", help="ssh username")
parser.add_argument("-p", "--password", default="ubnt", help="ssh password")
parser.add_argument("-P", "--port", default="22", help="ssh port")
parser.add_argument("ip_address", help="IP address")

options = parser.parse_args()

LOGGING = options.verbose


######################
# Options validation #
######################
if not os.path.isfile(os.path.join(current_dir, options.template)):
    parser.error("File '%s' not found" % options.template)

if not os.path.isfile(os.path.join(current_dir, options.cambium_id)):
    parser.error("File '%s' not found" % options.cambium_id)

if options.update_firmware:
    if not os.path.isfile(os.path.join(current_dir, options.update_firmware)):
        parser.error("Firmware '%s' not found" % options.update_firmware)


######################
# Connect to device  #
######################
host = options.ip_address
username = options.username
password = options.password
port = int(options.port)

if LOGGING:
    print("Connecting to device %s " % host)
    print("Username: %s" % username)
    print("Password: %s" % password)

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
conf_name = ".configured_%s" % options.firmware_version

try:
    stdin, stdout, stderr = client.exec_command("mkdir -p /etc/persistent/mnt/config/")

    scp.put(options.template, "/etc/persistent/mnt/config/%s" % conf_name)
    if LOGGING:
        print("configiguration file copied")

    if options.cambium_id:
        scp.put(options.cambium_id, "/etc/persistent/mnt/config/cambium_id")
        if LOGGING:
            print("configiguration file copied")

    scp.put(os.path.join(current_dir, "passwd"), "/etc/persistent/mnt/config/passwd")
    if LOGGING:
        print("passwd file copied")

    stdin, stdout, stderr = client.exec_command("cfgmtd -w -f /tmp/running.cfg -p /etc/")

    if LOGGING:
        for line in stderr:
            print(line)
        print("configuration files saved to flash")

    if options.update_firmware:
        scp.put(options.update_firmware, "/tmp/fwupdate.bin")
        if LOGGING:
            print("Firmware copied")
        stdin, stdout, stderr = client.exec_command("/usr/bin/fwupdate -m /tmp/fwupdate.bin")
        if LOGGING:
            print("Firmware update started")
except (SCPException,paramiko.SSHException)  as error:
    tb = traceback.format_exc()
    print(error)
    sys.exit()

client.close()

print("Elevation of %s successfully completed" % host)
