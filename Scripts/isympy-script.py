#!c:\users\sheveksmath\documents\programming\pb2\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'sympy==1.3','console_scripts','isympy'
__requires__ = 'sympy==1.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('sympy==1.3', 'console_scripts', 'isympy')()
    )
