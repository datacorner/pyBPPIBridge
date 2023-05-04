# Introduction
This repository proposes a Python program that makes a bridge between Blue Prism Process Intelligence (alias BPPI) and external data sources. Its purpose is to access these external datasources, collect them ant automate their importation into a BPPI instance (cloud or on-prem). BPPI is the solution provided by Blue Prism for Process and Task Mining and is a ABBYY Timeline OEM provided by Blue Prism. But when it is about Process Mining it necessary about data as this kind of solutions needs their oil to work properly.  

# Requirements (Python)
Python 3.10.x minimum
Each Python sub projects has its own requirements.txt file available, to install the needed package just execute:
```
pip install -r requirements.txt
```

# Project description 
The BPPI Repository Python API Wrapper ! 
This project contains the API wrapper for Python which enables to load data directly into BPPI by using the Native BPPI Repository (and to do features)
* Load a file (CSV) directly into a repository
* Load a SQL Server Query (by using pyODBC)
* Load the Blue Prism logs data from the Blue Prism Repository
All of these loads also offer the posibility to execute one or several BPPI To do (to directly load the data into a project) 
## Requirements:
* Python 3.10.x mminimum
* Python library: time, requests, json, urllib, logging, pyODBC
* To use this API it's mandatory to configure correctly the BPPI repository first (Cf. Data Sources / DBMS CLI tool configuration). Cf. https://help.abbyy.com/en-us/timeline/5/user_guide/connectingtodbmsdatasource/
## CLI Arguments
### Load from a CSV file
Program name loadcsv.py  
* **-filename** file to load (CSV format)
* **-token** Token (provided while configuring BPPI datasource)
* **-url** Server URL (without last slash)
#### Example
Launch the program in the shell (windows or linux) command line like this:
```
$ python3 bppibridge.py -sourcetype csv -filename {InternationalDeclarations.csv} -token {token} -url {BPPI Server URL}
```
### Load from an SQL Server Query (via ODBC)
Program name loadsql.py  
* **-query** Query to execute to get the data
* **-token** BPPI Token from the CLI configuration screen
* **-url** BPPI http URL server
* **-connectionstring** ODBC Connection String
* **-configfile** Config file with all configuration details (INI format, see the template below)
if a file is specified for the -configfile parameter the parameter file must follow the INI format rules. Example/Template -> see the [config.ini-template](https://github.com/datacorner/pyProcessMiningTools/blob/main/pyBPPIAPI/config.ini-template)  (rename it as an *.ini file)
#### Example
Launch the program in the shell (windows or linux) command line like this:
```
$ python3 bppibridge.py -sourcetype odbc -configfile {config.ini}
```
**ODBC Connection String example:** DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=***;UID=***;PWD=***;ENCRYPT=No
### Load from a Blue Prism Repository (from 7.x)  
Program name loadbp.py  
* **-configfile** Config file with all configuration details (INI format) / must follow the INI format rules. Example/Template -> See the [config.ini-template](https://github.com/datacorner/pyProcessMiningTools/blob/main/pyBPPIAPI/config.ini-template) (rename it as an *.ini file)*
Capabilities:
* Can connect directly to the Blue Prism Repository by using an ODBC Connection String
* Gather logs from a selected Blue Prism process (use the processname parameter)
* Collect only the Blue Prism variable from the list (parameters parameter in the ini file)
* Filter out/remove these stagetype (use the stagetypefilters ini parameter an list all the stages types code not desired)
* Include or not the VBO logs (use the includevbo option)
* Support Unicode (use the unicode option)
* Can gather Blue Prism logs data beteween 2 dates (use the command line todate and/or fromdate). By this way it's possible to manage full or delta load
#### Example
Launch the program in the shell (windows or linux) command line like this:
```
$ python3 bppibridge.py -sourcetype blueprism -configfile {config.ini} [-fromdate YYYY-MM-DD HH:MM:SS] [-todate YYYY-MM-DD HH:MM:SS]
```