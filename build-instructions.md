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
1) build the *.toml file
2) run python3 -m build
3) deploy / pyPI 
    python3 -m twine upload --repository testpypi dist/*