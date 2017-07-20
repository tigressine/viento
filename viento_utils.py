#!/usr/bin/env python3
"""
Common utility functions for viento. This script includes functions used by other aspects
of the viento program, as well as definitions for all non-.py files used by the program.
If you would like to change the destinations for any of the non-.py files feel free to
edit them below.

Author: tgsachse (Tiger Sachse)
Initial Release: 7/13/2017
Current Release: 7/21/2017
Version: 0.4.0-beta
License: GNU GPLv3
"""
import os
import time
import json

def check_directories():
    """
    Checks for the necessary directories in the user's home folder. If they do not exist
    they are created. The necessary directories are defined by the directories variable.
    """
    for each in directories:
        if not os.path.exists(each):
            #log('FILE: {0} did not exist so it was created'.format(each))
            os.mkdir(each)

def load_links():
    """
    Reads the links file defined by the variable f_links. If the file exists it is loaded
    into the program. If it does not, an empty list is loaded and the error is logged.
    """
    check_directories()
    try:
        with open(f_links, 'r') as f:
            links = json.load(f)
            log('FILE: \'{0}\' loaded'.format(f_links))
            return links
    except FileNotFoundError:
        with open(f_links, 'w') as f:
            links = []
            json.dump(links, f)
            log('FILE: \'{0}\' does not exist'.format(f_links))
            log('FILE: empty list being returned, no transfer will occur')
            return links

def log(s, leading_newline=False):
    """
    Writes the s string into a log file, defined by the variable f_log. If the primary
    log exceeds a certain size (MAX_LOG) then the log is shelved and a new log is created.
    After 5 total logs exist the oldest log will be deleted before each shelving action.
    """
    MAX_LOG = 10000
    timestamp = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime())
    check_directories()
    try:
        if os.path.getsize(f_log.format(1)) > MAX_LOG:
            try:
                os.remove(f_log.format(5))
            except OSError:
                pass

            for i in reversed(range(2,6)):
                try:
                    os.rename(f_log.format(i-1), f_log.format(i))
                except OSError:
                    pass
            
            with open(f_log.format(1), 'w') as f:
                if leading_newline == True:
                    f.write('\n')
                f.write(timestamp +
                        'FILE: log size exceeded, logs shifted' +
                        '\n' + timestamp + s + '\n')
        else:        
            with open(f_log.format(1), 'a') as f:
                if leading_newline == True:
                    f.write('\n')
                f.write(timestamp + s + '\n')
    
    except FileNotFoundError:
        with open(f_log.format(1), 'w') as f:
            if leading_newline == True:
                f.write('\n')
            f.write(timestamp + s + '\n')

"""
The following variables are paths to various files and directories required for this
program to function properly. By design, these directories and files can be renamed here
and the rest of the program will follow suit. If you feel the need to change the paths
for the program's files, please change them here and not elsewhere, otherwise you'll stumble
into heaps of FileNotFoundErrors. :)
"""
directories = [os.path.expanduser('~/.config'),
               os.path.expanduser('~/.config/systemd'),
               os.path.expanduser('~/.config/systemd/user'),
               os.path.expanduser('~/.viento'),
               os.path.expanduser('~/.viento/logs'),
               os.path.expanduser('~/.viento/jobs')]
f_links = directories[3] + '/links.json'
f_service = directories[2] + '/viento.service'
f_log = directories[4] + '/log{}.log'
f_job = directories[5] + '/job{}.dat'
