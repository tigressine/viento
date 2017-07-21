#! /usr/bin/env python3
"""
This script provides a CLI to edit the .json file that stores all of the links
used by viento.

Author: tgsachse (Tiger Sachse)
Initial Release: 7/13/2017
Current Release: 7/21/2017
Version: 0.4.0-beta
License: GNU GPLv3
"""
import os
import json
import shutil
import viento_utils
from termcolor import cprint

### CLASSES ###
class Counter:
    """
    Returns a counter object.
    Attributes: count
    Functions: __init__, increment, reset
    """
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0

### FUNCTIONS ###
# Generical functions #
def header():
    """
    Clears the current window, then outputs the header defined by the variable
    head. The header also includes the total number of unsaved changes made by the
    user since the launch of the program.
    """
    os.system('clear')
    text = "Viento Setup Utility (" + str(change_count.count) + " changes)"
    head = '{:^{width}}'.format(text, width=window[0])
    cprint(head + "\n", 'green')

def input_restricted(prompt, valid):
    """
    Confirms that a given input is valid, as defined by the valid list var.
    """
    while(True):
        i = input(prompt)
        if i in valid:
            return i
        else:
            print("Invalid input.")

def print_restricted(s, space_list):
    """
    Prints to the window in 5 columns. Needed to list all links.
    """
    entry = ': {:^{w1}} : {:<{w2}} : {:<{w3}} : {:^{w4}} : {:^{w5}} :'
    string = entry.format(s[0][:space_list[0]],
                          s[1][:space_list[1]],
                          s[2][:space_list[2]],
                          s[3][:space_list[3]],
                          s[4][:space_list[4]],
                          w1=space_list[0],
                          w2=space_list[1],
                          w3=space_list[2],
                          w4=space_list[3],
                          w5=space_list[4])
    print(string)

def confirm_input():
    """
    Produces a prompt to allow the user to check his/her input.
    """
    print("Is this correct? (Y/n)")
    valid = ['y', 'Y', 'yes', 'Yes', 'n', 'N', 'no', 'No']
    
    while(True):
        i = input_restricted("> ", valid)
        if i in valid[:4]:
            return True
        elif i in valid[4:]:
            return False

def select_link():
    """
    Allows the user to select a link from a list of links.
    """
    while(True):
        print("Enter the number of the value you'd like to modify.")
        i = input("> ")
        if i.isnumeric() and int(i) <= len(links) and int(i) > 0:
            for link in links:
                if link[0] == i:
                    return link
        else:
            print("Invalid input. Please enter a number between 1 and " + str(len(links)) + ".")

# Command functions #
def command_help():
    """
    Prints a table of commands, names, and descriptions to the window.
    """
    header()
    print("COMMAND : NAME   : DESCRIPTION\n" +
          "      h : help   : Displays this help menu.\n" +
          "      n : new    : Creates a new link.\n" +
          "      r : remove : Removes a specific link.\n" +
          "      e : edit   : Edits a specific link.\n" +
          "      l : list   : Lists all existing links.\n" +
          "      w : write  : Writes all changes to file.\n" +
          "      c : clear  : Clears all changes.\n" +
          "      q : quit   : Quits this setup utility.\n")

def command_new():
    """
    Retrieves input from the user for a new link, which is then saved to the
    links variable. This function, if completed properly, increments the
    change_count.
    """
    header()
    src = str(input("Source (absolute path): "))
    dest = str(input("Destination (absolute path): "))
    valid = ['sync', 'copy', 'move']
    
    while(True):
        i = input("Interval (minutes): ")
        if i.isnumeric() and int(i) > 0 and int(i) <= 1440:
            intv = i
            break
        else:
            print("Invalid input. Please enter a number between 1 and 1440.")

    method = input_restricted("Method (sync/copy/move): ", valid)

    if confirm_input():
        change_count.increment()
        num = str(len(links) + 1)
        link = [num, src, dest, intv, method]
        links.append(link)

def command_remove():
    """
    Retrieves input from the user to remove an existing link. This function,
    if completely properly, increments the change_count.
    """
    header()
    command_list()

    link = select_link()
    change_count.increment()
    links.remove(link)
    for each in links:
        each[0] = str(links.index(each) + 1)

def command_edit():
    """
    Lists all links in the links variable. Then the user may select a specific
    link to modify. After, the user selects which value of the link to modify.
    Once properly completed, the function saves the edited values and link to the
    links variable and increments the change_count.
    """
    header()
    command_list()

    valid = ['1', '2', '3', '4']
    link = select_link()
    header()
    print("(1) Source:      " + link[1] + "\n" +
          "(2) Destination: " + link[2] + "\n" +
          "(3) Interval:    " + link[3] + "\n" +
          "(4) Method:      " + link[4] + "\n")
    
    while(True):
        print("Enter the number of the value you'd like to modify.")
        i = input_restricted("> ", valid)
        
        print("Old value: " + str(links[int(link[0]) - 1][int(i)]))
        new = input("New value: ")
        if confirm_input():
            change_count.increment()
            links[int(link[0]) - 1][int(i)] = new
            break

def command_list():
    """
    Lists all of the links in the links variable, using the print_restricted
    function.
    """
    example = ['#', 'SOURCE', 'DESTINATION', 'INTERVAL', 'METHOD']
    print_restricted(example, spacing)
    print("{:-^{w}}".format("-", w=window[0]))
    for each in links:
        print_restricted(each, spacing)
    print("")

def command_write():
    """
    Writes changes to file, and resets the change_count.
    """
    viento_utils.check_directories()
    with open(viento_utils.f_links, 'w') as f:
        json.dump(links, f)

    print(str(change_count.count) + " change", end='')
    if change_count.count != 1:
        print("s", end='')
    print(" saved to file.")
    change_count.reset()

def command_clear():
    change_count.reset()
    links = viento_utils.load_links()#####probably has to be global
    header()

def command_quit():
    header()
    print("You would like to quit.")
    if confirm_input():
        os.system('clear')
        quit()
    else:
        header()

def main():
    valid = {'h':command_help,
             'n':command_new,
             'r':command_remove,
             'e':command_edit,
             'l':command_list,
             'w':command_write,
             'c':command_clear,
             'q':command_quit}
    header()
    while(True):
        print("Enter a command. ('h' for help)")
        command = input_restricted("> ", valid)
        for each in valid:
            if command == each:
                valid[each]()
                break

### BEGIN PROGRAM ###
viento_utils.check_directories()
links = viento_utils.load_links()
change_count = Counter()

"""
The following variables determine the size of the current terminal window and then
save the appropriate spacings into a spacing list. This list is used by the
command_list() function.
"""
window = shutil.get_terminal_size()
####################################################
spacing = [3, None, None, 8, 6]
f_name_spacing = int((window[0] - spacing[0] - spacing[3] - spacing[4] - 16)/2)
spacing[1] = f_name_spacing
spacing[2] = f_name_spacing #CLEANUP######################################

if __name__ == '__main__':
    main()
