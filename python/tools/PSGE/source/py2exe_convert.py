'''
Run this in terminal python
python py2exe_convert.py py2exe --includes sip
'''


from py2exe.build_exe import py2exe
from distutils.core import setup
setup(console=["PSGE.py"])


