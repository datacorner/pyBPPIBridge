# Presentation
![BPPI Bridge principle](./schema.png)
This repository proposes a Python program that makes a bridge between Blue Prism Process Intelligence (alias BPPI) and external data sources. Its purpose is to access these external datasources, collect them ant automate their importation into a BPPI instance (cloud or on-prem). By executing a TO DO into the BPPI repository it also enables to performs BPPI transformations and load directly in one or several projects.  
Currently this bridge can access and load data from
* External file (csv)
* External Excel Spreadsheet (xls, xlsx, xlsm, xlsb, odf, ods and odt)
* External XES File
* ODBC Data Sources (checked with SQL Server) by using an configurable SQL query
* Blue Prism repository (Can gather all the session logs for a specified process)   
* SAP Read Table via SAP RFC

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
* For the SAP connectivity. The RFC SDK (NWRFCSDK) must be installed and the [pyrfc package](https://sap.github.io/PyRFC) deployed as well.
* The configuration file [config.ini-template](https://github.com/datacorner/pyBPPIBridge/blob/main/config.ini-template) is mandatory for ODBC and Blue Prism Connection. When the data source is a CSV file all needed parameters are passed through the command line.

# Usage 
This project leverages the BPPI API and loads data directly into the BPPI Repository. Using this bridge is pretty easy as you just have to launch a command line (CLI).

### Load from a CSV file
#### CLI 
* **-sourcetype** (Mandatory) csv
* **-configfile** (Mandatory) Config file with all configuration details (INI format, see the template below)
if a file is specified for the -configfile parameter the parameter file must follow the INI format rules. Example/Template -> see the [config.ini-template](https://github.com/datacorner/pyBPPIBridge/blob/main/config.ini-template)  (rename it as an *.ini file)
* **-filename** (Mandatory) file to load (CSV format)
* **-sep** (Optional/Comma by default) Fields separator
#### Capabilities
* Read the CSV file and load it into the BPPI Repository
* Manages other delimiter (field separators), by default comma.
#### Example
Launch the program in the shell (windows or linux) command line like this:
```
$ python3 bppibridge.py -sourcetype csv -filename {myfile.csv} -configfile {config.ini}
```

### Load from a XES file
#### CLI 
* **-sourcetype** (Mandatory) xes
* **-configfile** (Mandatory) Config file with all configuration details (INI format, see the template below)
if a file is specified for the -configfile parameter the parameter file must follow the INI format rules. Example/Template -> see the [config.ini-template](https://github.com/datacorner/pyBPPIBridge/blob/main/config.ini-template)  (rename it as an *.ini file)
* **-filename** (Mandatory) file to load (XES format)
#### Capabilities
* Read the XES file and load it into the BPPI Repository
* Manages other delimiter (field separators), by default comma.
#### Example
Launch the program in the shell (windows or linux) command line like this:
```
$ python3 bppibridge.py -sourcetype xes -filename {myfile.xes} -configfile {config.ini}
```

### Load from an Excel file
Excel files supported: xls, xlsx, xlsm, xlsb, odf, ods and odt
#### CLI
* **-sourcetype** (Mandatory) excel
* **-configfile** (Mandatory) Config file with all configuration details (INI format, see the template below) if a file is specified for the -configfile parameter the parameter file must follow the INI format rules. Example/Template -> see the [config.ini-template](https://github.com/datacorner/pyBPPIBridge/blob/main/config.ini-template)  (rename it as an *.ini file)
* **-filename** (Mandatory) file to load (CSV format)
* **-sheet** [Optional] Sheet nema (by default takes the first one
#### Capabilities
* Read an excel spreadsheet and load it into the BPPI Repository
* It's possible to choose the sheet to load (by default it takes the first one)
#### Example
Launch the program in the shell (windows or linux) command line like this:
```
$ python3 bppibridge.py -sourcetype excel -filename {myfile.xslx} -configfile {config.ini} 
```

### Load from an ODBC Data Source
#### CLI
* **-sourcetype** (Mandatory) odbc
* **-configfile** (Mandatory) Config file with all configuration details (INI format, see the template below) if a file is specified for the -configfile parameter the parameter file must follow the INI format rules. Example/Template -> see the [config.ini-template](https://github.com/datacorner/pyBPPIBridge/blob/main/config.ini-template)  (rename it as an *.ini file)
#### Capabilities
* Get Data from an ODBC Data Source and load it into the BPPI Repository
#### Example
Launch the program in the shell (windows or linux) command line like this:
```
$ python3 bppibridge.py -sourcetype odbc -configfile {config.ini}
```
**ODBC Connection String example:** DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=***;UID=***;PWD=***;ENCRYPT=No

### Load from a Blue Prism Repository (from 7.x)  
#### CLI
* **-sourcetype** (Mandatory) blueprism
* **-configfile** (Mandatory) Config file with all configuration details (INI format) / must follow the INI format rules. Example/Template -> See the [config.ini-template](https://github.com/datacorner/pyBPPIBridge/blob/main/config.ini-template) (rename it as an *.ini file)*
* **-fromdate** [Optional] From Date filtering (Delta load) (Format expected YYYY-MM-DD HH:MM:SS)
* **-todate** [Optional] To Date filtering (Delta load) (Format expected YYYY-MM-DD HH:MM:SS)
#### Capabilities
* Can connect directly to the Blue Prism Repository by using an ODBC Connection String (on the BP Repository SQL Server / Read only the log tables)
* Gather logs from a selected Blue Prism process (use the processname parameter)
* Collect only the Blue Prism variable from the list (parameters parameter in the ini file)
* Include or not the VBO logs (use the includevbo option). By including the VBOs activities it's possible to have a full view of the Process Execution.
* Support BP Unicode or BP Non-Unicode Logs (use the unicode option)
* Can gather Blue Prism logs data between 2 dates (use the command line todate and/or fromdate). 
* Support Delta or Full load (use the delta option).
* Filter out/remove the selected stage types (For that, just use the stagetypefilters ini parameter an list all the stages types code not desired)
* Can exclude all the Start and End stages except the First & Last one in the BP parent process (the ones in the Main Page). By this way it removes Starts and Ends potential duplicates (which exists on each pages & VBOs)
#### Example
Launch the program in the shell (windows or linux) command line like this:
```
$ python3 bppibridge.py -sourcetype blueprism -configfile {config.ini} [-fromdate YYYY-MM-DD HH:MM:SS] [-todate YYYY-MM-DD HH:MM:SS]
```

### Load from SAP Table (via RFC)
* **-sourcetype** (Mandatory) saptable
* **-configfile** (Mandatory) Config file with all configuration details (INI format, see the template below) if a file is specified for the -configfile parameter the parameter file must follow the INI format rules. Example/Template -> see the [config.ini-template](https://github.com/datacorner/pyBPPIBridge/blob/main/config.ini-template)  (rename it as an *.ini file)
#### Capabilities
* Get Data from a SAP Table (leverage the RFC_READ_TABLE BAPI)
#### Example
Launch the program in the shell (windows or linux) command line like this:
```
$ python3 bppibridge.py -sourcetype saptable -configfile {config.ini}
```
More come soon :-)
