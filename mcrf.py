#!/usr/bin/env python

import os
import subprocess
import time
import interfaces

# Consolidate input methods

try:
    input = raw_input
except:
    pass

# Global vars
working = True
macchanger, ip, iwconfig = '', '', ''

def logoPrint():
    """Prints the logo"""
    print("""
 \33[92m,     .
\33[92m( ( \33[91mo \33[92m) )
 \33[92m`  \33[0m:  \33[92m'
  \33[0m.~`~.  ### \33[91mMACAROON FACTORY \33[0m###
  \___/  Mac changer and interface manager
    """)

def changeMac(interface, mode='none'):
    """Changes an interface's (or multiple interfaces') MAC address"""
    global ip, iwconfig, macchanger
    if mode == 'none':
        print("")
        print("\033[91m### \033[92m INTERFACE {} \033[91m###\033[0m".format(interface['name']))
        print("\033[91m[\033[92m0\033[91m]\033[0m: Change MAC address")
        print("\033[91m[\033[92m1\033[91m]\033[0m: Flip monitor mode on/off")
        print("\033[91m[\033[92m2\033[91m]\033[0m: Both")
        print("\033[91m[\033[92mq\033[91m]\033[0m: Back")
        print("\033[92m################")
        sel = input("\033[91m[*] \033[0mSelection: ")
        if sel == '0':
            mode = 'mac'
        elif sel == '1':
            mode = 'mon'
        elif sel == '2':
            mode = 'all'
        elif sel == 'q':
            return
        else:
            print("\033[91m[*] \033[0mInvalid selection!")
            return()
    os.system("{} link set {} down".format(ip, interface['name']))
    if mode in ['mon', 'all']:
        try:
            if interface['mon'] != 'Wired':
                if interface['mon'] == 'Managed':
                    os.system('{} {} mode monitor'.format(iwconfig, interface['name']))
                    print("\n\033[91m[*] \033[0mPut station interface \033[92m{}\033[0m in monitor mode.".format(interface['name']))
                    interface['mon'] = 'Monitor'
                elif interface['mon'] == 'Monitor':
                    os.system('{} {} mode managed'.format(iwconfig, interface['name']))
                    print("\n\033[91m[*] \033[0mPut monitor interface \033[92m{}\033[0m in station mode.".format(interface['name']))
                    interface['mon'] = 'Managed'
            else:
                print("\n\033[91m[*] \033[0mCannot put a wired interface into monitor mode!")
        except:
            print("\n\033[91m[*] \033[0mInterface cannot be put into monitor mode.")
    if mode in ['mac', 'all']:
        try:
            os.system("{} link set {} down".format(ip, interface['name']))
            print("\n\033[91m##### \033[0mINTERFACE \033[92m{} \033[91m#####\033[0m".format(interface['name']))
            os.system('{} -A {} 2>/dev/null'.format(macchanger, interface['name']))
            time.sleep(0.25)
            os.system("{} link set {} up".format(ip, interface['name']))
        except:
            print("\n\033[91m[*] \033[0mInvalid interface!")
def intQuery(interfaces):
    """Gets user interface selection from a list of interfaces"""
    global working, macchanger, ip, iwconfig
    intRef = {}
    i = 0
    print("")
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
        print("\033[91m[\033[92m2\033[91m]\033[0m: Back")
        print("\033[92m################")
        sel = input("\033[91m[*] \033[0mSelection: ")
        mode = 'none'
        if sel == '0':
            mode = 'mac'
        elif sel == 'q':
            return
        for interface in interfaces:
            changeMac(interface, mode)
            allInt = True
    if not allInt:
        changeMac(interface)
def checkPaths():
    """Fills program path variables"""
    global macchanger, ip, iwconfig
    ret = interfaces.pathGet()
    if ret == '1':
        print("MACCHANGER not installed! Please install and try again.")
        quit()
    if ret == '2':
        print("IP not installed! Please install and try again.")
        quit()
    if ret == '3':
        print("IWCONFIG not installed! Please install and try again.")
        quit()
    else:
        macchanger = ret[0]
        ip = ret[1]
        iwconfig = ret[2]
def menu():
    """Displays the user interface"""
    if os.getuid() != 0:
        print("Must be run as root!")
    else:
        global working
        checkPaths()
        logoPrint()
        while working:
            intQuery(interfaces.intGet())
        print("\033[91m[*] \033[31mHappy Trails, Stranger.")
        print("\033[0m")
if __name__ == '__main__':
    menu()
