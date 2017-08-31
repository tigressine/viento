#! /usr/bin/env python3
"""
The engine of viento. Transfers files on specified intervals according to a
list of 'drafts.' Can accept signals to force transfers, as well as learn from
previous transfers.

Author: tgsachse (Tiger Sachse)
Initial Release: 7/13/2017
Current Release: 8/31/2017
Version: 0.6.0-beta
License: GNU GPLv3
"""
import os
import re
import time
import signal
import threading
from viento import viento_utils

### CLASSES ###
class Draft:
    """
    Returns a draft object.
    Attributes: id, source, destination, interval, method, flags, options,
                job_path, job_contents, count, adjust_lengths,
                interval_persist, transferring, time_executed, command
    Methods: __init__, main, command_construct, command_run, interval_adjust,
             interval_learn, job_read, statistics_save, transfer_check
    """
    def __init__(self, attributes):
        """
        Defines a whole ton of attributes based on the attributes argument. The
        job file is read and self.command is constructed.
        """
        self.id = attributes[0]
        self.source = attributes[1]
        self.destination = attributes[2]
        self.interval = int(attributes[3])
        self.method = attributes[4]
        #self.flags = attributes[5]
        self.options = ['react']#attributes[6]

        self.job_path = viento_utils.f_job.format(self.id)

        self.count = 0
        self.adjust_lengths = [2, 3]
        self.interval_persist = self.interval

        self.transferring = False
        self.time_executed = 0
        self.command = self.command_construct()

    def main(self, time_executed):
        """
        Calls self.command_run() and logs the action. Then calls functions that
        correspond to the options found in the self.options variable.
        """
        self.time_executed = time_executed
        self.command_run()
        viento_utils.log('trans_success', args=[self.method,
                                                self.source,
                                                self.destination])

        if 'adjust' in self.options:
            self.interval_adjust()
        if 'learn' in self.options:
            self.interval_learn() 

    def command_construct(self, redirect_output=True):
        """
        Builds a command string to be executed by the self.main() method.
        """
        command = 'rclone -v {0} '.format(self.method)
        #if len(self.flags) != 0: 
        #    for each in self.flags:
        #        command += '{0} '.format(each)
        command += '{0} {1} '.format(self.source, self.destination)
        if redirect_output == True:
            command += '&> {0}'.format(self.job_path)
        return command

    def command_run(self):
        """
        Refreshes the draft's job file, if it exists, then runs the command.
        Afterwards any relevant statistics are saved by statistics_save().
        """
        if os.path.exists(self.job_path):
            os.remove(self.job_path)
        self.transferring = True
        os.system(self.command)
        self.statistics_save()
        self.transferring = False

    def interval_adjust(self):
        """
        If the daemon detects that changes have been made in a transferred
        directory, then the daemon will change the interval for the changed
        directory temporarily to increase the likelihood of transferring newly
        changed files as quickly as possible.
        """
        if self.transfer_check():
            self.interval = 1
            self.count = 1
            viento_utils.log('state_enter', args=[self.source, self.method])
            viento_utils.log('state_change', args=[self.method, self.interval])

        elif self.count >= self.adjust_lengths[1]:
            self.interval = self.interval_persist
            self.count = 0
            viento_utils.log('state_leave', args=[self.source, self.method])
            viento_utils.log('state_revert', args=[self.method, self.interval])

        elif (self.count >= self.adjust_lengths[0] and 
              self.interval_persist != 1):
            self.interval = 2
            self.count += 1
            viento_utils.log('state_change', args=[self.method, self.interval])

        elif self.count > 0:
            self.count += 1

    def interval_learn(self):
        """
        It'll be lit, but you gotta wait fam.
        """
        pass

    def job_read(self, path):
        """
        Reads the job file.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                contents = f.readlines()
        except FileNotFoundError:
            contents = []
        return contents

    def statistics_save(self):
        """
        Reads statistics by pulling them from the job file, via regex. Saves
        them to the statistics file defined by viento_utils.f_stats.
        """
        self.job_contents = self.job_read(self.job_path)
        match_bytes = (r'^Transferred:(\s*)(?P<bytes>[0-9.]+) ' + 
                       r'(?P<type>[kMGT]*)Bytes \([0-9.]+ .*Bytes/s\)')
        match_transfers = r'^Transferred:(\s*)(?P<transfers>[0-9]+)$'
        for line in reversed(self.job_contents):
            if re.match(match_bytes, line):
                value = float(re.match(match_bytes, line).group('bytes'))
                prefix = re.match(match_bytes, line).group('type')
                if prefix == '':
                    stat_bytes = value
                elif prefix == 'k':
                    stat_bytes = value*1024**1
                elif prefix == 'M':
                    stat_bytes = value*1024**2
                elif prefix == 'G':
                    stat_bytes = value*1024**3
                viento_utils.statistics_record('bytes', int(stat_bytes))
                break

        for line in reversed(self.job_contents):
            if re.match(match_transfers, line):
                stat_transfers = int(re.match(match_transfers,
                                              line).group('transfers'))
                viento_utils.statistics_record('transfers', stat_transfers)
                break

    def transfer_check(self):
        """
        Checks the job_contents loaded from the job file. If any of the
        matches_transfers strings are found in the job_contents, returns True.
        """
        self.job_contents = self.job_read(self.job_path)
        matches_transfers = [': Copied \(new\)$',
                             ': Copied\(replaced existing\)$',
                             ': Deleted$']
        for line in self.job_contents:
            if re.match('|'.join(matches_transfers), line):
                return True
        else:
            return False

### FUNCTIONS ###
def main():
    """
    A while loop that checks the time periodically. If the checked time divided
    by the interval of a draft equals 0 (if the interval has been reached) then
    the main() method of the draft is executed.
    """
    with open(viento_utils.f_pid, 'w') as f:
        f.write(str(os.getpid()))
    signal.signal(signal.SIGUSR1, handler_SIGUSR1)
    signal.signal(signal.SIGUSR2, handler_SIGUSR2)
    viento_utils.log('inst_new', leading_newline=True)
    while(True):
        hour = int(time.strftime('%H', time.localtime()))
        minute = int(time.strftime('%M', time.localtime()))
        new_minutes = minute + (60 * hour)
        try:
            if new_minutes != minutes:
                viento_utils.statistics_record('uptime_min', 1)
        except UnboundLocalError:
            pass
        minutes = new_minutes

        for each in drafts:
            if all([minutes % each.interval == 0,
                    each.time_executed != minutes,
                    each.transferring == False]):
                threading.Thread(target=each.main, args=(minutes,)).start()
        time.sleep(20)

def handler_SIGUSR1(signum, frame):
    """
    Reinitializes the daemon. This reloads the drafts variable and is signalled
    primarily by viento_setup. When viento_setup saves a new draft file, the
    daemon is told to reinitialize via this handler.
    """
    initialize()

def handler_SIGUSR2(signum, frame):
    """
    Reads the ID to force from the f_force file. Then forces that draft to
    transfer and logs the action. Finally removes the f_force temporary file.
    """
    with open(viento_utils.f_force, 'r') as f:
        force_id = f.read()
        for each in drafts:
            if each.id == force_id:
                each.command_run()
                viento_utils.log('trans_force', args=[each.method,
                                                      each.source,
                                                      each.destination])
                break
    os.remove(viento_utils.f_force)

def initialize():
    global drafts

    viento_utils.directories_check()
    drafts = []
    for each in viento_utils.drafts_load():
        drafts.append(Draft(each))

### BEGIN PROGRAM ###
if __name__ == '__main__':
    initialize()
    main()
