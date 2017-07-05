#! /usr/bin/env python3
import os

# Functions #
def header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("AutoClone Setup Utility (" + str(change_count) + " changes)\n")

def input_specific(prompt, valid_input):
    i = input(prompt)
    if i in valid_input:
        return i
    else:
        return False

def confirm():
    print("\nIs this correct? (Y/n)")
    while(True):
        valid = ['y','Y','yes','Yes','n','N','no','No']
        yn = input_specific("> ", valid)
        if yn in valid[:4]:
            return True
        elif yn in valid[4:]:
            return False
        elif yn == False:
            print("Invalid response")

def load_links():
    global new_links

    try:
        with open("links.data","r") as f:
            pass
    except FileNotFoundError:
        with open("links.data","w") as f:
            pass
    finally:
        with open("links.data","r") as f:
            new_links = []
            lines = f.readlines()
            for line in lines:
                new_links.append(line.split("\t"))

def list_links():
    print("Number\tSource\tDestination\tFlag\tInterval\n")
    for x in new_links:
        for y in x:
            print(y + "\t", end="")
        print("")
    print("\n")

def select_link(action):
    while(True):
        print("Enter the number of the link you'd like to " + action + ".")
        i = input("> ")

        if i == 'q':
            return False

        elif i.isnumeric() and int(i) <= len(new_links) and int(i) != 0:
            for x in new_links:
                if x[0] == i:
                    for each in x:
                        print(each + "\t", end="")
                        if confirm():
                            return x
                        else:
                            break
                else:
                    pass
        else:
            print("Please enter a number between 1 and " + str(len(new_links)) + ".")




def main():
    global change_count

    change_count = 0
    valid = ['h', 'n', 'r', 'e', 'l', 'w', 'c', 'q']
    header()
    while(True):
        print("Enter a command. ('h' for help)")
        i = input_specific("> ", valid)
    
        if i == 'h': #help
            header()
            print("COMMAND : NAME   : DESCRIPTION\n" +
                  "      h : help   : Brings up the help menu\n" +
                  "      n : new    : Creates a new link\n" +
                  "      r : remove : Removes a selected link\n" +
                  "      e : edit   : Edits a selected link\n" +
                  "      l : list   : Lists all existing links\n" +
                  "      w : write  : Writes changes to file\n" +
                  "      c : clear  : Clears changes to file\n" +
                  "      q : quit   : Quits the setup utility\n")

        elif i == 'n': #new
            header()
            src = str(input("Source: "))
            dest = str(input("Destination: "))
            
            while(True):
                valid_flags = ['-s', '-c']
                i = input_specific("Flags: ", valid_flags)
                if i != False:
                    flag = i
                    break
                else:
                    print("Enter a valid flag")

            while(True):
                intv = input("Interval: ")   
                if intv.isnumeric():
                    intv = int(intv)
                    if intv > 0 and intv <= 86400:
                        intv = str(intv)
                        break
                else:
                    print("Enter a number between 1 and 86400")

            print("\n" + src + "\t" + dest + "\t" + flag + "\t" + intv + "\n")
            
            if confirm():
                change_count += 1
                link_num = str(len(new_links) + 1)
                new_link = [link_num, src, dest, flag, intv]
                new_links.append(new_link)
            header()

        elif i == 'r': #remove
            header()
            list_links()

            bad_link = select_link("remove")
            if bad_link:
                change_count += 1
                new_links.remove(bad_link)
                for each in new_links:
                    if each[0] != str(new_links.index(each) + 1):
                        each[0] = str(new_links.index(each) + 1)
            header()

        elif i == 'e': #edit
            header()
            list_links()
            edit_link = select_link("edit")
            print("(1) Source:      " + edit_link[1] + "\n" +
                  "(2) Destination: " + edit_link[2] + "\n" +
                  "(3) Flags:       " + edit_link[3] + "\n" +
                  "(4) Interval:    " + edit_link[4])
            valid_nums = ['1', '2', '3', '4']

            def edit_element(link, element): #####
                while(True):
                    print("Old value: " + str(new_links[int(link)-1][int(element)]))
                    i = input("New value: ")
                    if confirm():
                        change_count += 1
                        new_links[link-1][element] = i
                        break

            while(True):
                print("Select the number of the value you'd like to modify.")
                i = input_specific("> ", valid_nums)
                if i == False:
                    print("Select a number between 1 and 4.")
                elif i in valid_nums:

                    while(True):
                        print("Old value: " + str(new_links[int(edit_link[0])-1][int(i)]))
                        x = input("New value: ")
                        if confirm():
                            change_count += 1
                            new_links[int(edit_link[0])-1][int(i)] = x
                            print(new_links[int(edit_link[0])-1][int(i)])
                            break
                    header()
                    break

        elif i == 'l': #list
            header()
            list_links()
            
        elif i == 'w': #write
            print(change_count)

        elif i == 'q': #quit
            header()
            print("You would like to quit")
            if confirm():
                os.system('cls' if os.name == 'nt' else 'clear')
                quit()
            else:
                header()

        else: #invalid
            print("invalid")

load_links()
main()
