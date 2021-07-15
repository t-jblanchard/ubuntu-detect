## Ubuntu Detection Tool


## Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)
* [Updates](#updates)

## General Info
Tool to scan a codebase, directory, or file for a list of common Ubuntu-specific packages, commands, and filepaths. The scanned for items are located in **database/packages.csv**, **database/commands.csv**, and **database/filepaths.csv**. 

## Technologies
Project is created with:
* Python3
* SQLite Database  
	
## Setup
Clone script and database:
```
$ git clone https://github.com/t-jblanchard/ubuntu-detect.git
```

## Usage 
To ensure latest update of script run:
```
$ git pull
```
To run script on entire codebase:  
```
$ ./detect.py [path to codebase]
```
To run script on specific file:
```
$ git clone https://github.com/t-jblanchard/ubuntu-detect.git
$ ./detect.py [full filepath]
```

## Updates
1. Clone script and database:
```
$ git clone https://github.com/t-jblanchard/ubuntu-detect.git
```
2. Update packages.csv, commands.csv, or filepaths.csv with the following format: 
	**ubuntu package/command/filepath, mariner replacement, notes**
3. Update SQLite database (ubuntu.db) but running:
```
$ ./csv_reader.py
```
4. Push changes to repo:
```
$ git push -u origin main
```
