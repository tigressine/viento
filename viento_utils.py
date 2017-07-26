#!/usr/bin/env python3
"""
Common utility functions for viento. This script includes functions used by other aspects
of the viento program, as well as paths for all non-.py files used by the program. If you 
would like to change the paths for any of the non-.py files feel free to edit them below.

Author: tgsachse (Tiger Sachse)
Initial Release: 7/13/2017
Current Release: 7/27/2017
Version: 0.5.0-beta
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
    they are created. The necessary directories are defined by the directories list.
    """
    for each in directories:
        if not os.path.exists(each):
            os.mkdir(each)

def drafts_load():
    """
    Reads the drafts file defined by the variable f_drafts. If the file exists it is loaded
    into the program. If it does not, an empty list is loaded and the error is logged.
    """
    directories_check()
    try:
        with open(f_drafts, 'r') as f:
            drafts = json.load(f)
            log('file_load', args=[f_drafts])
    except FileNotFoundError:
        with open(f_drafts, 'w') as f:
            drafts = []
            json.dump(drafts, f)
            log('file_dne', args=[f_drafts])
            log('file_empty')
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

def log(key, args=[], leading_newline=False):
    """
    Writes a formatted string (key formatted with args) to the log file (f_log). If the
    primary log file becomes too large, the logs are shifted using shift_logs().
    """
    directories_check()###
    timestamp = time.strftime('[%Y-%m-%d %H:%M:%S] ', time.localtime())
    entry = log_entries[key].format(args)

    try:
        f = open(f_log.format(1), 'a')
    except FileNotFoundError:
        f = open(f_log.format(1), 'w')
    finally:
        if leading_newline == True:
            f.write('\n')
        f.write(timestamp + entry + '\n')
        f.close()

    if os.path.getsize(f_log.format(1)) > MAX_LOG:
        shift_logs()

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

def setup_check():
    """
    Checks for the existence of critical files and directories. If no drafts file
    (defined in viento_utils) exists then the program exits. If no service file
    (also defined in viento_utils) exists then the user is prompted to generate one.
    The template for this generation is defined by the list t_service.
    """
    if not os.path.exists(f_drafts):
        print("No drafts file exists. Please run 'viento setup' to make one.")
        return False

    if not os.path.exists(f_service):
        directories_check()
        s = "No service file exists. Would you like to create one at {}?".format(f_service)
        if confirm_input(prompt="(Y/n) > ", ask=s):
            with open(f_service, 'w') as f:
                for each in t_service:
                    f.write(each)
        else:
            return False
    return True

def shift_logs():
    """
    If the primary log exceeds a certain size (MAX_LOG) then the log is shelved and a
    new log is created. The maximum number of log files is defined by MAX_LOGS. After
    the max number of logs have been produced the oldest log will be deleted before each
    shelving action.
    """
    try:
        os.remove(f_log.format(MAX_LOGS))
    except OSError:
        pass
    
    for x in reversed(range(2, MAX_LOGS-1)):
        try:
            os.rename(f_log.format(x-1), f_log.format(x))
        except OSError:
            pass

def statistics_format():#UNFINISHED
    """
    """
    stats = statistics_open()
    fstats = []
    for k,v in stats.items():
        fstats.append([k,v])
    print(fstats)

def statistics_open():
    """
    Opens the statistics file, as defined by f_stats. If no file is found then
    statistics are generated as defined by the t_statistics dict.
    """
    try:
        with open(f_stats, 'r') as f:
            stats = json.load(f)
    except FileNotFoundError:
        stats = t_statistics
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
def statistics_record(stat, value):
    """
    Increments the appropriate stat by a defined value, and then saves to file.
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
f_pid = directories[3] + '/pid.dat'
f_force = directories[3] + '/force.tmp'
f_stats = directories[4] + '/stats.log'
f_log = directories[4] + '/log{}.log'
f_job = directories[5] + '/job{}.dat'

MAX_LOG = 10000
MAX_LOGS = 5

t_service = ['[Unit]\n',
             'Description=Viento Cloud Management Utility\n\n',
             '[Service]\n',
             'ExecStart=/usr/lib/python3.6/site-packages/viento_daemon.py\n\n',
             '[Install]\n',
             'WantedBy=default.target']

t_statistics = {'transfers' : ["Total Transfers:", 0],
                'uptime_min' : ["Uptime (minutes):", 0],
                'uptime_days' : ["Uptime (days/hours/minutes):", 0],
                'bytes' : ["Bytes transferred:", 0],
                'gigabytes' : ["Gigabytes transferred:", 0]}

log_entries = {'inst_new' : 'INSTANCE: new instance of Viento started',
               'inst_start' : 'INSTANCE: Viento start command executed',
               'inst_stop' : 'INSTANCE: Viento stop command executed',
               'inst_enable' : 'INSTANCE: Viento enabled at boot',
               'inst_disable' : 'INSTANCE: Viento disabled at boot',
               'state_enter' : 'STATE: entering heightened state for \'{0[0]}\' {0[1]}',
               'state_change' : 'STATE: {0[0]} interval changed to every {0[1]} minute(s)',
               'state_leave' : 'STATE: leaving heightened state for \'{0[0]}\' {0[1]}',
               'state_revert' : 'STATE: {0[0]} interval reverted to every {0[1]} minute(s)',
               'trans_success' : 'TRANSFER: {0[0]} \'{0[1]}\' >> \'{0[2]}\'',
               'trans_force' : 'TRANSFER: {0[0]} \'{0[1]}\' >> \'{0[2]}\' (forced)',
               'file_write' : 'FILE: {0[0]} change(s) made to \'{0[1]}\'',
               'file_load' : 'FILE: \'{0[0]}\' loaded',
               'file_dne' : 'FILE: \'{0[0]}\' does not exist',
               'file_empty' : 'FILE: empty list being returned, no transfer will occur'}
