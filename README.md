# Presentation
![BPPI Data Bridge principle](https://raw.githubusercontent.com/wiki/datacorner/pyBPPIBridge/img/schema.png)
This repository proposes a solution that build a data bridge between Blue Prism Process Intelligence (BPPI) and one or several external data sources. Its purpose is first to access these external datasources. Then its collect the needed data to automate their importation into an existing BPPI instance (cloud or on-prem). By executing a TO DO into the BPPI repository it also performs an automatic import to an existing BPPI Project.

🚀 Currently this Data Bridge provides data access and load from these data sources :

✅  [External file (csv)](https://github.com/datacorner/pyBPPIBridge/wiki/CSV-File)
✅  [External Excel Spreadsheet (xls, xlsx, xlsm, xlsb, odf, ods and odt)](https://github.com/datacorner/pyBPPIBridge/wiki/Excel-File)
✅  [External XES File](https://github.com/datacorner/pyBPPIBridge/wiki/XES-File)
✅  [ODBC Data Sources (checked with SQL Server) by using an configurable SQL query](https://github.com/datacorner/pyBPPIBridge/wiki/ODBC)
✅  [Blue Prism (Via session logs, Blue Prism API or vbo uses)](https://github.com/datacorner/pyBPPIBridge/wiki/Blue-Prism)
✅  [SAP Read Table via SAP RFC](https://github.com/datacorner/pyBPPIBridge/wiki/SAP-RFC-Table)

This BPPI Data Bridge reads the data from the Datasource and upload them into the BPPI Repository. Inside BPPI it's also possible to configure a TODO to automate some transformations and load the data into a BPPI Project (The program can execute thess To Do automatically). To make this bridge usable the user must configure a Data Source in the BPPI Repository, and get a token.  

*✨ Note: BPPI (Blue Prism Process Intelligence) is the solution provided by Blue Prism for Process and Task Mining (ABBYY Timeline OEM)*

👉 [Look at the wiki for more informations](https://github.com/datacorner/pyBPPIBridge/wiki)

👉 [Add a new issue](https://github.com/datacorner/pyBPPIBridge/issues)

👉 [Install the BPPI Bridge via pyPI](https://pypi.org/project/pyBPPIBridge/)

