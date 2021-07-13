#!/usr/bin/env python3

import sys 
import os
import sqlite3
import multiprocessing 
from functools import partial 

manager = multiprocessing.Manager()
files = manager.dict()

# usage function 
def usage():
    sys.exit(0)

# function to add information to the database 
def addto_db(path, command, line_num):
    # make sure file path is a key in data, if not add
    if path not in files:
        files[path] = {}
    
    # check if command is a key for data[path]
    if command in files[path].keys():
        # apend line_num to list 
        files[path][command].append(line_num)
        # ensure no duplicates of line numbers
        set(files[path][command])
    # if not in data[path] add
    else:
        files[path][command] = [line_num]

    return True 


# function to scan line for specific package names and extensions
def package_scan(package, line):

    return None 


# function to scan line for specific file paths 
def filepath_scan(filepath, line):
    
    return None 


# function to scan line for specfic commands 
def command_scan(path, line_num, line, command):
    # put in proper format 
    c = str(command[0])
    l = str(line)

    # check if the command is in the line
    if c in l:
        addto_db(path, c, line_num)

    return files


# function to scan line in a file
def line_scan(path, line, line_num):
    # establish connection with databse containing Ubuntu syntax 
    conn = sqlite3.connect('ubuntu.db')
    cur = conn.cursor()

    # COMMANDS 
    # get each Ubuntu command in db and put into list
    cur.execute('SELECT command from commands')
    inputs = cur.fetchall()
    records = len(inputs)

    # start processing pool, with a process for each record
    pool = multiprocessing.Pool()
    pool = multiprocessing.Pool(processes=records)

    # set line arg for these command_scan function calls 
    #func_command = partial 
    func_command = partial(command_scan, path, line_num, line)

    # do processing 
    files = pool.map(func_command, inputs)

    #if found_commands != ['']:
        #print(found_commands)

    # output information about found commands 
    #print(found_commands)
    
    # FILE PATHS 
    # scan line for each Ubuntu file path in database 
    # use multiprocessing here 


    # PACKAGES 
    # scan line for each Ubuntu package in database 
    # use multiprocessing here 


    # close database connection
    conn.close() 

    return True 

# function to scan file 
def file_scan(path):
    # ensure path is a file by opening 
    f = open(path)

    # check to make sure f exists:
    if not f: 
        return False 

    # get line and line number 
    try:
        for line_num, line in enumerate(f, 1):
            # strip new line and call line_scan
            code = line.strip()
            line_scan(path, code, line_num)
    except UnicodeDecodeError:
        #print("UnicodeDecodeError Exception")
        return 
            
    return True

# function to scan directory name for Ubuntu-specifics
def dirname_scan(dir_path):
    return True



# function to scan directories for files 
def dir_scan(cwd): 
    # scan directory name for Ubuntu-specifics 
    dirname_scan(cwd)

    # get items in directory 
    dir_items = os.listdir(cwd)

    # remove ubuntu.db file
    if 'ubuntu.db' in dir_items: 
        dir_items.remove('ubuntu.db')

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
    global files
    # if singular file inputted (argv = 2), call scan_file
    if len(sys.argv) == 2:
        file_scan(str(sys.argv[1]))

    # if no inputted file (argv = 1), call scan_dir on current path
    elif len(sys.argv) == 1:
        # get the current working directory path and call scan_dir 
        cwd_path = os.getcwd()
        dir_scan(cwd_path) 

    # call usage if argv > 2 
    else:
        usage()
    
    print(files)


if __name__ == '__main__':
    # call main
    main()