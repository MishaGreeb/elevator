#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scp import SCPClient, SCPException
import argparse

import traceback
import paramiko
import sys
import os
import _cffi_backend
import socket
import time

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    import sys
    current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

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

def fwinfo(txt):
    txt = txt.decode('utf8').replace('.', '')
    typefirmware = txt[:2]
    verfirmware = int(txt[3:6])
    if verfirmware > 604:
        firmware_signed = True
    else:
        firmware_signed = False
    return typefirmware, firmware_signed

def extract_files(file):
    from subprocess import call,check_output
    from platform import system
    os = system()
    if os == 'Linux':
        line = check_output(["./fwsplit", file])
    elif os == 'Windows':
        line = check_output(['fwsplit.exe',file], shell = True)
    lines = line.splitlines()
    for line in lines:
        if ".kernel" in line:
            firmware_kernel = line.strip("\t\n ")
        if ".rootfs" in line:
            firmware_rootfs = line.strip("\t\n ")
    return firmware_kernel, firmware_rootfs

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
except (paramiko.ssh_exception.AuthenticationException,socket.error) as error:
    tb = traceback.format_exc()
    print (error)
    sys.exit()

######################
# Main  #
######################
# Copy "sm.json" to "/etc/persistent/.configured_3.3" on the device
scp = SCPClient(client.get_transport())
conf_name = ".configured_%s" % options.firmware_version

try:
    stdin, stdout, stderr = client.exec_command('cat /etc/version')
    data = stdout.read() + stderr.read()
    fwtype, fwsign = fwinfo(data)
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
        if fwsign:
            kernel,rootfs = extract_files(options.update_firmware)
            print("Firmware copy to %s" %host)
            scp.put("mtd", "/tmp/mtd")
            scp.put(kernel, "/tmp/kernel")
            scp.put(rootfs, "/tmp/rootfs")
            #set attribute
            stdin, stdout, stderr = client.exec_command('chmod +x /tmp/mtd;chmod +x /tmp/kernel;chmod +x /tmp/rootfs;')
            print("Firmware update started")
            time.sleep(2)
            stdin, stdout, stderr = client.exec_command('/tmp/mtd write /tmp/kernel kernel && /tmp/mtd -r write /tmp/rootfs rootfs')
            for line in stderr:
                print(line)
                if line.count("Rebooting") > 0:
                    print("Firmware %s\t of %s successfully completed" % (options.update_firmware, host))
                    break
        else:
            scp.put(options.update_firmware, "/tmp/fwupdate.bin")
            print("Firmware update started")
            stdin, stdout, stderr = client.exec_command("/usr/bin/fwupdate -m /tmp/fwupdate.bin")
            if LOGGING:
                print("Elevation of %s successfully completed" % host)
except (SCPException, paramiko.SSHException) as error:
    tb = traceback.format_exc()
    print(error)
    sys.exit()

client.close()

print("Elevation of %s successfully completed" % host)
