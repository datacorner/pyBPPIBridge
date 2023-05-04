# Introduction
This repository proposes a Python program that makes a bridge between Blue Prism Process Intelligence (alias BPPI) and external data sources. Its purpose is to access these external datasources, collect them ant automate their importation into a BPPI instance (cloud or on-prem). Currently this bridge can access to
* External file (CSV)
* ODBC Data Sources (checked with SQL Server) by using an configurable SQL query
* Blue Prism repository (Can gather all the session logs for a specified process)  

This bridge reads the data from the Datasource and upload them into the BPPI Repository. Inside BPPI it's also possible to configure a TODO to automate some transformations and load the data into a BPPI Project (The program can execute thess To Do automatically). To make this bridge usable the user must configure a Data Source in the BPPI Repository, and get a token.  

Note: BPPI is the solution provided by Blue Prism for Process and Task Mining (ABBYY Timeline OEM).

# Requirements (Python)
* [Python 3.10.x minimum](https://www.python.org/downloads/release/python-3100)
* Python library: Several Python packages are necessary, to install them just execute the command below
```
pip install -r requirements.txt
```
* To use this API it's mandatory to configure correctly the BPPI repository first (Cf. Data Sources / DBMS CLI tool configuration). Cf. https://help.abbyy.com/en-us/timeline/6/user_guide/connectingtodbmsdatasource/
* for the ODBC Connectivity and Blue Prism Connectivity an ODBC Connection string and a User/password is necessary to query the data base. Only Read access to the expected tables are mandatory. 
* For the Blue Prism Connectivity, the read only access is required for these Tables:
  * BPASession
  * BPAResource 
  * BPASessionLog_NonUnicode or BPASessionLog_Unicode
* The configuration file [config.ini-template](https://github.com/datacorner/pyBPPIBridge/blob/main/config.ini-template) is mandatory for ODBC and Blue Prism Connection. When the data source is a CSV file all needed parameters are passed through the command line.

# Usage 
This project leverages the BPPI API and loads data directly into BPPI. Using this bridge is pretty easy as you just have to launch a command line (CLI).
### Load from a CSV file
#### CLI 
* **-filename** (Mandatory) file to load (CSV format)
* **-token** (Mandatory) Token (provided while configuring BPPI datasource)
* **-url** (Mandatory) Server URL (without last slash)
* **-other.logfilename** [Optional] Log filename and path
#### Example
Launch the program in the shell (windows or linux) command line like this:
```
$ python3 bppibridge.py -sourcetype csv -filename {myfile.csv} -token {token} -url {BPPI Server URL} [-other.logfilename filenameandpath] 
```
### Load from an SQL Server Query (via ODBC)
#### CLI 
* **-configfile** (Mandatory) Config file with all configuration details (INI format, see the template below)
if a file is specified for the -configfile parameter the parameter file must follow the INI format rules. Example/Template -> see the [config.ini-template](https://github.com/datacorner/pyBPPIBridge/blob/main/config.ini-template)  (rename it as an *.ini file)
#### Example
Launch the program in the shell (windows or linux) command line like this:
```
$ python3 bppibridge.py -sourcetype odbc -configfile {config.ini}
```
**ODBC Connection String example:** DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=***;UID=***;PWD=***;ENCRYPT=No

### Load from a Blue Prism Repository (from 7.x)  
#### CLI 
* **-configfile** (Mandatory) Config file with all configuration details (INI format) / must follow the INI format rules. Example/Template -> See the [config.ini-template](https://github.com/datacorner/pyBPPIBridge/blob/main/config.ini-template) (rename it as an *.ini file)*
* **-fromdate** [Optional] From Date filtering (Delta load) (Format expected YYYY-MM-DD HH:MM:SS)
* **-todate** [Optional] To Date filtering (Delta load) (Format expected YYYY-MM-DD HH:MM:SS)
#### Capabilities
* Can connect directly to the Blue Prism Repository by using an ODBC Connection String
* Gather logs from a selected Blue Prism process (use the processname parameter)
* Collect only the Blue Prism variable from the list (parameters parameter in the ini file)
* Filter out/remove these stagetype (use the stagetypefilters ini parameter an list all the stages types code not desired)
* Include or not the VBO logs (use the includevbo option)
* Support Unicode (use the unicode option)
* Can gather Blue Prism logs data beteween 2 dates (use the command line todate and/or fromdate). By this way it's possible to manage full or delta load
* Can exclude all the Start and End stages except the First & Last one in the BP parent process (the ones in the Main Page)
#### Example
Launch the program in the shell (windows or linux) command line like this:
```
$ python3 bppibridge.py -sourcetype blueprism -configfile {config.ini} [-fromdate YYYY-MM-DD HH:MM:SS] [-todate YYYY-MM-DD HH:MM:SS]
```
