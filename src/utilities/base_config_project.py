# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from os.path import dirname, abspath
from sys import path

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from config import is_console_debug


path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
if is_console_debug:
    print(f'Working folder: {dirname(dirname(dirname(abspath(__file__))))}')
