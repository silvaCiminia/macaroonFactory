#!/usr/bin/env python

import os
import subprocess
import time

# Consolidate input methods
try:
    input = raw_input
except:
    pass

working = True

def logoPrint():
    print("""
 \33[92m,     .
\33[92m( ( \33[91mo \33[92m) )
 \33[92m`  \33[0m:  \33[92m'
  \33[0m.~`~.  ### \33[91mMACAROON FACTORY \33[0m###
  \___/  Mac changer and interface manager
    """)

def changeMac(interface, mode='none'):
    if mode == 'none':
        print("")
        print("\033[91m### \033[92m INTERFACE {} \033[91m###\033[0m".format(interface['name']))
        print("\033[91m[\033[92m0\033[91m]\033[0m: Change MAC address")
        print("\033[91m[\033[92m1\033[91m]\033[0m: Flip monitor mode on/off")
        print("\033[91m[\033[92m2\033[91m]\033[0m: Both")
        print("\033[92m################")
        sel = input("\033[91m[*] \033[0mSelection: ")
        if sel == '0':
            mode = 'mac'
        elif sel == '1':
            mode = 'mon'
        elif sel == '2':
            mode = 'all'
        else:
            print("\033[91m[*] \033[0mInvalid selection!")
            return()
    os.system("ip link set {} down".format(interface['name']))
    if mode in ['mon', 'all']:
        try:
            print("")
            if interface['mon'] != 'Wired':
                if interface['mon'] == 'Managed':
                    os.system('iwconfig {} mode monitor'.format(interface['name']))
                    print("\033[91m[*] \033[0mPut station interface \033[92m{}\033[0m in monitor mode.".format(interface['name']))
                    interface['mon'] = 'Monitor'
                elif interface['mon'] == 'Monitor':
                    os.system('iwconfig {} mode managed'.format(interface['name']))
                    print("\033[91m[*] \033[0mPut monitor interface \033[92m{}\033[0m in station mode.".format(interface['name']))
                    interface['mon'] = 'Managed'
                print("")
            else:
                print("\033[91m[*] \033[0mCannot put a wired interface into monitor mode!")
        except:
            print("\033[91m[*] \033[0mInterface cannot be put into monitor mode.")
    if mode in ['mac', 'all']:
        try:
            os.system("ip link set {} down".format(interface['name']))
            print("\n\033[91m##### \033[0mINTERFACE \033[92m{} \033[91m#####\033[0m\n".format(interface['name']))
            os.system('macchanger -A {} 2>/dev/null'.format(interface['name']))
            time.sleep(0.25)
            os.system("ip link set {} up".format(interface['name']))
            print("")
        except:
            print("\033[91m[*] \033[0mInvalid interface!")

def intGet():
    global working
    interfaces = []
    a = str(subprocess.check_output('ip link show', shell=True))
    ints = a.split(': ')
    for i in range(len(ints)):
        if len(ints[i].split()) == 1:
            if ints[i] not in ["1", "lo", "b'1"]:
                interface = {'name':str(ints[i])}
                interfaces.append(interface)
    # Get interface properties
    for interface in interfaces:
        name = interface['name']
        macs = str(subprocess.check_output('macchanger -s {}'.format(name), shell=True))
        interface['cMac'] = macs.split()[2]
        interface['cVend'] = macs.split("(")[1].split(")")[0]
        interface['pMac'] = macs.split("\n")[1].split()[2]
        interface['pVend'] = macs.split("\n")[1].split("(")[1].split(")")[0]
        try:
            mon = str(subprocess.check_output('iwconfig {} 2> /dev/null'.format(name), shell=True)).split()
            mon1 = mon[3].split(':')[1]
            if mon1 == 'off/any':
                mon1 = mon[4].split(':')[1]
            interface['mon'] = mon1
        except:
            interface['mon'] = 'Wired'
    intRef = {}
    i = 0
    for item in interfaces:
        print("\033[91m[\033[92m{}\033[91m]\033[0m: {} \033[92m::: \033[0m{} \033[92m// \033[0m{} \033[92m// \033[0m{} ".format(i, item['name'], item['pVend'], item['cVend'], item['mon']))
        intRef[i] = item
        i += 1
    print("\033[91m[\033[92m{}\033[91m]\033[0m: All interfaces".format(i))
    print("\033[91m[\033[92m{}\033[91m]\033[91m: EXIT".format('q'))
    print("\033[92m################")
    no = input("\033[91m[*] \033[0mSelection: ")
    allInt = False
    # Quit
    if no == 'q':
        working = False
        return
    # Single interface
    elif no != str(i):
        try:
            interface = intRef[int(no)]
        except:
            print("\033[91m[*] \033[0mInvalid interface!")
            quit()
    # All interfaces
    else:
        print("\033[91m[\033[92m0\033[91m]\033[0m: Change MAC addresses")
        print("\033[91m[\033[92m1\033[91m]\033[0m: Handle each interface individually")
        print("\033[92m################")
        sel = input("\033[91m[*] \033[0mSelection: ")
        mode = 'none'
        if sel == '0':
            mode = 'mac'
        for interface in interfaces:
            changeMac(interface, mode)
            allInt = True
    if not allInt:
        changeMac(interface)
macchanger, ip, iwconfig = '', '', ''
if os.getuid() != 0:
    print("Must be run as root!")
else:
    macchanger = subprocess.check_output("which macchanger", shell=True)
    ip = subprocess.check_output("which ip", shell=True)
    iwconfig = subprocess.check_output("which iwconfig", shell=True)
    if macchanger == '':
        print("MACCHANGER not installed! Please install and try again.")
        quit()
    if ip == '':
        print("IP not installed! Please install and try again.")
        quit()
    if iwconfig == '':
        print("IWCONFIG not installed! Please install and try again.")
        quit()

    logoPrint()
    while working:
        intGet()
    print("\033[91m[*] \033[31mHappy Trails, Stranger.")
    print("")
