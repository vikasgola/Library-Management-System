from setuptools import setup
from codecs import open
from os import path
import subprocess
from setuptools.command.test import test

class setupTestRequirements(test, object):
    def run_script(self):
        cmd = ['bash', 'scripts/Library_Management_System']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        ret = p.communicate()
        print(ret[0])

    def run(self):
        self.run_script()
        super(setupTestRequirements, self).run()

setup(name='Library Management System',
      version='0.1.0',
      description='Library management system for IIT Jammu',
      author='Vikas Gola',
      author_email='vikasgola2015@gmail.com',
      python_requires = '>=3.6',
      packages=['Library_Management_System'],
      scripts = ["scripts/Library_Management_System"],
      install_requires = ["pymysql==0.9.3", "PyQT5==5.9.2", "pandas==0.24.1", "mimesis==3.0.0"],
      cmdclass={'test': setupTestRequirements}
     )