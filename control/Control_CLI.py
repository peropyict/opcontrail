#! /usr/bin/env python

# Author        : Slobodan Blatnjak <blatnjak@gmail.com>
# Platform      : Contrail 19xx
version = '1'
# Date          : 2020-9-29

# This script provides a demo for some junos friendly commands to list and retrieve contrail object details at config, control and agent level.

import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
import json
#import VN_res
#from tabCompletion import Tabcomplete
from prompt_toolkit import prompt
import readline

import pdb

'''from control.rest.IP_res import IPResManager
from control.rest.VN_res import VNResManager
from control.ControlHelper import helperClass
from control.rest.RI_res import RIManager'''

from config.rest.control.bgp import BGP #move bgp.py file


class BGPCLI(object):
    def __init__(self):
        VN_UUID = ''

    def print_bgp_neighboors(self):
        bgp = BGP()
        bgp.SnhShowBgpNeighborConfigReq() 
        

