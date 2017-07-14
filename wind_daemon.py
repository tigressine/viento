#! /usr/bin/env python3
"""
This script is the central daemon behind Wind. It pulls custom links from a .json
file, then it executes rclone commands based on information in the custom links. The
script outputs to log files defined by the variables f_log1 and f_log2.

Author: tgsachse (Tiger Sachse)
Initial Release: 7/13/2017
Current Release: 7/14/2017
Version: 0.2.0-beta
License: GNU GPLv3
"""
import os
import re
import json
import time
import signal
import threading

### CLASSES ###
class Link():
    """
    Returns Link object.
    Attributes: f_job, src, dest, interval, method, flags, count, intv_persist, command
    Functions: __init__, transfer, react, learn
    """
    def __init__(self, attributes):
        """
        Initializes Link object with several attributes.
        """
        self.f_job = f_job_template.format(attributes[0])
        self.src = attributes[1]
        self.dest = attributes[2]
        self.interval = int(attributes[3])
        self.method = attributes[4]
        # Not yet implemented.
        self.flags = ['-r']#attributes[5]
        
        self.count = 0
        self.intv_persist = self.interval
        self.command = 'rclone -v {0} {1} {2} &> {3}'.format(self.method,
                                                             self.src,
                                                             self.dest,
                                                             self.f_job)
    def transfer(self):
        """
        Executes a system command using self.command.
        If enabled, link object can react and learn from the results of this command.
        """
        os.system(self.command)
        log('TRANSFER: {0} \'{1}\' >> \'{2}\''.format(self.method,
                                                      self.src,
                                                      self.dest))
        if '-r' in self.flags:
            self.react()
        if '-l' in self.flags:
            self.learn()

    def react(self):
        """
        If enabled, the script will react to the outcome of the command executed in
        transfer(). It does this by using the re module to scan a job.dat file (which
        contains the verbose output of the command executed in transfer()). If the re
        module finds a match in the .dat file (e.g. the string ':Copied (new)') then
        the script will put itself into a heightened mode. This heightened mode results
        in a shortened interval for transfers, starting at 1 minute intervals and, after
        enough iterations of transfer() without any more activity, the intervals decay
        back to original values (stored in self.intv_persist).
        """
        job_matches = [': Copied \(new\)',
                       ': Copied\(replaced existing\)',
                       ': Deleted']
        job_match = '|'.join(job_matches)
        # This list pair defines how long the script will remain heightened, in intervals.
        react_len = [2,3]

        with open(self.f_job, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if re.search(job_match, line):
                    self.interval = 1
                    self.count = 1
                    log('STATE: entering heightened state for \'{0}\' {1}'.format(self.src,
                                                                                  self.method))
                    log('STATE: {0} interval changed to every {1} minute(s)'.format(self.method,
                                                                                    self.interval))
                    break
        
        if self.count >= react_len[1]:
            self.interval = self.intv_persist
            self.count = 0
            log('STATE: leaving heightened state for \'{0}\' {1}'.format(self.src,
                                                                         self.method))
            log('STATE: {0} interval reverted to every {1} minute(s)'.format(self.method,
                                                                             self.interval))
        elif self.count >= react_len[0] and self.intv_persist != 1:
            self.interval = 2
            self.count += 1
            log('STATE: {0} interval changed to every {1} minute(s)'.format(self.method,
                                                                            self.interval))
        elif self.count > 0:
            self.count += 1

    def learn(self):
        """
        WIP
        """
        pass


### FUNCTIONS ###
def check_dirs():
    """
    Checks for the required directories in the user's home folder.
    If they do not exist they are created. The required directories are defined
    by the variable dirs.
    """
    for each in dirs:
        if not os.path.exists(each):
            os.mkdir(each)

def load_links():
    """
    Reads the .json file at the path defined by the variable f_links. If the file
    exists the script will log an error but continue and process nothing. Perhaps
    this should be more dramatic.
    """
    try:
        with open(f_links, 'r') as f:
            x = json.load(f)
            links = []
            for each in x:
                links.append(Link(each))
            log('FILE: \'{0}\' loaded'.format(f_links))
            return links
    except FileNotFoundError:
        log('FILE: \'{0}\' does not exist'.format(f_links))
        log('FILE: empty list being returned, no transfers will occur')
        return []

def log(s):
    """
    Logs the passed string variable s into logs defined by the variables f_log1
    and f_log2. The length of these logs is capped by the variable max_log. If
    the primary log (f_log1) becomes too large, the secondary log (f_log2) is deleted,
    f_log1 becomes f_log2, and a new f_log1 is created.
    """
    max_log = 10000
    timestamp = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime())
    
    try:
        if os.path.getsize(f_log1) > max_log:
            os.remove(f_log2)
            os.rename(f_log1, f_log2)

            with open(f_log1, 'w') as f:
                f.write(timestamp +
                        'LOG SIZE EXCEEDED: \'{0}\' moved, \'{1}\' deleted'.format(f_log1,
                                                                                   f_log2))
                f.write('\n' + timestamp + s + '\n')
        else:        
            with open(f_log1, 'a') as f:
                f.write(timestamp + s + '\n')
    
    except FileNotFoundError:
        with open(f_log1, 'w') as f:
            f.write(timestamp + s + '\n')

def signal_SIGUSR1_handler(signum, frame):
    """
    WIP
    """
    pass

def main():
    """
    Contains the script's main while loop that drives the entire daemon. For each link
    described in the list links, the while loop determines if the appropriate interval
    of time has passed before that link's command should be executed. If it has passed,
    the while loop executes that command in a new thread.
    """
    log('INSTANCE: new instance of Wind started')

    while(True):
        hour = int(time.strftime('%H', time.localtime()))
        minute = int(time.strftime('%M', time.localtime()))
        minutes = minute + (60 * hour)

        for each in links:
            if minutes % each.interval == 0:
                threading.Thread(target=each.transfer).start()
        time.sleep(60)


### PROGRAM START ###
"""
These variables define where all the files that Wind needs are located, besides
the actual .py scripts. These variables should be changeable as you see fit. It will
be necessary to edit them in all 3 .py scripts however (i.e. this script, the wind_setup.py
script, and the main wind script).
"""
dirs = [os.path.expanduser('~/.wind'),
        os.path.expanduser('~/.wind/logs'),
        os.path.expanduser('~/.wind/jobs')]
f_links = dirs[0] + '/links.json'
f_log1 = dirs[1] + '/daemon.log'
f_log2 = dirs[1] + '/daemon_old.log'
f_job_template = dirs[2] + '/job{}.dat'

check_dirs()
links = load_links()

signal.signal(signal.SIGUSR1, signal_SIGUSR1_handler)

main()
