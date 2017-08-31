#! /usr/bin/env python3
"""
This script provides a CLI to edit the .json file that stores all of the drafts
used by viento.

Author: tgsachse (Tiger Sachse)
Initial Release: 7/13/2017
Current Release: 8/01/2017
Version: 0.5.0-beta
License: GNU GPLv3
"""
import os
import json
import shutil
import signal
from viento import viento_utils
from termcolor import cprint

### CLASSES ###
class Counter:
    """
    Returns a counter object.
    Attributes: count
    Functions: __init__, increment, reset
    This may get moved to viento_utils or deleted alltogether.
    """
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0

### FUNCTIONS ###
def main():
    """
    Defines a valid dictionary that contains all possible commands. When the
    user inputs a command, if it is found in the dictionary and executed.
    """
    valid = {'c':command_clear,
             'e':command_edit,
             'h':command_help,
             'l':command_list,
             'n':command_new,
             'q':command_quit,
             'r':command_remove,
             'w':command_write}
    header()
    while(True):
        print("Enter a command. ('h' for help)")
        command = viento_utils.input_restricted("> ", valid)
        for each in valid:
            if command == each:
                valid[each]()
                break

def command_clear():
    """
    Clears all changes since the last file read by reconstructing the drafts
    variable via a new file read (drafts_load()). This resets the change_count.
    """
    global drafts #Not sure if necessary

    change_count.reset()
    drafts = viento_utils.drafts_load()
    header()

def command_edit():
    """
    Lists all drafts in the drafts variable. Then the user may select a
    specific draft to modify. After, the user selects which value of the draft
    to modify. Once properly completed, the function saves the edited values
    and draft to the drafts variable and increments the change_count.
    """
    header()
    command_list()

    valid = ['1', '2', '3', '4']#, '5', '6']
    draft = draft_select()
    header()
    print("(1) Source:      " + draft[1] + "\n" +
          "(2) Destination: " + draft[2] + "\n" +
          "(3) Interval:    " + draft[3] + "\n" +
          "(4) Method:      " + draft[4] + "\n")# +
          #"(5) Flags:       " + draft[5] + "\n" +
          #"(6) Options:     " + draft[6] + "\n")
    
    while(True):
        print("Enter the number of the value you'd like to modify.")
        i = viento_utils.input_restricted("> ", valid)
        
        print("Old value: " + str(drafts[int(draft[0]) - 1][int(i)]))
        new = input("New value: ")
        if viento_utils.confirm_input():
            change_count.increment()
            drafts[int(draft[0]) - 1][int(i)] = new
            break

def command_help():
    """
    Prints a table of commands, names, and descriptions to the window.
    """
    header()
    print("COMMAND : NAME   : DESCRIPTION\n" +
          "      h : help   : Displays this help menu.\n" +
          "      n : new    : Creates a new draft.\n" +
          "      r : remove : Removes a specific draft.\n" +
          "      e : edit   : Edits a specific draft.\n" +
          "      l : list   : Lists all existing drafts.\n" +
          "      w : write  : Writes all changes to file.\n" +
          "      c : clear  : Clears all changes.\n" +
          "      q : quit   : Quits this setup utility.\n")

def command_list(show_header=True):
    """
    Lists all of the drafts in the drafts variable, using print_restricted()
    from viento_utils.
    """
    if show_header == True:
        header()
    spacing = [3, int((window[0]-33)/2), int((window[0]-33)/2), 8, 6]
    if window[0] % 2 == 0:
        spacing[2] += 1
    example = ['#', 'SOURCE', 'DESTINATION', 'INTERVAL', 'METHOD']
    template = [': {:^{width}} ',
                ': {:<{width}} ',
                ': {:<{width}} ',
                ': {:^{width}} ',
                ': {:^{width}} :']
    viento_utils.print_restricted(example, template, spacing, color='cyan')
    print("")
    print("{:-^{w}}".format("-", w=window[0]))
    for each in drafts:
        viento_utils.print_restricted(each, template, spacing, color='cyan')
    print("\n")

def command_new():
    """
    Retrieves input from the user for a new draft, which is then saved to the
    drafts variable. This function, if completed properly, increments the
    change_count.
    """
    header()
    source = str(input("Source (absolute path): "))
    destination = str(input("Destination (absolute path): "))
    valid = ['sync', 'copy', 'move']
    
    while(True):
        i = input("Interval (minutes): ")
        if i.isnumeric() and int(i) > 0 and int(i) < 1439:
            interval = i
            break
        else:
            print("Invalid input. Please enter a number between 1 and 1439.")

    method = viento_utils.input_restricted("Method (sync/copy/move): ", valid)

    if viento_utils.confirm_input():
        change_count.increment()
        num = str(len(drafts) + 1)
        draft = [num, source, destination, interval, method]
        drafts.append(draft)

def command_quit():
    """
    Quits the program.
    """
    header()
    if viento_utils.confirm_input(ask="Are you sure you'd like to quit? (Y/n)"):
        os.system('clear')
        quit()
    else:
        header()

def command_remove():
    """
    Retrieves input from the user to remove an existing draft. This function,
    if completely properly, increments the change_count.
    """
    header()
    command_list()

    draft = draft_select()
    change_count.increment()
    drafts.remove(draft)
    for each in drafts:
        each[0] = str(drafts.index(each) + 1)

def command_write():
    """
    Writes changes to file, and resets the change_count.
    """
    viento_utils.directories_check()
    with open(viento_utils.f_drafts, 'w') as f:
        json.dump(drafts, f)

    print(str(change_count.count) + " change", end='')
    if change_count.count != 1:
        print("s", end='')
    print(" saved to file.")
    viento_utils.log('file_write', args=[change_count.count,
                                         viento_utils.f_drafts])
    change_count.reset()
    try:
        with open(viento_utils.f_pid, 'r') as f:
            pid = int(f.read())
        os.kill(pid, signal.SIGUSR1)
    except FileNotFoundError:
        pass

def draft_select(prompt="Enter the number of the value you'd like to modify."):
    """
    Allows the user to select a draft from a list of drafts.
    """
    while(True):
        print(prompt)
        i = input("> ")
        if i.isnumeric() and int(i) <= len(drafts) and int(i) > 0:
            for draft in drafts:
                if draft[0] == i:
                    return draft
        elif i == 'q':
            break
        else:
            print("Invalid input. Please enter a number between 1 and " +
                  str(len(drafts)) + ".")

def header():
    """
    Clears the current window, then outputs the header defined by the variable
    head. The header also includes the total number of unsaved changes made by
    the user since the last write to file.
    """
    os.system('clear')
    text = "Viento Setup Utility (" + str(change_count.count) + " changes)"
    head = '{:^{width}}'.format(text, width=window[0])
    cprint(head + "\n", 'green')

### BEGIN PROGRAM ###
drafts = viento_utils.drafts_load()
change_count = Counter()
window = shutil.get_terminal_size()
if __name__ == '__main__':
    main()
