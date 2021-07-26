# Ubuntu Detection Tool

## Table of Contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)
* [Sample I/O](#sample-io)
* [Updates](#updates)

## General Info
A tool to scan a codebase, directory, or file for a list of common Ubuntu-specific packages, commands, and file/directory paths. The tool aims to speed up the codebase reconfiguration process and assist in planning of time and resources when migrating from Ubuntu to Mariner. When using the tool, keep in mind that the scanned for instances are not 100% comprehensive, and all suggested Mariner replacements won't be universally applicable. 

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

To ensure latest update of script run:
```
$ git pull
```
To see usage information:  
```
$ ./detect.py usage
```
To run script on entire codebase:  
```
$ ./detect.py [full codebase path]
```
To run script on specific file or directory:
```
$ ./detect.py [full path]
```
Output Format:
* **package_data.csv**: packages hardcoded into files in codebase  
```
[full filepath],[list of line numbers],[Ubuntu package],[Mariner counterpart (if applicable)],[notes]
```
* **command_data.csv**: commands hardcoded into files in codebase  
```
[full filepath],[list of line numbers],[Ubuntu command],[Mariner counterpart (if applicable)],[notes]
```
* **filepath_inline_data.csv**: paths hardcoded into files in codebase  
```
[full filepath],[list of line numbers],[Ubuntu path],[Mariner counterpart (if applicable)],[notes]
```
* **filepath_data.csv**: directory/filepaths in codebase  
```
[full path],[Ubuntu relative path],[Mariner counterpart (if applicable)],[notes]
```

## Sample I/O
Input: 
```
$ git clone https://github.com/t-jblanchard/ubuntu-detect.git
$ ./detect.py ~/codebase
```
Output (into top-level of ubuntu-detect):
```
command_data.csv    package_data.csv    filepath_data.csv    filepath_inline_data.csv
```

## Updates
_Note: Instructions are for on a machine, but updates can also be done directly on GitHub_
1. Clone repository onto machine:
```
$ git clone https://github.com/t-jblanchard/ubuntu-detect.git
```
2. Update packages.csv, commands.csv, or filepaths.csv with the following format (delimeter: ','):  
	**[ubuntu package/command/filepath],[mariner replacement],[notes]**

3. Push changes to repo:
```
$ git push -u origin main
```
