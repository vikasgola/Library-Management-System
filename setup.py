from setuptools import setup
from codecs import open
from os import path
import subprocess
from setuptools.command.test import test

setup(name='Library Management System',
      version='0.1.0',
      description='Library management system for IIT Jammu',
      author='Vikas Gola',
      author_email='vikasgola2015@gmail.com',
      python_requires = '>=3.6',
      packages=['Library_Management_System', 'Library_Management_System/helper','Library_Management_System/gui','Library_Management_System/database', 'Library_Management_System/datagenerator'],
      scripts = ["Library_Management_System/scripts/LibMSsetup" , "Library_Management_System/scripts/LibMS"],
      install_requires = ["pymysql==0.9.3", "PyQT5==5.9.2", "pandas==0.24.1", "mimesis==3.0.0"]
     )