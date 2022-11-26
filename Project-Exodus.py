import click
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
    print('      -search      |     Search for target by name')
    print('      -stats       |     Get targets followers, following, and post count')
    print('      -photo       |     Get targets profile picture')
    print('      -posts       |     Download all targets posts (pictures only)')
    print('      -compare     |     Compares inputted photo to posts made by target')
    print('      -delete      |     Deletes all gathered info on target')
    print('      -reset       |     Resets the screen')
    print('      -exit        |     Exits the program')
    
    # print('      -email       | Get targets email')
    # print('      -phone       | Get targets phone number')
    # print('      -dox         | Get targets address')
    print(colors.reset)

def reboot():
    print(colors.red + 'Rebooting Program' + colors.reset)
    os.system('cls')

def startProgram():
    InstaPWN.init()
    reboot()
    splashScreen()
    print_menu()

def selection():
    
    usr_input = input(colors.reset + 'Please enter a command: ' + colors.grey).lower().split()
    
    if len(usr_input) == 0:
        selection()
    elif usr_input[0] == '-h' or usr_input[0] == '-help':
        print_menu()
        selection()
    elif usr_input[0] == '-exit' or usr_input[0] == 'exit':
        print(colors.red + 'Exiting Program' + colors.reset)
        InstaPWN.driver.quit()
        quit()
    elif usr_input[0] == '-reset':
        print(colors.red + 'Resetting Program' + colors.reset)
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
    elif usr_input[0] == '-stats':
        if usr_input[1] == '-h' or usr_input[1] == '-help':
            print(colors.yellow + '-stats [username of target]')
            print(colors.yellow + 'Examples:')
            print(colors.yellow + '    -stats project__exodus')
            selection()
        else:
            InstaPWN.getStats(usr_input[1])
            selection()
    elif usr_input[0] == '-photo':
        if usr_input[1] == '-h' or usr_input[1] == '-help':
            print(colors.yellow + '-photo [username of target]')
            # print(colors.yellow + '-photo [username of target][-png -jpg]')
            print(colors.yellow + '    Downloads the targets profile picture')
            # print(colors.yellow + '\n    Options:')
            # print(colors.yellow + '        -png        specifies file type *.png')
            # print(colors.yellow + '        -jpg        specifies file type *.jpg')
            
            
            selection()
        else:
            if len(usr_input) == 2:
                InstaPWN.getPhoto(usr_input[1])
                selection()
            else:
                print(colors.red + 'Invalid syntax' + colors.reset)
                selection()
    elif usr_input[0] == '-posts':
        if usr_input[1] == '-h' or usr_input[1] == '-help':
            print(colors.yellow + '-posts [username of target]')
            print(colors.yellow + '    downloads the targets posts as images only (will add support for videos later)')
            # print(colors.yellow + '\n    Options:')
            # print(colors.yellow + '        -png        specifies file type *.png')
            # print(colors.yellow + '        -jpg        specifies file type *.jpg')
            
            
            selection()
        else:
            if len(usr_input) == 2:
                InstaPWN.getPosts(usr_input[1])
                selection()
            else:
                print(colors.red + 'Invalid syntax' + colors.reset)
                selection()
    elif usr_input[0] == '-compare':
        if usr_input[1] == '-h' or usr_input[1] == '-help':
            print(colors.yellow + '-compare [username of target]')
            print(colors.yellow + '    compares inputted photo of target with posts made by target username')
            # print(colors.yellow + '\n    Options:')
            # print(colors.yellow + '        -png        specifies file type *.png')
            # print(colors.yellow + '        -jpg        specifies file type *.jpg')
            
            
            selection()
        else:
            if len(usr_input) == 2:
                InstaPWN.comparePhotosAndPosts(usr_input[1])
                selection()
            else:
                print(colors.red + 'Invalid syntax' + colors.reset)
                selection()
    elif usr_input[0] == '-delete':
        if len(usr_input) == 1:
                print(colors.red + 'Invalid syntax' + colors.reset)
                selection()
        if usr_input[1] == '-h' or usr_input[1] == '-help':
            print(colors.yellow + '-delete [username of target]')
            print(colors.yellow + '    Deletes all gathered target info')
            selection()
        if usr_input[1] == '-all':
            InstaPWN.deleteAllTargetsInfo()
            selection()
        else:
            if len(usr_input) == 2 and usr_input[1] != '':
                InstaPWN.deleteTargetData(usr_input[1])
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
