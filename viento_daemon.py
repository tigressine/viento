#! /usr/bin/env python3
"""
"""
import os
import re
import time
import signal
import threading
import viento_utils

######################################## CLASSES #########################################
class Draft:
    """
    """
    def __init__(self, attributes):
        """
        """
        self.job_path = viento_utils.f_job.format(attributes[0])
        self.job_contents = self.job_read(self.job_path)

        self.source = attributes[1]
        self.destination = attributes[2]
        self.interval = int(attributes[3])
        self.method = attributes[4]
        self.flags = attributes[5]
        self.options = attributes[6]

        self.count = 0
        self.adjust_lengths = [2, 3]
        self.interval_persist = self.interval

        self.transferring = False
        self.time_executed = 0
        self.command = self.command_construct()

    def main(self, time_executed):
        """
        """
        self.time_executed = time_executed
        self.command_run()
        entry = 'TRANSFER: {0} \'{1}\' >> \'{2}\''.format(self.method,
                                                          self.source,
                                                          self.destination)
        viento_utils.log(entry)

        if 'adjust' in self.options:
            self.interval_adjust()
        if 'learn' in self.options:
            self.interval_learn()

    def command_construct(self, redirect_output=True):
        """
        """
        command = 'rclone -vv {0} '.format(self.method)
        if len(self.flags) != 0: 
            for each in self.flags:
                command += '{0} '.format(each)
        command += '{0} {1} '.format(self.source, self.destination)
        if redirect_output == True:
            command += '&> {0}'.format(self.job_path)
        return command

    def command_run(self):
        """
        """
        if os.path.exists(self.job_path):
            os.remove(self.job_path)
        self.transferring = True
        os.system(self.command)
        self.transferring = False

    def interval_adjust(self):
        """
        """
        if self.transfer_check():
            self.interval = 1
            self.count = 1
            entry = 'STATE: entering heightened state for \'{0}\' {1}'.format(self.source,
                                                                              self.method)
            viento_utils.log(entry)
            entry = 'STATE: {0} interval changed to every {1} minute(s)'.format(self.method,
                                                                                self.interval)
            viento_utils.log(entry)

        elif self.count >= self.adjust_lengths[1]:
            self.interval = self.interval_persist
            self.count = 0
            entry = 'STATE: leaving heightened state for \'{0}\' {1}'.format(self.source,
                                                                             self.method)
            viento_utils.log(entry)
            entry = 'STATE: {0} interval reverted to every {1} minute(s)'.format(self.method,
                                                                                 self.interval)
            viento_utils.log(entry)

        elif self.count >= self.adjust_lengths[0] and self.interval_persist != 1:
            self.interval = 2
            self.count += 1
            entry = 'STATE: {0} interval changed to every {1} minute(s)'.format(self.method,
                                                                                self.interval)
            viento_utils.log(entry)

        elif self.count > 0:
            self.count += 1

    def interval_learn(self):
        """
        It'll be lit, but you gotta wait fam.
        """
        pass

    def job_read(self, path):
        """
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                contents = f.readlines()
        except FileNotFoundError:
            contents = []
        return contents

    def statistics_save(self):
        """
        """
        pass

    def transfer_check(self):
        """
        """
        matches_transfers = [': Copied \(new\)$',
                             ': Copied\(replaced existing\)$',
                             ': Deleted$']
        for line in self.job_contents:
            if re.match('|'.join(matches_transfers), line):
                return True
        else:
            return False

######################################## FUNCTIONS ######################################
def main():
    """
    """
    signal.signal(signal.SIGUSR1, handler_SIGUSR1)
    viento_utils.log('INSTANCE: new instance of Viento started', leading_newline=True)
    while(True):
        hour = int(time.strftime('%H', time.localtime()))
        minute = int(time.strftime('%M', time.localtime()))
        minutes = minute + (60 * hour)

        for each in drafts:
            if minutes % each.interval == 0 and each.time_executed != minutes:
                threading.Thread(target=each.main, args=(minutes,)).start()
        time.sleep(20)

def pid_get():
    """
    """
    return os.getpid()

def handler_SIGUSR1(signum, frame):
    """
    """
    for each in drafts:
        if each.transferring == True:
            return True
    else:
        return False

##################################### BEGIN PROGRAM #####################################
if __name__ == '__main__':
    viento_utils.directories_check()
    drafts_list = viento_utils.drafts_load()
    drafts = []
    for each in drafts_list:
        drafts.append(Draft(each))
    main()
