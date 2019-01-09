#! /usr/bin/python3.6
import sys
import socket
import time
from multiprocessing import Pool
import curses
from datetime import datetime, timedelta
import subprocess
import re

##################################################################
# If you are reading this than what are you doing with your life #
# Made with coffee by Ben0 over several night shifts             #
# Relays UDP data to a specified list of IP addresses            #
# Developed for linux only, must be run from a terminal          #
# This is the headless service version                           #
##################################################################

# Global Variables
# Blank IP List
dest_ip_list = []
# IP address and port to listen for UDP packets
source_ip = '10.20.23.230'
source_port = 5019
# Local IP address and port to bind to
binding_ip = '10.20.64.253'
dest_port = 5019
# File with the list of IP addresses
ip_list = '/home/minesys/Desktop/final.conf'

# Statistics
transmit_ok = 0
transmit_errors = 0
transmit_perc = 0
receive_ok = 0
receive_errors = 0
receive_perc = 0
send_ok = 0
send_errors = 0
send_perc = 0

# Start timing
_uptime = ''
timestamp = time.time()
delay = 0
prev_delay = 0

# Placeholder variable for netstat output
netstat = ''


def ipList():
    '''
    Parse ip_list file and append to dest_ip_list array
    Ignore lines starting with #
    '''
    with open(ip_list, 'r') as f:
        for line in f.readlines():
            if line[0] == '#':
                continue
            else:
                stripped_line = line.strip('\n')
                split_line = stripped_line.split(':')
                dest_ip = split_line[1].split('/')[0]
                dest_ip_list.append(dest_ip)


def send(ip, data, s):
    '''
    Send {data} to {ip} using {s} (socket)
    This is threaded
    '''
    try:
        s.settimeout(0.01)
        s.sendto(data, (ip, dest_port))
        return(ip, True)
    except:
        return(ip, False)
    s.shutdown(s.SHUT_RDWR)
    s.close()

def uptime(seconds):
    '''
    Calculates uptime in weeks, days, hours, minutes, seconds
    '''
    intervals = (
    ('w', 604800),  # 60 * 60 * 24 * 7
    ('d', 86400),    # 60 * 60 * 24
    ('h', 3600),    # 60 * 60
    ('m', 60),
    ('s', 1),
    )

    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{}{}".format(int(value), name))
    return(', '.join(result[:4]))

def getBuffer():
    '''
    Returns the system udp tx buffer
    '''
    out = subprocess.Popen(['netstat', '-a'], stdout=subprocess.PIPE)
    stdout,stderr = out.communicate()
    decoded = stdout.decode("utf-8").split('\n')
    for line in decoded:
        if 'localhost.localdom:5019' in line:
            splitline = line.split()
            port_active = True
            return(splitline)
        else:
            port_active = False
    if not port_active:
        return(['udp', 0, 0])


    # self.box7.addstr(1,1,'  Rx: {} kb'.format(round(int(netstat[1])/1000)))
    # self.box7.addstr(2,1,'  Tx: {} kb'.format(round(int(netstat[2])/1000)))




if __name__ == '__main__':

    # Generate an ip list
    ipList()

    # Count the length of the list
    how_many = len(ip_list)

    # Create threads
    p = Pool(processes=how_many)

    # Open socket once (i.e not for each thread)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set socket buffer options
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8388608)
    # Bind to ip and port
    s.bind((binding_ip, source_port))


    # Bröther may I have some lööps?
    while True:
        # Receive UDP on socket
        try:
            s.settimeout(1.1)
            data, addr = s.recvfrom(32768)
            receive_ok += 1
        except:
            receive_errors += 1
            addr = None


        try:
            if addr[0] == source_ip:
                prev_delay = time.time()
                transmit_ok += 1
                # Send data to each ip in separate threads
                results = [p.apply_async(send, args=(ip, data, s,)) for ip in dest_ip_list]
                # Convert results of threads to an array
                output = [p.get() for p in results]
                # Count success and errors
                for i in output:
                    if i[1] == True:
                        send_ok += 1
                    else:
                        send_errors += 1

        except:
            transmit_errors += 1

        # Calculate uptime
        uptime_seconds = time.time()-timestamp
        _uptime = uptime(uptime_seconds)

        # Calculate percentages, handle dividing by 0
        try:
            receive_total = receive_ok + receive_errors
            receive_perc = round((receive_ok/receive_total)*100, 2)
        except:
            receive_perc = 100
        try:
            transmit_total = transmit_ok + transmit_errors
            transmit_perc = round((transmit_ok/transmit_total)*100, 2)
        except:
            transmit_perc = 100
        try:
            send_total = send_ok + send_errors
            send_perc = round((send_ok/send_total)*100, 2)
        except:
            send_perc = 100
        
        # Get kernal udp tx and rx buffer usage
        netstat = getBuffer()
        # Calculate processing delay time
        delay = time.time()-prev_delay
