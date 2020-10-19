'''
Date        : Mon Oct 19 23:32:26 CEST 2020
Autor       : Leonid Burmistrov
Description : Simple reminder-training example.
'''

import os
import sys
#
import module01

if __name__ == "__main__":
    os.system('echo "\n 1) Info : --> test of the module01"')
    print(sys.modules['module01'])
    print(sys.modules['module01'].__file__)
    module01.main()
