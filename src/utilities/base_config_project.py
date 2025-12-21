# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from os.path import dirname, abspath
from sys import path


path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
