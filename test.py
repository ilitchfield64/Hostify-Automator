from sys import exit
from sys import argv
from os import system, name
import platform
import subprocess
import paramiko


filename = open('ip_log.csv','w')


def list_to_str(list1):
    string1 = str(list1[0]) + "." + str(list1[1]) + "." + str(list1[2]) + "." + str(list1[3])
    return string1

## Pings the remote host to determine if the AP is up
def pinger(host):

    # return True # this is for debugging REMOVE ME
    parameter = '-n' if platform.system().lower()=='windows' else '-c'

    command = ['ping', parameter, '1', host]
    response = subprocess.call(command)

    if response == 0:
        print("Ping!")
        filename.write(host)
        filename.write(',')
        return True
        
    else:
        print("Failed to Ping")
        return False


pinger('10.64.113.100')
pinger('10.64.113.101')
pinger('10.64.113.102')
pinger('10.64.113.103')
filename.close()

