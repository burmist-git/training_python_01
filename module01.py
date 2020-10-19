'''
Date        : Tue Oct 20 00:02:56 CEST 2020
Autor       : Leonid Burmistrov
Description : Simple reminder-training example
'''

import json
import os.path

def get_config_json(filename="./config.json"):
    '''
    Example to read json config file    
    '''
    config = json.load(open('config.json'))
    return config

def print_config(config):
    '''
    Print config
    '''
    print(type(config))
    print(config.keys())
    print(config["par1"])
    print(config["par2"])
    print(config["par3"])
    
def main():
    '''
    Definition of the main function (use for testing only)
    '''
    config = get_config_json()
    print_config(config)
    
if __name__ == "__main__":
    '''
    Run as main script (use for testing only)
    '''
    main()
