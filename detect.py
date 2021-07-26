#!/usr/bin/env python3

import sys 
import os
import multiprocessing 
from functools import partial 
import csv

# dictionary containing info about Ubuntu specific packages (with file/line number description)
# format: { key: filepath, value: {key: package name, value: [line numbers]} }
found_packages = {}

# dictionary containing info about Ubuntu specific words/commands (with file/line number description)
# format: { key: filepath, value: {key: command, value: [line numbers]} }
found_commands = {}

# dictionary containing info about Ubuntu specific filepaths (with file/line number description)
# format: { key: filepath, value: ubuntu relative path}
found_filepaths = {}

# lists containing Ubuntu-specific instances from packages.csv, commands.csv, and filepaths.csv
ubuntu_packages_list = []
ubuntu_commands_list  = [] 
ubuntu_filepaths_list = []

# dictionaries containing Ubuntu-specific instances from packages.csv, commands.csv, and filepaths.csv as keys and the Mariner replacement + notes as values
ubuntu_packages_dict ={}
ubuntu_commands_dict = {}
ubuntu_filepaths_dict = {}


# usage function for Ubuntu detection tool 
def usage():
    print("Ubuntu Detection Tool: Usage Information")
    print("")
    # different modes in which the tool can be ran 
    print("For specified file, RUN: ./detect.py [FUll FILE PATH]")
    print("For specified directory/codebase, RUN: ./detect.py [ FULL DIRECTORY PATH]")
    print("")
    print("For more information please visit: aka.ms/ubuntu-detection")
    sys.exit(0)


# convert dictionary data for found_commands and found_packages into .csv file format for customer to reference 
def output_csv(replacement_dict, data_dict, csv_filename, type):
    csv_file = csv_filename + ".csv"
    with open(csv_file, 'w') as f:  
        writer = csv.writer(f)
        # TYPE == 1: iterate through dictionary containing data and add to csv file 
        if type == 1:
            for filepath, syntax_dict in data_dict.items():
                for syntax, line_nums in syntax_dict.items():
                    replacement = replacement_dict[syntax]
                    writer.writerow([filepath, line_nums, syntax, replacement[0], replacement[1]])
        # TYPE == 2: iterate through dictionary containing data and add to csv file 
        if type == 2:
            for filepath, relative_filepath in data_dict.items():
                replacement = replacement_dict[relative_filepath]
                writer.writerow([filepath, relative_filepath, replacement[0], replacement[1]])


# function to add package information to the found_packages dictionary   
def add_packages(path, packages_dict):
    # add to the packages_dict as the value for the file path in found_packages
    found_packages[path] = packages_dict


# function to add command information to the found_commands dictionary   
def add_commands(path, commands_dict):
    # add to the command_dict as the value for the file path in found_commands
    found_commands[path] = commands_dict


# function to scan file for specific package names and extensions
def package_scan(path, package):
    f = open(path)
    if not f: 
        print("ERROR: " + path + " is not a readable file")
        return {}
    # create temp dictionary to return 
    package_dict = {package: []}
    # loop through file and check if package name is anywhere in the file 
    try:
        for line_num, line in enumerate(f, 1):
            code = str(line.strip())
            if package in code:
                package_dict[package].append(line_num)
    except UnicodeDecodeError:
        #sprint("UnicodeDecodeError Exception")
        return {}
    f.close()
    return package_dict


# function to scan line for specfic commands 
def command_scan(path, command):
    f = open(path)
    if not f: 
        print("ERROR: " + path +" is not a readable file")
        return False 
    # create temp dictionary to return 
    command_dict = {command: []}
    # loop through file and check if command is anywhere in the file 
    # try/except for when file is unreadable 
    try:
        for line_num, line in enumerate(f, 1):
            code = str(line.strip())
            if command in code:
                command_dict[command].append(line_num)
    except UnicodeDecodeError:
        #print("UnicodeDecodeError Exception")
        return {}
    f.close()
    return command_dict


# function to scan file and send to proper function using multiprocessing 
def file_scan(path):
    # COMMANDS - this is where the script scans for Ubuntu specific commands
    # start processing pool, with a process for each for number of CPUs
    pool = multiprocessing.Pool()
    pool = multiprocessing.Pool(processes=os.cpu_count())
    func_command = partial(command_scan, path)
    # do processing - process for each command
    commands = pool.map(func_command, ubuntu_commands_list)
    # merge commands into one dict 
    temp_dict = {}
    for item in commands:
        for key, value in item.items():
            if len(value) >= 1:
                temp_dict[key] = value
    # if temp_dict is NOT empty: add temp_dict with commands + line numbers to found_commands 
    if temp_dict:
        add_commands(path, temp_dict)
    
    # PACKAGES
    # start processing pool, with a process for each for number of CPUs
    pool = multiprocessing.Pool()
    pool = multiprocessing.Pool(processes=os.cpu_count())
    func_package = partial(package_scan, path)
    # do processing - process for each package
    packages = pool.map(func_package, ubuntu_packages_list)
    # merge commands into one dict 
    temp_dict = {}
    for item in packages:
        for key, value in item.items():
            if len(value) >= 1:
                temp_dict[key] = value
    # if temp_dict is NOT empty: add temp_dict with packages + line numbers to greater files dictionary 
    if temp_dict:
        add_packages(path, temp_dict)
    

# function to do multiprocessing for dirname_scan
def dirname_scan_multi(dir_path, path):
    # if the path is in the dir_path add info to the global dictionary directory_paths 
    if path in dir_path:
        return path
    return ''    


# function to scan directory name for Ubuntu-specific filepath
def dirname_scan(dir_path):
    # start processing pool, with a process for each for number of CPUs
    pool = multiprocessing.Pool()
    pool = multiprocessing.Pool(processes=os.cpu_count())
    func_path = partial(dirname_scan_multi, dir_path)
    # do processing - process for each package
    paths = pool.map(func_path, ubuntu_filepaths_list)
    # if path was found, add to the found_filepaths dictionary 
    for path in paths:
        if path != '':
            found_filepaths[dir_path] = path


# function to scan directories for its contents and send to the proper scanning function
def dir_scan(dir_path): 
    # scan directory name for Ubuntu-specifics 
    dirname_scan(dir_path)
    dir_items = os.listdir(dir_path)
    for item in dir_items:
        full_path = dir_path + '/' + item 
        if os.path.isfile(full_path):
            file_scan(full_path)   
        elif os.path.isdir(full_path):
            dir_scan(full_path)
        else:
            continue


# function to read .csv data files into respective data structures 
def csv_reader(packages, commands, filepaths):
    # PACKAGES: open packages.csv and read into data structures
    with open(packages) as csvfile:
        data = csv.reader(csvfile, delimiter = ',')        
        for contents in data:
            ubuntu_package = contents[0]
            mariner_replacement = contents[1]
            notes = contents[2] 
            ubuntu_packages_list.append(ubuntu_package)
            ubuntu_packages_dict[ubuntu_package] = [mariner_replacement, notes]

    # COMMANDS: open commands.csv and read into data structures
    with open(commands) as csvfile:
        data = csv.reader(csvfile, delimiter = ',')
        for contents in data:
            ubuntu_command = contents[0]
            mariner_replacement = contents[1]
            notes = contents[2] 
            ubuntu_commands_list.append(ubuntu_command)
            ubuntu_commands_dict[ubuntu_command] = [mariner_replacement, notes]
    
    # FILEPATHS: open filepaths.csv and read into data structures
    with open(filepaths) as csvfile:
        data = csv.reader(csvfile, delimiter = ',')
        for contents in data:
            ubuntu_fp = contents[0]
            mariner_replacement = contents[1]
            notes = contents[2] 
            ubuntu_filepaths_list.append(ubuntu_fp)
            ubuntu_filepaths_dict[ubuntu_fp] = [mariner_replacement, notes]


def main():
    # if singular file or directory is inputted (argv = 2), determine if file or directory, and call proper function
    if len(sys.argv) == 2:
        path = str(sys.argv[1])
        if path == "usage":
            usage()
        csv_reader("database/packages.csv", "database/commands.csv", "database/filepaths.csv")
        if os.path.isfile(path):
            file_scan(path)
        elif os.path.isdir(path):
            dir_scan(path)
        else:
            print("ERROR: Inputted invald file/directory path.")
            print("")
            usage()
    else:
        usage()

    # call output_csv to output data file for both packages and commands 
    output_csv(ubuntu_packages_dict, found_packages, "package_data", 1)
    output_csv(ubuntu_commands_dict, found_commands, "command_data", 1)
    output_csv(ubuntu_filepaths_dict, found_filepaths, "filepath_data", 2)


if __name__ == '__main__':
    main()  