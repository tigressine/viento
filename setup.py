#! /usr/bin/env python3
import os

# FUNCTIONS #
# Generical functions #
def header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("AutoClone Setup Utility (" + str(change_count) + " changes)\n")

def input_restricted(prompt, valid_list):
    i = input(prompt)
    if i in valid_list:
        return i
    else:
        return False

def print_restricted(item, max_len):
    for x in range(max_len):
        try:
            print(item[x], end='')
        except IndexError:
            print(" ", end='')

def confirm_input():
    print("Is this correct? (Y/n)")
    valid_list = ['y', 'Y', 'yes', 'Yes', 'n', 'N', 'no', 'No']
    
    while(True):
        i = input_restricted("> ", valid_list)
        if i == False:
            print("Invalid input. Please enter 'y' or 'n'.")
        elif i in valid_list[:4]:
            return True
        elif i in valid_list[4:]:
            return False

def load_links():
    links = []
    try:
        with open(f_links, 'r') as f:
            lines = f.read().splitlines()
            for each in lines:
                links.append(each.split('\t'))
    except FileNotFoundError:
        pass
    finally:
        return links

def select_link():
    
    while(True):
        print("Enter the number of the value you'd like to modify.")
        i = input("> ")
        if i.isnumeric() and int(i) <= len(links) and int(i) > 0:
            for link in links:
                if link[0] == i:
                    for x in range(1,5):
                        print_restricted(link[x], spacing[x])
                        print(" : ", end='')
                    print("\n")
                    if confirm_input():
                        return link
                    else:
                        return False
                else:
                    pass
        else:
            print("Invalid input. Please enter a number between 1 and " + str(len(links)) + ".")

# Command functions #
def command_help():
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
    global change_count

    header()
    src = str(input("Source: "))
    dest = str(input("Destination: "))
    valid_list = ['-s', '-c', 's', 'c']
    
    while(True):
        i = input("Interval: ")
        if i.isnumeric() and int(i) > 0 and int(i) <= 86400:
            intv = i
            break
        else:
            print("Invalid input. Please enter a number between 1 and 86400.")

    while(True):
        i = input_restricted("Flags: ", valid_list)
        if i == False:
            print("Invalid input. Please enter a valid flag.")
        elif i in valid_list:
            flag = i
            break
    
    print(src + "\t" + dest + "\t" + intv + "\t" + flag)

    if confirm_input():
        change_count += 1
        num = str(len(links) + 1)
        link = [num, src, dest, intv, flag]
        links.append(link)

def command_remove():
    global change_count

    header()
    command_list()

    link = select_link()
    if link:
        change_count += 1
        links.remove(link)
        for each in links:
            each[0] = str(links.index(each) + 1)

def command_edit():
    global change_count

    header()
    command_list()

    valid_list = ['1', '2', '3', '4']
    link = select_link()
    print("(1) Source:      " + link[1] + "\n" +
          "(2) Destination: " + link[2] + "\n" +
          "(3) Interval:    " + link[3] + "\n" +
          "(4) Flags:       " + link[4] + "\n")
    
    while(True):
        print("Enter the number of the value you'd like to modify.")
        i = input_restricted("> ", valid_list)
        if i == False:
            print("Invalid input. Please enter a number between 1 and 4.")
        elif i in valid_list:

            while(True):
                print("Old value: " + str(links[int(link[0]) - 1][int(i)]))
                new = input("New value: ")
                if confirm_input():
                    change_count += 1
                    links[int(link[0]) - 1][int(i)] = new
                    break
            break

def command_list():
    print("NUMBER : SOURCE : DESTINATION : INTERVAL : FLAGS")
    for each in links:    
        for x in range(5):
            print_restricted(each[x], spacing[x])
            print(" : ", end='')
        print("\n")

def command_write():
    global change_count

    with open(f_links, 'w') as f:
        for x in links:
            for y in x:
                if x.index(y) < len(x) - 1:
                    f.write(y + "\t")
                else:
                    f.write(y)
            f.write("\n")
    print(str(change_count) + " change", end='')
    if change_count != 1:
        print("s", end='')
    print(" saved to file.")
    change_count = 0


# BEGIN PROGRAM #
f_links = "links.data"
links = load_links()
change_count = 0
valid_commands = ['h', 'n', 'r', 'e', 'l', 'w', 'c', 'q']
spacing = [3, 30, 30, 5, 4]

header()
while(True):
    print("Enter a command. ('h' for help)")
    command = input_restricted("> ", valid_commands)

    if command == False:
        print("Invalid input. Please enter a valid command.")
    
    elif command == 'h':
        command_help()

    elif command == 'n':
        command_new()
        header()

    elif command == 'r':
        command_remove()
        header()

    elif command == 'e':
        command_edit()
        header()

    elif command == 'l':
        header()
        command_list()

    elif command == 'w':
        command_write()

    elif command == 'c':
        change_count = 0
        links = load_links()
        header()

    elif command == 'q':
        header()
        print("You would like to quit.")
        if confirm_input():
            os.system('cls' if os.name == 'nt' else 'clear')
            quit()
        else:
            header()
