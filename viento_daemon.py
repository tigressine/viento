#! /usr/bin/env python3
"""
This script is the central daemon behind Viento. It pulls custom links from a .json
file, then it executes rclone commands based on information in the custom links. The
script outputs to log files defined by the variables f_log1 and f_log2.

Author: tgsachse (Tiger Sachse)
Initial Release: 7/13/2017
Current Release: 7/21/2017
Version: 0.4.0-beta
License: GNU GPLv3
"""
import os
import re
import json
import time
import signal
import threading
import viento_utils

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
        self.f_job = viento_utils.f_job.format(attributes[0])
        self.src = attributes[1]
        self.dest = attributes[2]
        self.interval = int(attributes[3])
        self.method = attributes[4]
        # Not yet implemented.
        self.flags = ['-r']#attributes[5]
        
        self.count = 0
        self.intv_persist = self.interval### CLEANUP?VVVV
        self.command = 'rclone -v {0} {1} {2} &> {3}'.format(self.method,
                                                             self.src,
                                                             self.dest,
                                                             self.f_job)
        self.command_force = 'rclone -v {0} {1} {2}'.format(self.method,
                                                            self.src,
                                                            self.dest)
    def force(self):
        """
        Executes a system command based on self.command_force. This command is intended
        to be used by the main viento program to force a transfer outside of regular
        intervals or when the daemon is not running.
        """
        os.system(self.command_force)
        viento_utils.log('TRANSFER: {0} \'{1}\' >> \'{2}\' (forced)'.format(self.method,
                                                                            self.src,
                                                                            self.dest))

    def transfer(self):
        """
        Executes a system command using self.command. If enabled, link object can react
        and learn from the results of this command.
        """
        if os.path.exists(self.f_job):
            os.remove(self.f_job)
        os.system(self.command)
        viento_utils.log('TRANSFER: {0} \'{1}\' >> \'{2}\''.format(self.method,
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
        ######################Can trip up with no file exist
        with open(self.f_job, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if re.search(job_match, line):
                    self.interval = 1
                    self.count = 1
                    viento_utils.log('STATE: entering heightened state for \'{0}\' {1}'.format(self.src,
                                                                                               self.method))
                    viento_utils.log('STATE: {0} interval changed to every {1} minute(s)'.format(self.method,
                                                                                                 self.interval))
                    break
        
        if self.count >= react_len[1]:
            self.interval = self.intv_persist
            self.count = 0
            viento_utils.log('STATE: leaving heightened state for \'{0}\' {1}'.format(self.src,
                                                                                      self.method))
            viento_utils.log('STATE: {0} interval reverted to every {1} minute(s)'.format(self.method,
                                                                                          self.interval))
        elif self.count >= react_len[0] and self.intv_persist != 1:
            self.interval = 2
            self.count += 1
            viento_utils.log('STATE: {0} interval changed to every {1} minute(s)'.format(self.method,
                                                                                         self.interval))
        elif self.count > 0:
            self.count += 1

    def learn(self):
        """
        It'll be lit, but you gotta wait fam.
        """
        pass


### FUNCTIONS ###
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
    viento_utils.log('INSTANCE: new instance of Viento started', leading_newline=True)
    viento_utils.check_directories()
    while(True):
        hour = int(time.strftime('%H', time.localtime()))
        minute = int(time.strftime('%M', time.localtime()))
        minutes = minute + (60 * hour)

        for each in links:
            if minutes % each.interval == 0:
                threading.Thread(target=each.transfer).start()
        time.sleep(60)

### BEGIN PROGRAM ###
links_list = viento_utils.load_links()
links = []
for each in links_list:
    links.append(Link(each))
signal.signal(signal.SIGUSR1, signal_SIGUSR1_handler)

if __name__ == '__main__':
    main()
