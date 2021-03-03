#! /usr/bin/env python

# Author        : Slobodan Blatnjak <blatnjak@gmail.com>
# Platform      : Contrail 19xx
version = '1'
# Date          : 2021-02-29

# This script provides some junos friendly commands to list and retrieve contrail object details at config, control and agent level.

import json
#import VN_res
from prompt_toolkit import prompt
import readline

import argparse


import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from config.rest.IP_res import IPResManager
from config.ConfigHelper import HelperClass


class IPCLI(object):
    def __init__(self):
        #IP_UUID = ''
        self.IPManager = IPResManager()
        self.IPs = self.IPManager.getIPs()
        self.IPhelper = HelperClass(self.IPs, search_object_by='address')
    
    def print_IPs(self):
        
        #search/filter, get search_result_list from total IPs list
        print_all = self.IP_search_helper()
        #get/print IP details for IPs in the search result list

        #TODO fix a bug (print only selected ones)
        if print_all:
            for key, val in self.IPs.items():
                IP = self.IPManager.getIPDetails(key)
                self.print_IP_detail(IP)
        else:
            for key, val in self.IPs.items():
                if val['address'] in self.IPhelper.search_result_list:
                    IP = self.IPManager.getIPDetails(key)
                    self.print_IP_detail(IP)
            
     
    def IP_search_helper(self):
        readline.set_completer_delims("\n")
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.IPhelper.complete)
        self.IPhelper.search_result_list = []
        IP_address  = input("IP address: ")
        if len(IP_address) > len(self.IPhelper.last_search_text): #search text changed + enter -> we have to remove all non matching items from search_result_list
            for search_result_list_item in self.IPhelper.search_result_list:
                if IP_address not in search_result_list_item:
                    self.IPhelper.search_result_list.remove(search_result_list_item)
        if len(IP_address) > 0:
            print("search result list for '" + IP_address + "': " + str(self.IPhelper.search_result_list)) 
        else:
            print('List all IPs....') 
        
        #return search_all=True if no single char is used for search
        return True if len(IP_address) == 0  else  False

    def print_IP_summary(self, IP):
        
        for key in IP:
            print("IP uuid: " , str(key))
            print("IP address: " , str(key))
            for item in IP[key]:
                print(item, '->', str(IP[key][item]))

    def print_IP_detail(self, IP):
        print("-----------------------------------------" )
        for key in IP:
            print("IP uuid: " , str(key))
            for item in IP[key]:
                print(item, '->', str(IP[key][item]))
            

    

