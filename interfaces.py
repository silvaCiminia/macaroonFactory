#!/usr/bin/env python

import subprocess

def pathGet():
    """Gets the path of macchanger, ip, and iwlink (required to gather interface info and change settings)"""
    macchanger = subprocess.check_output("which macchanger", shell=True)[:-1]
    ip = subprocess.check_output("which ip", shell=True)[:-1]
    iwconfig = subprocess.check_output("which iwconfig", shell=True)[:-1]
    if macchanger == '':
        return(1)
    if ip == '':
        return(2)
    if iwconfig == '':
        return(3)
    else:
        return( macchanger, ip, iwconfig)
def intGet():
    """ Returns a list of interfaces, including the name, current and permanent MAC addresses and vendors, and the interface mode""" 
    macchanger, ip, iwconfig = pathGet()
    interfaces = []
    a = str(subprocess.check_output("{} link show".format(ip), shell=True))
    ints = a.split(': ')
    for i in range(len(ints)):
        if len(ints[i].split()) == 1:
            if ints[i] not in ["1", "lo", "b'1"]:
                interface = {'name':str(ints[i])}
                interfaces.append(interface)
    # Get interface properties
    for interface in interfaces:
        name = interface['name']
        macs = str(subprocess.check_output("{} -s {}".format(macchanger, name), shell=True))
        interface['cMac'] = macs.split()[2]
        interface['cVend'] = macs.split("(")[1].split(")")[0]
        interface['pMac'] = macs.split("\n")[1].split()[2]
        interface['pVend'] = macs.split("\n")[1].split("(")[1].split(")")[0]
        try:
            mon = str(subprocess.check_output("{} {} 2> /dev/null".format(iwconfig, name), shell=True)).split()
            mon1 = mon[3].split(':')[1]
            if mon1 == 'off/any':
                mon1 = mon[4].split(':')[1]
            interface['mon'] = mon1
        except:
            interface['mon'] = 'Wired'
    return(interfaces)

