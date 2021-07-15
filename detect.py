#!/usr/bin/env python3

import sys 
import os
import sqlite3
import multiprocessing 
from functools import partial 
import csv

# dictionary containing info about Ubuntu specific words/commands (with file/line number description)
# format: { key: filepath, value: {key: command, value: [line numbers]} }
files_commands = {}

# dictionary containing info about Ubuntu specific packages (with file/line number description)
# format: { key: filepath, value: {key: package name, value: [line numbers]} }
files_packages = {}

# dictionary containing info about Ubuntu specific filepaths (with file/line number description)
# format: { key: filepath, value: ubuntu relative path}
filepaths = {}

# usage function for Ubuntu detection tool 
def usage():
    print("Ubuntu Detection Tool: Usage Information")
    print("")

    # different modes in which the tool can be ran 
    print("For specified file, RUN: ./detect.py [FILE PATH]")
    print("For specified directory, RUN: ./detect.py [DIRECTORY PATH]")
    print("To scan entirecobase, in top-level directory RUN: ./detect.py")

    print("")
    print("For more information please visit: aka.ms/ubuntu-detection")

    # exit the tool 
    sys.exit(0)
    
# convert dictionary data for files_commands and file_packages into .csv file format for customer to reference 
def output_csv1(replacement_dict, data_dict, csv_filename):
    # name csv file 
    csv_file = csv_filename + ".csv"

    # open file with write permissions 
    with open(csv_file, 'w') as f:  
        writer = csv.writer(f)

        # iterate through dictionary containing data and add to csv file 
        for filepath, syntax_dict in data_dict.items():
            for syntax, line_nums in syntax_dict.items():
                writer.writerow([filepath, syntax, line_nums, replacement_dict[syntax]])
    
    return True


# convert dictionary data for filepaths into .csv file format for customer to reference 
def output_csv2(replacement_dict, data_dict, csv_filename):
    # name csv file 
    csv_file = csv_filename + ".csv"

    # open file with write permissions 
    with open(csv_file, 'w') as f:  
        writer = csv.writer(f)

        # iterate through dictionary containing data and add to csv file 
        for filepath, relative_filepath in data_dict:
            writer.writerow([filepath, relative_filepath, replacement_dict[relative_filepath]])
    
    return True


# populate Mariner replacement dictionary 
def mariner_replacements():
    # establish connection with databse containing Ubuntu syntax 
    conn = sqlite3.connect('database/ubuntu.db')

    # set connection cursor 
    cur = conn.cursor()

    # get each Ubuntu command in db and put into list
    cur.execute('SELECT command from commands')
    commands = cur.fetchall()

    # get each Ubuntu command replacement in db and put into list 
    cur.execute('SELECT mariner_replacement from commands')
    command_replacements = cur.fetchall()

    # get each Ubuntu package in db and put into list
    cur.execute('SELECT package from packages')
    packages = cur.fetchall()

    # get each Ubuntu package replacement in db and put into list 
    cur.execute('SELECT mariner_replacement from packages')
    package_replacements = cur.fetchall()

    # get each Ubuntu filepath in db and put into list
    cur.execute('SELECT filepath from filepaths')
    filepaths = cur.fetchall()

    # get each Ubuntu filepath replacement in db and put into list 
    cur.execute('SELECT mariner_replacement from filepaths')
    filepath_replacements = cur.fetchall()

    # initial dictionary 
    replacement_dict = {}

    # add commands + replacements to dictionary 
    for index, command in enumerate(commands): 
        replacement_dict[str(command[0])] = str(command_replacements[index][0])
    
    # add packages + replacements to dictionary 
    for index, package in enumerate(packages): 
        replacement_dict[str(package[0])] = str(package_replacements[index][0])

    # add filepaths + replacements to dictionary 
    for index, filepath in enumerate(filepaths): 
        replacement_dict[str(filepath[0])] = str(filepath_replacements[index][0])

    # close database connection
    conn.close() 

    # return newly populated dictionary 
    return replacement_dict


# function to add command information to the files_commands dictionary   
def add_commands(path, commands_dict):
    # add to the command_dict as the value for the file path in files_commands
    files_commands[path] = commands_dict

    return True 


# function to add package information to the files_packages dictionary   
def add_packages(path, packages_dict):
    # add to the packages_dict as the value for the file path in files_packages
    files_packages[path] = packages_dict

    return True 


# function to scan file for specific package names and extensions
def package_scan(path, package):
    # ensure path is a file by opening 
    f = open(path)

    # check to make sure f exists:
    if not f: 
        print("ERROR: " + path + " is not a readable file")
        return {}
    
    # put pacakage name in proper string format 
    p = str(package[0])

    # create temp dictionary to return 
    package_dict = {p: []}

    # loop through file and check if package name is anywhere in the file 
    # try/except for when file is unreadable 
    try:
        for line_num, line in enumerate(f, 1):
            # get line and strip 
            code = str(line.strip())
            # check if the package is in the line
            if p in code:
                # if it is add it to the temp dictionary 
                package_dict[p].append(line_num)
    except UnicodeDecodeError:
        # print("UnicodeDecodeError Exception")
        return {}

    # properly close the file 
    f.close()

    # return temporary dictionary 
    return package_dict


# function to scan line for specfic commands 
def command_scan(path, command):
    # ensure path is a file by opening 
    f = open(path)

    # check to make sure f exists:
    if not f: 
        print("ERROR: " + path +" is not a readable file")
        return False 
    
    # put command in proper format 
    c = str(command[0])

    # create temp dictionary to return 
    command_dict = {c: []}

    # loop through file and check if command is anywhere in the file 
    # try/except for when file is unreadable 
    try:
        for line_num, line in enumerate(f, 1):
            # strip new line and call line_scan
            code = str(line.strip())
                # check if the command is in the line
            if c in code:
                # if it is add it to the temp dictionary 
                command_dict[c].append(line_num)
    except UnicodeDecodeError:
        # print("UnicodeDecodeError Exception")
        return {}

    # properly close the file 
    f.close()

    # return temporary dictionary 

    return command_dict


# function to scan file and send to proper function using multiprocessing 
def file_scan(path):
    # establish connection with databse containing Ubuntu syntax 
    conn = sqlite3.connect('database/ubuntu.db')

    # set connection cursor 
    cur = conn.cursor()

    # COMMANDS - this is where the script scans for Ubuntu specific commands 
    # get each Ubuntu command in db and put into list
    cur.execute('SELECT command from commands')

    # inputs is the list of commands
    inputs = cur.fetchall()

    # records is the number of commands the db contains 
    records = len(inputs)

    # start processing pool, with a process for each record
    pool = multiprocessing.Pool()
    pool = multiprocessing.Pool(processes=records)

    # set args for these command_scan function calls 
    func_command = partial(command_scan, path)

    # do processing - process for each command
    commands = pool.map(func_command, inputs)

    # merge commands into one dict 
    temp_dict = {}
    for item in commands:
        for key, value in item.items():
            if len(value) >= 1:
                temp_dict[key] = value
    
    # if temp_dict is NOT empty: add temp_dict with commands + line numbers to files_commands 
    if temp_dict:
        add_commands(path, temp_dict)

    
    # PACKAGES 
    # get each Ubuntu package in db and put into list
    cur.execute('SELECT package from packages')

    # inputs is the list of packages
    inputs = cur.fetchall()

    # records is the number of packages the db contains 
    records = len(inputs)

    # start processing pool, with a process for each record
    pool = multiprocessing.Pool()
    pool = multiprocessing.Pool(processes=records)

    # set args for these package_scan function calls 
    func_package = partial(package_scan, path)

    # do processing - process for each package
    packages = pool.map(func_package, inputs)

    # merge commands into one dict 
    temp_dict = {}
    for item in packages:
        for key, value in item.items():
            if len(value) >= 1:
                temp_dict[key] = value
    
    # if temp_dict is NOT empty: add temp_dict with packages + line numbers to greater files dictionary 
    if temp_dict:
        add_packages(path, temp_dict)
    

    # close database connection
    conn.close() 
    
    # return out of function to scan next item
    return True


# function to scan directory name for Ubuntu-specifics
def dirname_scan(dir_path):
    # establish connection with databse containing Ubuntu syntax 
    conn = sqlite3.connect('database/ubuntu.db')

    # set curser 
    cur = conn.cursor()

    # FILE PATHS 
    # get each Ubuntu-specific path in db and put into list
    cur.execute('SELECT filepath from filepaths')

    # paths contains all ubuntu-specific file paths in database 
    paths = cur.fetchall()

    # loop through every path in paths and check to see if current directory path contains path 
    for path in paths:
        # put path in correct string format 
        path = str(path[0])
        # if it does add info to the global dictionary directory_paths 
        if path in dir_path:
            filepaths[dir_path] = path 

    # close database connection
    conn.close()

    # return out of function to scan next item
    return True


# function to scan directories for its contents and send to the proper scanning function
def dir_scan(cwd): 
    # scan directory name for Ubuntu-specifics 
    dirname_scan(cwd)

    # get items in directory 
    dir_items = os.listdir(cwd)

    # remove ubuntu.db file
    if "ubuntu.db" in dir_items: 
        dir_items.remove("ubuntu.db")

    # remove detect.py file
    if "detect.py" in dir_items: 
        dir_items.remove("detect.py")

    # walk through items in directory 
    for item in dir_items:
        # construct full path of item
        full_path = cwd + '/' + item 

        # check if item is a file -> if yes, call scan_file 
        if os.path.isfile(full_path):
            file_scan(full_path)   

        # check if item is a directory -> if yes, call scan_dir 
        elif os.path.isdir(full_path):
            dir_scan(full_path)

        # else continue 
        else:
            continue

    # return to main or out of recursion
    return True 


def main():
    # if singular file or directory is inputted (argv = 2), determine if file or directory, and call proper file 
    if len(sys.argv) == 2:
        # put path in proper string format 
        path = str(sys.argv[1])
        # if path is a file call file_scan
        if os.path.isfile(path):
            file_scan(path)
        # elif path is a directory call dir_scan
        elif os.path.isdir(path):
            dir_scan(path)
        # if it is niether print error and call usage 
        else:
            print("ERROR: Inputted invald file/directory path.")
            print("")
            usage()

    # if no inputted file (argv = 1), call scan_dir on current path
    elif len(sys.argv) == 1:
        # get the current working directory path and call scan_dir 
        cwd_path = os.getcwd()
        dir_scan(cwd_path) 

    # call usage if argv > 2 
    else:
        usage()
    
    # populate mariner replacement dictionary 
    replacement_dict = mariner_replacements()

    # call output_csv to output data file for both packages and commands 
    output_csv1(replacement_dict, files_commands, "commands")
    output_csv1(replacement_dict, files_packages, "packages")
    output_csv2(replacement_dict, filepaths, "filepaths")

    return True 


if __name__ == '__main__':
    # call main
    main()  