#!/bin/bash

########################################################################
#                                                                      #
# Copyright(C) 2020 - LBS - (Single person developer.)                 #
# Tue Oct 20 22:17:39 CEST 2020                                        #
# Autor: Leonid Burmistrov                                             #
#                                                                      #
# File description:                                                    #
#                                                                      #
# Input paramete:                                                      #
#                                                                      #
# This software is provided "as is" without any warranty.              #
#                                                                      #
########################################################################

function clean_sh {
    rm -rf *~ build dist trainingpython.egg-info __pycache__
}

function printHelp {
    echo " --> ERROR in input arguments "
    echo " -d  : default"
    echo " -p2 : second parameter"
}

if [ $# -eq 0 ]; then
    printHelp
else
    if [ "$1" = "-d" ]; then
            clean_sh
    elif [ "$1" = "-p2" ]; then
	echo " $1 "
    else
        printHelp
    fi
fi
