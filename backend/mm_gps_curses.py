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
# About 5 lines to do the job, 265 to print crap to terminal     #
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


class display():
    '''
    Curses display for the current statistics
    '''

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_RED, -1)
        self.ascii_art = asciiArt()


    def screen(self):
        # Clear the screen
        self.stdscr.clear()

        # Create a boarder
        self.stdscr.border(0)

        # Title
        self.stdscr.addstr(0,32,"Minesystems' UDP Relay")

        # Position windows
        self.box1 = curses.newwin(3, 28, 1, 29) # Top middle (uptime)
        self.box2 = curses.newwin(5, 28, 4, 1) # Middle left (corrections in)
        self.box3 = curses.newwin(5, 28, 4, 29) # Middle middle (corrections out)
        self.box4 = curses.newwin(5, 28, 4, 57) # Middle right (corrections sent)
        self.box5 = curses.newwin(4, 28, 9, 1) # Bottom left (list)
        self.box6 = curses.newwin(4, 28, 9, 29) # Bottom middle (binding)
        self.box7 = curses.newwin(4, 28, 9, 57) # Bottom right (buffer)
        self.box8 = curses.newwin(3, 28, 1, 1) # Top Left (warning)
        self.box9 = curses.newwin(3, 28, 1, 57) # Top Right (delay)
        self.box10 = curses.newwin(20, 44, 13, 20) # Bottom (ascii art)

        # Create boarder box's
        self.box1.box()
        self.box2.box()
        self.box3.box()
        self.box4.box()
        self.box5.box()
        self.box6.box()
        self.box7.box()
        self.box8.box()
        self.box9.box()
        self.box10.box()

        # Titles of the windows
        self.box1.addstr(0,11,"Uptime")
        self.box2.addstr(0,6,"Corrections In")
        self.box3.addstr(0,6,"Corrections Out")
        self.box4.addstr(0,5,"Corrections Sent")
        self.box5.addstr(0,12,"List")
        self.box6.addstr(0,10,"Binding")
        self.box7.addstr(0,11,"Buffer")
        self.box8.addstr(0,10,"Warning")
        self.box9.addstr(0,12,"Delay")
        self.box10.addstr(0,17,"A Satellite")

        # Contents of each window
        self.box1.addstr(1,1,' '*26)
        self.box1.addstr(1,1,_uptime.center(26, ' '))

        self.box2.addstr(1,1,'      OK: {}'.format(receive_ok))
        self.box2.addstr(2,1,'    Fail: {}'.format(receive_errors))
        self.box2.addstr(3,1,' Percent: {}%'.format(receive_perc))

        self.box3.addstr(1,1,'      OK: {}'.format(transmit_ok))
        self.box3.addstr(2,1,'    Fail: {}'.format(transmit_errors))
        self.box3.addstr(3,1,' Percent: {}%'.format(transmit_perc))

        self.box4.addstr(1,1,'      OK: {}'.format(send_ok))
        self.box4.addstr(2,1,'    Fail: {}'.format(send_errors))
        self.box4.addstr(3,1,' Percent: {}%'.format(send_perc))

        self.box5.addstr(1,1,'    File: final.conf')
        self.box5.addstr(2,1,'     IPs: {}'.format(len(dest_ip_list)))

        self.box6.addstr(1,1,'  Local:{}:{}'.format(binding_ip, dest_port))
        self.box6.addstr(2,1,' Remote:{}:{}'.format(source_ip, source_port))

        self.box7.addstr(1,1,'  Rx: {} kb'.format(round(int(netstat[1])/1000)))
        self.box7.addstr(2,1,'  Tx: {} kb'.format(round(int(netstat[2])/1000)))

        self.box8.addstr(1,1,' '*26)
        self.box8.addstr(1,1,'DO NOT CLOSE'.center(26, ' '), curses.color_pair(1))

        self.box9.addstr(1,1,' '*26)
        self.box9.addstr(1,1,str(delay).center(26, ' '))

        # Ascii window
        for y, line in enumerate(self.ascii_art.splitlines(), 2):
            self.box10.addstr(y, 2, line)
        
        # Refresh whole screen and each window
        self.stdscr.refresh()
        self.box1.refresh()
        self.box2.refresh()
        self.box3.refresh()
        self.box4.refresh()
        self.box5.refresh()
        self.box6.refresh()
        self.box7.refresh()
        self.box8.refresh()
        self.box9.refresh()
        self.box10.refresh()


def asciiArt():
    '''
    Litterally just returns ascii art 
    '''
    return(
    r'''
                }--O--{
                  [^]
                 /ooo\
 ______________:/o   o\:______________
|=|=|=|=|=|=|:A|":|||:"|A:|=|=|=|=|=|=|
^""""""""""""""!::{o}::!""""""""""""""^
                \     /
                 \.../
      ____       "---"       ____
     |\/\/|=======|*|=======|\/\/|
     :----"       /-\       "----:
                 /ooo\
                #|ooo|#
                 \___/
    '''
    )



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

    # Initialize curses display
    _display = display()

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

        # Refresh the screen
        _display.screen()