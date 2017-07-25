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
from termcolor import cprint

def confirm_input(prompt="> ", ask="Is this correct? (Y/n)"):
    """
    Prompts the user to validate his/her input.
    """
    print(ask)
    valid = ['y', 'Y', 'yes', 'Yes', 'n', 'N', 'no', 'No']
    
    while(True):
        i = input_restricted(prompt, valid)
        if i in valid[:4]:
            return True
        elif i in valid[4:]:
            return False

def directories_check():
    """
    Checks for the necessary directories in the user's home folder. If they do not exist
    they are created. The necessary directories are defined by the directories variable.
    """
    for each in directories:
        if not os.path.exists(each):
            os.mkdir(each)

def drafts_load():
    """
    Reads the links file defined by the variable f_links. If the file exists it is loaded
    into the program. If it does not, an empty list is loaded and the error is logged.
    """
    directories_check()
    try:
        with open(f_drafts, 'r') as f:
            drafts = json.load(f)
            log('FILE: \'{0}\' loaded'.format(f_drafts))
    except FileNotFoundError:
        with open(f_drafts, 'w') as f:
            drafts = []
            json.dump(drafts, f)
            log('FILE: \'{0}\' does not exist'.format(f_drafts))
            log('FILE: empty list being returned, no transfer will occur')
    return drafts

def input_restricted(prompt, valid, invalid="Invalid input."):
    """
    Compares user input to a list of valid responses. If the input is in the valid
    list, the input is returned, else the invalid statement is printed and the user
    is allowed to enter input again.
    """
    while(True):
        i = input(prompt)
        if i in valid:
            return i
        else:
            print(invalid)

def log(s, leading_newline=False):
    """
    Writes the s string into a log file, defined by the variable f_log. If the primary
    log exceeds a certain size (MAX_LOG) then the log is shelved and a new log is created.
    After 5 total logs exist the oldest log will be deleted before each shelving action.
    """
    timestamp = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime())
    directories_check()
    try:
        if os.path.getsize(f_log.format(1)) > MAX_LOG:
            try:
                os.remove(f_log.format(MAX_LOGS))
            except OSError:
                pass

            for i in reversed(range(2,MAX_LOGS-1)):
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

def print_restricted(strings, template, spacing, color=None):
    """
    Prints a list of strings spaced out on the screen according to an accompanying
    template list. Output can be colored via cprint and the color variable.
    """
    string_list = []
    for each in zip(strings, template, spacing):
        segment = each[1].format(each[0][:each[2]], width=each[2])
        string_list.append(segment)

    for each in string_list:
        if color == None:
            print(each, end='')
        else:
            cprint(each, color, end='')

def statistics_format():#UNFINISHED
    """
    """
    stats = statistics_open()
    fstats = []
    for k,v in stats.items():
        fstats.append([k,v])
    print(fstats)

def statistics_open():#UNFINISHED
    """
    """
    try:
        with open(f_stats, 'r') as f:
            stats = json.load(f)
    except FileNotFoundError:
        stats = statistics
    return stats

def statistics_print():#UNFINISHED
    """
    """
    stats = statistics_format()
    template = ['{:<{width}}','{:^{width}}']
    spacing = [20,25]
    '''
    for k,v in statistics.items():
        rprint([k,str(v)], template, spacing)
        print("")
    '''
def statistics_record(stat, value):#UNFINISHED
    """
    """
    stats = statistics_open()
    for key in stats:
        if stat == key:
            stats[key] += value

    with open(f_stats, 'w') as f:
        json.dump(stats, f)

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
f_service = directories[2] + '/viento.service'
f_drafts = directories[3] + '/drafts.json'
f_stats = directories[4] + '/stats.log'
f_log = directories[4] + '/log{}.log'
f_job = directories[5] + '/job{}.dat'

MAX_LOG = 10000
MAX_LOGS = 5

statistics = {'transfers' : ["Total Transfers:", 0],
              'uptime_min' : ["Uptime (minutes):", 0],
              'uptime_days' : ["Uptime (days/hours/minutes):", 0],
              'bytes' : ["Bytes transferred:", 0],
              'gigabytes' : ["Gigabytes transferred:", 0]}

log_entries = {'inst_new' : 'INSTANCE: new instance of Viento started',
               'state_enter' : 'STATE: entering heightened state for \'{0}\' {1}',
               'state_change' : 'STATE: {0} interval changed to every {1} minute(s)',
               'state_leave' : 'STATE: leaving heightened state for \'{0}\' {1}',
               'state_revert' : 'STATE: {0} interval reverted to every {1} minute(s)',
               'trans_success' : 'TRANSFER: {0} \'{1}\' >> \'{2}\'',
               'file_load' : 'FILE: \'{0}\' loaded',
               'file_dne' : 'FILE: \'{0}\' does not exist',
               'file_empty' : 'FILE: empty list being returned, no transfer will occur',
               'file_size' : 'FILE: log size exceeded, logs shifted'}
               
