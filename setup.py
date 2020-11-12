# -*- coding: utf-8 -*-
"""
Program: setup.py
Created on 11/12/2020
@author: adhamlin

This file(setup.py) and the MANIFEST.in file describe the project and the files that belong to it.
setup.py and the MANIFEST.in file are completed, Use pip to install the project in a virtual environment.
Command to install: $ 'pip install -e .'   <-- Note the space and the period, means install in this active environment
Once install you can see the project is now installed with: 'pip list'
and call the app from any directory with the env active at your prompt:
Run your Application:
    windows - at the powershell prompt> '$env:FLASK_APP = "flaskr"'
    windows - at the powershell prompt> '$env:FLASK_ENV = "development"'
    windows - at the powershell prompt> 'flask run'
    ----------------------------------------------
    windows - at the cmd prompt> 'set FLASK_APP=flaskr'
    windows - at the cmd prompt> 'set FLASK_ENV=development'
    windows - at the cmd prompt> 'flask run'
    ----------------------------------------------
    linux/mac - at the terminal> 'export FLASK_APP=flaskr'
    linux/mac - at the terminal> 'export FLASK_ENV=development'
    linux/mac - at the terminal> 'flask run'
"""
# imports
from setuptools import find_packages
from setuptools import setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),  # find package directories automatically and the py files to include
    include_package_data=True,  # include other data/files (specified in the 'MANIFEST.in' file)
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
