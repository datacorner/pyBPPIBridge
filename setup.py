from setuptools import setup, find_packages
import os, sys

# LAUNCH --> python setup.py bdist_wheel
import pathlib
import pkg_resources

VERSION = "0.4.6"

DEPENDENCIES = [
'blinker==1.6.2',
'certifi==2023.5.7',
'charset-normalizer==3.1.0',
'click==8.1.3',
'colorama==0.4.6',
'contourpy==1.1.0',
'cvxopt==1.3.1',
'cycler==0.11.0',
'deprecation==2.1.0',
'Flask==2.3.2',
'fonttools==4.40.0',
'graphviz==0.20.1',
'idna==3.4',
'intervaltree==3.1.0',
'itsdangerous==2.1.2',
'Jinja2==3.1.2',
'kiwisolver==1.4.4',
'lxml==4.9.2',
'MarkupSafe==2.1.3',
'matplotlib==3.7.1',
'networkx==3.1',
'numpy==1.25.0',
'packaging==23.1',
'pandas==2.0.3',
'Pillow==9.5.0',
'pm4py==2.7.5',
'pydotplus==2.0.2',
'pyodbc==4.0.39',
'pyparsing==3.1.0',
'pyrfc==2.8.3',
'python-dateutil==2.8.2',
'pytz==2023.3',
'requests==2.31.0',
'scipy==1.11.1',
'six==1.16.0',
'sortedcontainers==2.4.0',
'StringDist==1.0.9',
'tqdm==4.65.0',
'tzdata==2023.3',
'urllib3==2.0.3',
'Werkzeug==2.3.6',
]

setup(
    name = 'pyBPPIBridge', 
    version=VERSION, 
    license = 'GPL V3',
    url = 'https://github.com/datacorner/pyBPPIBridge/wiki',
    download_url = 'https://github.com/datacorner/pyBPPIBridge',
    description = 'This solution builds a bridge between Blue Prism Process Intelligence (alias BPPI) and some external data sources (like files, databases via ODBC, SAP and Blue Prism).',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    data_files = [('dossier_config',['config-samples/bplogs.sql', 
                                     'config-samples/sqlite/config.ddl', 
                                     'config-samples/ini/config.ini-template'])],
    packages=find_packages(),
    install_requires=DEPENDENCIES,
)