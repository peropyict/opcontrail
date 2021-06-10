import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
import json
#import VN_res
#from tabCompletion import Tabcomplete
from prompt_toolkit import prompt
import readline

from config.rest.IP_res import IPResManager
from config.rest.VN_res import VNResManager, VirtualNetworkManager
from config.ConfigHelper import HelperClass
from config.rest.RI_res import RIManager, RoutingInstance
from config.rest.VMI_rest import VMRestManager,VirtualMachineInterface


class VNCLI(object):
    def __init__(self, vn_uuid = ''):
        self.vn_uuid = vn_uuid
        #test
        #test
    def print_VNs(self):
        VNManager = VNResManager()
        #VMRestManager = VMRestManager()
        VNs = VNManager.VNs
        VNhelper = HelperClass(VNs)

        readline.set_completer_delims("\n")
        readline.parse_and_bind("tab: complete")
        readline.set_completer(VNhelper.complete)
        
        VN_name  = input("Search for a VN Name: ")
        #case1 "" print summary of all VNs
        #case2 "auto" print matching VNs
        #case3 "full name" (VN_uuid exists for the searched string) print VN details
        #case1
        if VN_name == '':
            self.print_VN_summary(VNs)
            return
        VN_uuid = VNhelper.fqname_to_uuid(VN_name.split("."), "virtual-network")
        matchingVNs = []
        #case2
        if VN_uuid is None and len(str(VN_name)) > 0:
            matchingVNs = self.getAutoCompleteVNs(str(VN_name), VNs)
            self.printMatchingVNs(matchingVNs)
            return
        #case3
        self.printVNDetails(VN_uuid,VN_name)
    
    def getAutoCompleteVNs(self, completeval, VNs):
        matchingVNs = []
        for vn_id, vn_info in VNs.items():
            vn_name_string = '.'.join(vn_info["name"])        
            if completeval in vn_name_string:
                matchingVNs.append(VNs.get(vn_id))
        return matchingVNs

    def getVNIPs(self, VN_obj):
        ipManager = IPResManager()
        IPs_dict = {}
        #for instance_ip_back_ref in VN_obj["instance_ip_back_refs"]:
        for instance_ip_back_ref in VN_obj.IIP:
            IP_obj = ipManager.getIP(instance_ip_back_ref["uuid"])
            IPs_dict[instance_ip_back_ref["uuid"]] = {"IP_obj": IP_obj}
        return IPs_dict

    def print_VN_summary(self, VNs):
        #
        for vn_id, vn_info in VNs.items():
            print("VN fqname: " + str(vn_info["name"]) + " .... uuid(" + str(vn_id) + ")")

    def printMatchingVNs(self, matchingVNs):
        VNhelper = HelperClass({})
        for VN in matchingVNs:
            VN_uuid = VNhelper.fqname_to_uuid(VN.get('name'), "virtual-network")
            self.printVNDetails(VN_uuid, VN.get('name'))

    def printVNDetails(self, VNuuid, VN_name):
        print("-----------------------------------------" )
        print("VN fqname: " + str(VN_name))
        print("VN UUID: " + str(VNuuid))
        VNManager = VNResManager()
        VN_json = VNManager.getVN(VNuuid)
        VN_obj = VirtualNetworkManager(VN_json["virtual-network"])

        print("Route Targets: ---" )
        print("import route targets: " + str(VN_obj.RT_import))
        print("export route_targets: " + str(VN_obj.RT_export))

        #review RIuuid (why the list in API schema)
        RI = RoutingInstance(VN_obj.RI[0]["uuid"])
        #TODO VN_obj.RI is a list, in what cases we have more RIs?

        #__link_local__ doesn't have route_target_refs
        if RI.route_target_refs is not None:
            for rt in RI.route_target_refs:
                if int((rt["to"][0]).split(":")[2]) > 7999999:
                    print ("system generated route target: " + str(rt["to"]))
                else:
                    print ("user defined route target: " + str(rt["to"]))       
        #get RTs end

        if VN_obj.IPAM:
            print("Network IPAM: ---")
            for ipam in VN_obj.IPAM:
                print(str(ipam["to"]))
                print("Network subnets: ")
                for subnets in ipam["attr"]["ipam_subnets"]:
                    print(subnets["subnet"]["ip_prefix"] + "/" + str(subnets["subnet"]["ip_prefix_len"]))
        
        print("IP Instances: ---" )
        #TODO
        if  VN_obj.IIP:
            IPs_dict = self.getVNIPs(VN_obj)
            for IP_id, IP_info in IPs_dict.items():   
                print("IP : " + IP_info["IP_obj"]["instance-ip"]["instance_ip_address"] ) 
                
                for VMI_uuid in IP_info["IP_obj"]["instance-ip"]["virtual_machine_interface_refs"]:
                    vmi = VirtualMachineInterface(VMI_uuid["uuid"])
                    print ("compute node: " + vmi.compute )
                    print ("interface: [" + vmi.mac + " | " + vmi.tap + "]")
                    
        else:
            print("VN doesn't have any IP instance")
        