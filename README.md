# Atlas

## Table of Contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)
* [Data Output](#data-output)
* [Sample I/O](#sample-io)
* [Warnings](#warnings)
* [Custom Data](#custom-data)
* [Admin Updates](#admin-updates)

## General Info
[Overview Page](eng.ms/Mariner)  

A tool to scan a codebase, directory, or file for a list of common Ubuntu-specific packages, commands, and file/directory paths. The tool aims to speed up the codebase reconfiguration process and assist in planning of time and resources when migrating from Ubuntu to Mariner.

## Technologies
Project is created with:
* Python3  
	
## Setup
Clone repository onto machine outside of codebase/desired directory:
```
$ git clone https://github.com/t-jblanchard/ubuntu-detect.git
```

## Usage 
_Note: Always run in top-level of ubuntu-detect directory_  

1. To ensure latest update of script run:
```
$ git pull
```
2. To see usage information:  
```
$ ./detect.py usage
```
3. To run script on entire codebase:  
```
$ ./detect.py [full codebase path]
```
4. To run script on specific file or directory:
```
$ ./detect.py [full path]
```
5. After running the tool, visit the [References](), for more detailed information about your outputted data. 
## Data Output
Output Format in ubuntu-detect/data-output:
* **flagged_files.csv**: compiled list of anyfile in the codebase/directory that gets flagged with Ubuntu-specific syntax 
```
[full filepath]
```
* **packages.csv**: packages hardcoded into files in codebase  
```
[full filepath],[list of line numbers],[Ubuntu package],[Mariner counterpart (if applicable)],[notes]
```
* **commands.csv**: commands hardcoded into files in codebase  
```
[full filepath],[list of line numbers],[Ubuntu command],[Mariner counterpart (if applicable)],[notes]
```
* **filepaths.csv**: directory/filepaths in codebase  
```
[full path],[Ubuntu relative path],[Mariner counterpart (if applicable)],[notes]
```
* **filepaths_inline.csv**: paths hardcoded into files in codebase  
```
[full filepath],[list of line numbers],[Ubuntu path],[Mariner counterpart (if applicable)],[notes]
```

## Sample I/O
Input: 
```
$ git clone https://github.com/t-jblanchard/ubuntu-detect.git
$ ./detect.py ~/codebase
```
Output (into ubuntu-detect/data-output):
```
flagged_files.csv    packages.csv    commands.csv    filepaths.csv    filepaths_inline.csv
```

## Warnings 
* When using the tool, keep in mind that the scanned for instances are not 100% comprehensive, and all suggested Mariner replacements won't be universally applicable. 
* Some files that are you've pulled in from open-source may get flagged, so it is important to evaluate the data with that in mind. 

## Custom Data
If you know your service well, and have specific instances in mind you would like the tool to scan for the .csv files in /ubuntu-detect/database can be customized. Use the following format to edit packages.csv, commands.csv, or filepaths.csv with the following format (delimeter: ','):  
```
[ubuntu package/command/filepath],[mariner replacement],[notes]
```

## Admin Updates
_Note: Instructions are for on a machine, but updates can also be done directly on GitHub_
1. Clone repository onto machine:
```
$ git clone https://github.com/t-jblanchard/ubuntu-detect.git
```
2. Update packages.csv, commands.csv, or filepaths.csv with the following format (delimeter: ','):  
```
[ubuntu package/command/filepath],[mariner replacement],[notes]
```
3. Push changes to repo:
```
$ git push -u origin main
```
