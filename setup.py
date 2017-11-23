from distutils.core import setup
import py2exe

setup(console=['elevator.py'],    options = {'py2exe': {'bundle_files': 0}})
