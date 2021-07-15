#!/usr/bin/env python3

from csv import reader 

def read_csv(csv_file):
    # read csv file as a list of lists
    with open(csv_file, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)

    # close csv file 
    read_obj.close()
    
    # return list of the rows in the csv 
    return list_of_rows


def update_package_table(package_update):
    # establish connection with databse containing Ubuntu syntax 
    conn = sqlite3.connect('ubuntu.db')

    # set connection cursor 
    cur = conn.cursor()

    # delete current packages table 
    cur.execute('DROP TABLE packages')

    # create packages table 
    cur.execute("CREATE TABLE packages(id integer NOT NULL, package text NOT NULL, mariner_replacement text NOT NULL, notes text NOT NULL);")

    # iterate through each package_update entry and add to the table 
    for index, row in package_update:
        # note: each package_update row should be in the form: [package, mariner replacement, notes]
        cur.execute("INSERT INTO packages VALUES (" + index + "," + package_update[0] + "," + package_update[1] + "," package_update[2] + ")")

    # close database connection
    conn.close() 

    # return to main 
    return True 


def update_command_table(command_update):
    # establish connection with databse containing Ubuntu syntax 
    conn = sqlite3.connect('ubuntu.db')

    # set connection cursor 
    cur = conn.cursor()

    # delete current commands table 
    cur.execute('DROP TABLE commands')

    # create commands table 
    cur.execute("CREATE TABLE commands(id integer NOT NULL, command text NOT NULL, mariner_replacement text NOT NULL, notes text NOT NULL);")

    # iterate through each command_update entry and add to the table 
    for index, row in command_update:
        # note: each command_update row should be in the form: [command, mariner replacement, notes]
        cur.execute("INSERT INTO commands VALUES (" + index + "," + command_update[0] + "," + command_update[1] + "," command_update[2] + ")")

    # close database connection
    conn.close() 

    # return to main 
    return True 


def update_filepath_table(filepath_update):
    # establish connection with databse containing Ubuntu syntax 
    conn = sqlite3.connect('ubuntu.db')

    # set connection cursor 
    cur = conn.cursor()

    # delete current filepaths table 
    cur.execute('DROP TABLE commands')

    # create filepaths table 
    cur.execute("CREATE TABLE filepaths(id integer NOT NULL, filepath text NOT NULL, mariner_replacement text NOT NULL, notes text NOT NULL);")

    # iterate through each filepath_update entry and add to the table 
    for index, row in filepath_update:
        # note: each filepath_update row should be in the form: [filepath, mariner replacement, notes]
        cur.execute("INSERT INTO commands VALUES (" + index + "," + filepath_update[0] + "," + filepath_update[1] + "," filepath_update[2] + ")")

    # close database connection
    conn.close() 

    # return to main 
    return True 


def main():
    # set variable names 
    package_csv = 'packages.csv'
    command_csv = 'commands.csv'
    filepath_csv = 'filepaths.csv'

    # call csv reader and return list of lists of rows 
    package_update = read_csv(package_csv)
    command_update = read_csv(command_csv)
    filepath_update = read_csv(filepath_csv)

    # return 
    return True


if __name__ == '__main__':
    # call main
    main()  