#!/usr/bin/python
#How to run: sudo python2.7 cleanup.py
#The scripts clears the host sshd connections and cleans the mininet environment

import os
import sys

def cleanup():
    os.system('sudo mn -c')
    os.system('ps aux | grep "/usr/sbin/sshd -D -o UseDNS=no -u0" > tmp')
    for line in open('tmp'):
        if line.startswith('root'):
            pid = line.split()[1]
            os.system('sudo kill -9 ' + pid)
    os.system('rm tmp')
    print('*** Terminated sshd on hosts.')

if __name__ == '__main__':
    cleanup()
