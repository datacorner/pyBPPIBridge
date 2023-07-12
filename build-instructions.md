1) Build the requirements files
$ pip freeze > requirements.txt

2) build the wheel
(Modify setup.py accordindly)
$ python setup.py bdist_wheel

3) deploy / pyPI
twine upload --verbose dist/pyBPPIBridge-0.x.x-py3-none-any.whl
(may install twine via pip install twine)

**********************************
With TOML
**********************************
https://packaging.python.org/en/latest/tutorials/packaging-projects/

1) build the *.toml file
2) run python3 -m build
3) deploy / pyPI 
You will be prompted for a username and password. For the username, use __token__. For the password, use the token value, including the pypi- prefix.
    python3 -m twine upload --repository testpypi dist/*

Direct connection
    twine upload --verbose dist/pybppibridge-0.4.8.1-py3-none-any.whl