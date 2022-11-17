import os, sys
import InstaPWN
from splashscreen import splashScreen
from Colors import colors
version_number = 0.1

def print_menu():
    print(colors.yellow + '''    Core commands of the application. Some commands require 
    multiple arguments which can be shown with -h or -help
    ''')    
    print('    Options:')
    print('      -clear       | Clears the Screen')
    print('      -exit        | Exits the program')
    print('      -search      | Search for target by name')
    print('      -username    | Get targets followers, following, and posts')
    print('      -photo       | Get targets profile picture')
    print('      -posts       | Download all targets posts')
    # print('      -email       | Get targets email')
    # print('      -phone       | Get targets phone number')
    # print('      -dox         | Get targets address')
    print(colors.reset)

def startProgram():
    reboot()
    splashScreen()
    print_menu()

def reboot():
    print(colors.red + 'Rebooting Program' + colors.reset)
    os.system('cls')

def selection():
    usr_input = input(colors.reset + 'Please enter a command: ' + colors.grey).lower().split()
    if usr_input[0] == '-h' or usr_input[0] == '-help':
        print_menu()
        selection()
    elif usr_input[0] == '-exit' or usr_input[0] == 'exit':
        print(colors.red + 'Exiting Program' + colors.reset)
        quit()
    elif usr_input[0] == '-clear':
        print(colors.red + 'Rebooting Program' + colors.reset)
        os.system('cls')
        startProgram()
        selection()
    elif usr_input[0] == '-search':
        if usr_input[1] == '-h' or usr_input[1] == '-help':
            print(colors.yellow + '-search [first_name] [last_name] [num_results] [-scan]')
            print(colors.yellow + '    returns a list of top google results of queried name')
            print(colors.yellow + '\n    Options:')
            print(colors.yellow + '        -scan        runs the -username command on all returned usernames')
            selection()
        else:
            if len(usr_input) == 2: #-search [name]
                InstaPWN.getTopResults(name=usr_input[1])
                
            elif len(usr_input) == 3 and usr_input[2].__contains__('-'): #-search [name] -scan
                InstaPWN.getTopResults(name=usr_input[1], last_name='', num_results=5, command=usr_input[2])
                
            elif len(usr_input) == 3 and usr_input[2].isdigit() and not usr_input[2].__contains__('-'): #-search [name] [num_results]
                InstaPWN.getTopResults(name=usr_input[1], last_name='', num_results=usr_input[2], command='')
                
            elif len(usr_input) == 3 and not usr_input[2].__contains__('-'): #-search [name] [last_name]
                InstaPWN.getTopResults(name=usr_input[1], last_name=usr_input[2], num_results=5, command='')
                
            elif len(usr_input) == 4  and not usr_input[2].isdigit() and not usr_input[2].__contains__('-'): #-search [name] [lastname] -scan
                InstaPWN.getTopResults(name=usr_input[1], last_name=usr_input[2], num_results=5, command=usr_input[3])
                
            elif len(usr_input) == 4  and usr_input[2].isdigit() and not usr_input[2].__contains__('-'): #-search [name] [num_resutls] -scan
                InstaPWN.getTopResults(name=usr_input[1], last_name='', num_results=usr_input[2], command=usr_input[3])
                
            elif len(usr_input) == 5: #-search [name] [last_name] [num_results] -scan
                InstaPWN.getTopResults(name=usr_input[1], last_name=usr_input[2], num_results=usr_input[3], command=usr_input[4])
                
            else:
                print(colors.red + 'Invalid syntax' + colors.reset)
        selection()     
    elif usr_input[0] == '-username':
        if usr_input[1] == '-h' or usr_input[1] == '-help':
            print(colors.yellow + '-username [username of target]')
            print(colors.yellow + 'Examples:')
            print(colors.yellow + '    -username project__exodus')
            print(colors.yellow + '    -uname project__exodus')
            selection()
        else:
            InstaPWN.getUsernameInfo(usr_input[1])
            selection()
    elif usr_input[0] == '-photo':
        if usr_input[1] == '-h' or usr_input[1] == '-help':
            print(colors.yellow + '-photo [username of target][-png -jpg]')
            print(colors.yellow + '    Outputs the profile picture of the target to a specified file type')
            print(colors.yellow + '\n    Options:')
            print(colors.yellow + '        -png        specifies file type *.png')
            print(colors.yellow + '        -jpg        specifies file type *.jpg')
            
            
            selection()
        else:
            if len(usr_input) == 3:
                InstaPWN.getPhoto(usr_input[1], usr_input[2])
                selection()
            else:
                print(colors.red + 'Invalid syntax' + colors.reset)
                selection()
    elif usr_input[0] == '-posts':
        if usr_input[1] == '-h' or usr_input[1] == '-help':
            print(colors.yellow + '-posts [username of target]')
            print(colors.yellow + '    downloads the targets posts')
            # print(colors.yellow + '\n    Options:')
            # print(colors.yellow + '        -png        specifies file type *.png')
            # print(colors.yellow + '        -jpg        specifies file type *.jpg')
            
            
            selection()
        else:
            if len(usr_input) == 2:
                InstaPWN.getMedia(usr_input[1])
                selection()
            else:
                print(colors.red + 'Invalid syntax' + colors.reset)
                selection()
    elif (len(usr_input) == 1 and usr_input[0] != '-exit' and usr_input[0] != '-reboot') or ('-' not in usr_input[0]):
        print(colors.red + 'Invalid syntax' + colors.reset)
        selection()
    else:
        print(colors.red + 'Not a valid command')
        selection()
        

if __name__=='__main__':
    startProgram()
    selection()
