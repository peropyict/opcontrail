import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
import json

from prompt_toolkit import prompt
import readline

from config.rest.IP_res import IPResManager
from config.rest.VN_res import VNResManager, VirtualNetworkManager
from config.ConfigHelper import HelperClass
from config.rest.RI_res import RIManager, RoutingInstance
from config.rest.RT_res import RTRestManager, RouteTargetManager


class RTCLI(object):
    def __init__(self, rt_uuid = ''):
        self.rt_uuid = rt_uuid
        
    def print_RTs(self):
        RTManager = RTRestManager()
        RTs = RTManager.getRTs()
        RThelper = HelperClass(RTs)

        readline.set_completer_delims("\n")
        readline.parse_and_bind("tab: complete")
        readline.set_completer(RThelper.complete)
        
        RT_name  = input("Search for a RT Name: ")
        #case1 "" print summary of all RTs
        #case2 "auto" print matching RTs
        #case3 "full name" (RT_uuid exists for the searched string) print RT details
        #case1
        if RT_name == '':
            self.print_RI_summary(RTs)
            return
        RT_uuid = RThelper.fqname_to_uuid(RT_name.split("."), "virtual-network")
        matchingRTs = []
        #case2
        if RT_uuid is None and len(str(RT_name)) > 0:
            matchingRTs = self.getAutoCompleteRTs(str(RT_name), RTs)
            self.printMatchingRTs(matchingRTs)
            return
        #case3
        self.printRTDetails(RT_uuid,RT_name)
    
    def getAutoCompleteRTs(self, completeval, RTs):
        matchingRTs = []
        for RT_id, RT_info in RTs.items():
            RT_name_string = '.'.join(RT_info["name"])        
            if completeval in RT_name_string:
                matchingRTs.append(RTs.get(RT_id))
        return matchingRTs



    def print_RI_summary(self, RIs):
        #
        for ri_id, ri_info in RIs.items():
            print("RI fqname: " + str(ri_info["name"]) + " .... uuid(" + str(ri_id) + ")")

    def printMatchingRTs(self, matchingRTs):
        RThelper = HelperClass({})
        for RT in matchingRTs:
            RT_uuid = RThelper.fqname_to_uuid(RT.get('name'), "route-target")
            self.printRTDetails(RT_uuid, RT.get('name'))

    

    def printRTDetails(self, RTuuid, RT_name):
        print("-----------------------------------------" )
        print("RT fqname: " + str(RT_name))
        print("RT UUID: " + str(RTuuid))
        RTManager = RTRestManager()
        RT_json = RTManager.getRT(RTuuid)
        RT_obj = RouteTargetManager(RT_json["route-target"])

        print("Routing instances: ")
        for RI in  RT_obj.RIs:
            print(str(RI["to"]))

        
    