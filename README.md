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

[Look at the wiki for more informations](https://github.com/datacorner/pyBPPIBridge/wiki)
