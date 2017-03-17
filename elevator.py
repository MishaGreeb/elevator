# coding: utf-8
from scp import SCPClient, SCPException
from optparse import OptionParser
import traceback
import paramiko
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))


######################
# Setup              #
######################
parser = OptionParser()

parser.add_option("-v", "--verbose", default=False, help="prints logs")
parser.add_option("-t", "--template", default=os.path.join(current_dir, "sm.json"), help="template")
parser.add_option("-f", "--update-firmware", default=False, help="update firmware")
parser.add_option("-u", "--username", default="ubnt", help="username")
parser.add_option("-p", "--password", default="ubnt", help="password")
parser.add_option("-a", "--ip-address", help="[REQUIRED] ip-address")

(options, args) = parser.parse_args()

LOGGING = options.verbose


######################
# Options validation #
######################
if LOGGING:
    print("Validating parameters...")

if not options.ip_address:
    parser.error("IP address not given")

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
    print(tb)
    print(error)
    sys.exit()


######################
# Main  #
######################
# Copy "sm.json" to "/etc/persistent/.configured_3.3" on the device
scp = SCPClient(client.get_transport())
conf_name = ".configured_3.3"
if options.update_firmware:
    filename, file_extension = os.path.splitext(options.update_firmware)
    filename = filename.rsplit("-", 1)
    if len(filename) > 1:
        firmware_version = filename[-1]
        conf_name = ".configured_%s" % firmware_version

try:
    scp.put(options.template, "/etc/persistent/%s" % conf_name)
    if options.update_firmware:
        scp.put(options.update_firmware, "/tmp/fwupdate.bin")
except SCPException as error:
    tb = traceback.format_exc()
    print(tb)
    sys.exit()

if LOGGING:
    print("Start firmware updating...")

try:
    stdin, stdout, stderr = client.exec_command("/sbin/fwupdate -m")
except paramiko.SSHException as error:
    tb = traceback.format_exc()
    print(tb)
    print(error)
    sys.exit()

client.close()

print("Done")
