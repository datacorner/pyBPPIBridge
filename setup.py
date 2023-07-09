from setuptools import setup, find_packages
import os

# LAUNCH --> python setup.py bdist_wheel

setup(
    name = 'pyBPPIBridge', 
    version='0.4.4', 
    license = 'GPL V3',
    url = 'https://github.com/datacorner/pyBPPIBridge/wiki',
    download_url = 'https://github.com/datacorner/pyBPPIBridge',
    description = 'This solution builds a bridge between Blue Prism Process Intelligence (alias BPPI) and some external data sources (like files, databases via ODBC, SAP and Blue Prism).',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    data_files = [('dossier_config',['config-samples/bplogs.sql', 
                                     'config-samples/sqlite/config.ddl', 
                                     'config-samples/ini/config.ini-template'])],
    packages=find_packages(), 
)