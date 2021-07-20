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

    # exit the tool 
    sys.exit(0)
    
# convert dictionary data for found_commands and found_packages into .csv file format for customer to reference 
def output_csv1(replacement_dict, data_dict, csv_filename):
    # name csv file 
    csv_file = csv_filename + ".csv"

    # open file with write permissions 
    with open(csv_file, 'w') as f:  
        writer = csv.writer(f)

        # iterate through dictionary containing data and add to csv file 
        for filepath, syntax_dict in data_dict.items():
            for syntax, line_nums in syntax_dict.items():
                replacement = replacement_dict[syntax]
                writer.writerow([filepath, line_nums, syntax, replacement[0], replacement[1]])
    
    return True


# convert dictionary data for filepaths into .csv file format for customer to reference 
def output_csv2(replacement_dict, data_dict, csv_filename):
    # name csv file 
    csv_file = csv_filename + ".csv"

    # open file with write permissions 
    with open(csv_file, 'w') as f:  
        writer = csv.writer(f)

        # iterate through dictionary containing data and add to csv file 
        for filepath, relative_filepath in data_dict.items():
            replacement = replacement_dict[relative_filepath]
            writer.writerow([filepath, relative_filepath, replacement[0], replacement[1]])
    
    return True


# function to add package information to the found_packages dictionary   
def add_packages(path, packages_dict):
    # add to the packages_dict as the value for the file path in found_packages
    found_packages[path] = packages_dict

    return True 


# function to add command information to the found_commands dictionary   
def add_commands(path, commands_dict):
    # add to the command_dict as the value for the file path in found_commands
    found_commands[path] = commands_dict

    return True 


# function to scan file for specific package names and extensions
def package_scan(path, package):
    # ensure path is a file by opening 
    f = open(path)

    # check to make sure f exists:
    if not f: 
        print("ERROR: " + path + " is not a readable file")
        return {}

    # create temp dictionary to return 
    package_dict = {package: []}

    # loop through file and check if package name is anywhere in the file 
    # try/except for when file is unreadable 
    try:
        for line_num, line in enumerate(f, 1):
            # get line and strip 
            code = str(line.strip())
            # check if the package is in the line
            if package in code:
                # if it is add it to the temp dictionary 
                package_dict[package].append(line_num)
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

    # create temp dictionary to return 
    command_dict = {command: []}

    # loop through file and check if command is anywhere in the file 
    # try/except for when file is unreadable 
    try:
        for line_num, line in enumerate(f, 1):
            # strip new line and call line_scan
            code = str(line.strip())
                # check if the command is in the line
            if command in code:
                # if it is add it to the temp dictionary 
                command_dict[command].append(line_num)
    except UnicodeDecodeError:
        # print("UnicodeDecodeError Exception")
        return {}

    # properly close the file 
    f.close()

    # return temporary dictionary 
    return command_dict


# function to scan file and send to proper function using multiprocessing 
def file_scan(path):
    # COMMANDS - this is where the script scans for Ubuntu specific commands
    # start processing pool, with a process for each for number of CPUs
    pool = multiprocessing.Pool()
    pool = multiprocessing.Pool(processes=os.cpu_count())

    # set args for these command_scan function calls 
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

    # set args for these package_scan function calls 
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
    
    # return out of function to scan next item
    return True


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

    # set args for these package_scan function calls 
    func_path = partial(dirname_scan_multi, dir_path)

    # do processing - process for each package
    paths = pool.map(func_path, ubuntu_filepaths_list)

    # if path was found, add to the found_filepaths dictionary 
    for path in paths:
        if path != '':
            found_filepaths[dir_path] = path

    # return out of function to scan next item
    return True


# function to scan directories for its contents and send to the proper scanning function
def dir_scan(dir_path): 
    # scan directory name for Ubuntu-specifics 
    dirname_scan(dir_path)

    # get items in directory 
    dir_items = os.listdir(dir_path)

    # walk through items in directory 
    for item in dir_items:
        # construct full path of item
        full_path = dir_path + '/' + item 

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


# function to read .csv data files into respective data structures 
def csv_reader(packages, commands, filepaths):
    # PACKAGES: open packages.csv and read into data structures
    with open(packages) as csvfile:
        # use csv.reader to parse
        data = csv.reader(csvfile, delimiter = ',')
        
        # loop through row by row 
        for contents in data:
            # set each element in list properly 
            ubuntu_package = contents[0]
            mariner_replacement = contents[1]
            notes = contents[2] 

            # append to ubuntu_packages_list 
            ubuntu_packages_list.append(ubuntu_package)

            # add to ubuntu_packages_dict 
            ubuntu_packages_dict[ubuntu_package] = [mariner_replacement, notes]

    # COMMANDS: open commands.csv and read into data structures
    with open(commands) as csvfile:
        # use csv.reader to parse
        data = csv.reader(csvfile, delimiter = ',')
        
        # loop through row by row
        for contents in data:
            # set each element in list properly 
            ubuntu_command = contents[0]
            mariner_replacement = contents[1]
            notes = contents[2] 

            # append to ubuntu_commands_list 
            ubuntu_commands_list.append(ubuntu_command)

            # add to ubuntu_commands_dict 
            ubuntu_commands_dict[ubuntu_command] = [mariner_replacement, notes]
    
    # FILEPATHS: open filepaths.csv and read into data structures
    with open(filepaths) as csvfile:
        # use csv.reader to parse
        data = csv.reader(csvfile, delimiter = ',')
   
        # loop through row by row 
        for contents in data:
            # set each element in list properly 
            ubuntu_fp = contents[0]
            mariner_replacement = contents[1]
            notes = contents[2] 

            # append to ubuntu_filepaths_list 
            ubuntu_filepaths_list.append(ubuntu_fp)

            # add to ubuntu_filepaths_dict 
            ubuntu_filepaths_dict[ubuntu_fp] = [mariner_replacement, notes]

    # return to main
    return True


def main():
    # if singular file or directory is inputted (argv = 2), determine if file or directory, and call proper file 
    if len(sys.argv) == 2:
        # put path in proper string format 
        path = str(sys.argv[1])
        
        # check if path is usage
        if path == "usage":
            usage()
        
        # call csv_reader on data files 
        csv_reader("database/packages.csv", "database/commands.csv", "database/filepaths.csv")
        
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
   
    # call usage if argv != 2 
    else:
        usage()

    # call output_csv to output data file for both packages and commands 
    output_csv1(ubuntu_packages_dict, found_packages, "package_data")
    output_csv1(ubuntu_commands_dict, found_commands, "command_data")
    output_csv2(ubuntu_filepaths_dict, found_filepaths, "filepath_data")

    return True 


if __name__ == '__main__':
    # call main
    main()  