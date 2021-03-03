import json
import requests
from requests.auth import HTTPBasicAuth
import configparser

import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from config.rest.VMI_rest import VMIRestManager



class IPResManager(object):
    #IPs_URL_PATH = 'http://localhost:8095/instance-ips'
    #IP_URL_PATH = 'http://localhost:8095/instance-ip/'
    #API_PASSWORD = 'vj2q9QvhPHUupDaXmBXXXF6Aj'

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.IPs_URL_PATH = config['API_SERVER']['URL_PATH'] + 'instance-ips'
        self.IP_URL_PATH = config['API_SERVER']['URL_PATH'] + 'instance-ip/'
        self.API_PASSWORD = config['API_SERVER']['PASSWORD']


    def getIPs(self):
        response = requests.get(self.IPs_URL_PATH, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        IPs = response.json()
        IPs_dict = {}
        print("Retrieving all IP objects from Config API... ","Total number:", len(IPs["instance-ips"]))
        
        for IP in IPs["instance-ips"]:
            IP_detail = self.getIP(IP['uuid']) 
            address = IP_detail["instance-ip"]["instance_ip_address"]
            #review vn_ref and get the list as an IP can belong to multiple VNs
            #vn_ref = IP_detail["instance-ip"]["virtual_network_refs"][0]["to"]
            vn_ref = IP_detail["instance-ip"]["virtual_network_refs"]
            IPs_dict[IP['uuid']] = {"address": address, "VN":vn_ref}
        return IPs_dict

    def getIP(self, uuid):
        response = requests.get(self.IP_URL_PATH+uuid, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        if response.status_code == 200:
            return response.json()
        return {}
    
    def getIPDetails(self, uuid):
        VMI_rest_manager = VMIRestManager()
        IP = self.getIP(uuid)
        IPs_dict = {}
        address = IP['instance-ip']['instance_ip_address']
        vn_ref = IP['instance-ip']['virtual_network_refs']
        #review vn_ref and get the list as an IP can belong to multiple VNs
        #vn_ref = IP_detail["instance-ip"]["virtual_network_refs"][0]["to"]
        VMI_details = VMI_rest_manager.getVMI(IP['instance-ip']['virtual_machine_interface_refs'][0]['uuid'])
        VM_details = VMI_rest_manager.getVM(VMI_details['virtual-machine-interface']['virtual_machine_refs'][0]['uuid'])

        IPs_dict[uuid] = {'address': address, 
                        'VN':vn_ref, 
                        'VMI': VMI_details['virtual-machine-interface']['virtual_machine_interface_mac_addresses'],
                        'compute': VMI_details['virtual-machine-interface']['virtual_machine_interface_bindings']['key_value_pair'][0]['value'],
                        'VM': VM_details['virtual-machine']['fq_name']}
        return IPs_dict
        IPs_list = []
        IPs_list.append()
'''class IP(object, IP):
    def __init__():
        self.address = IP['instance-ip']['instance_ip_address']
        self.vn = IP['instance-ip']['virtual_network_refs']
        self.compute = VMI_rest_manager.getVM(VMI_details['virtual-machine-interface']['virtual_machine_refs'][0]['uuid'])
        sel'''

'''class IPInstance(IPResManager):

    def __init__(self, uuid):
        super().__init__()

        self.IP = self.getRI(uuid)["routing-instance"]

        self.fq_name = self.RI["fq_name"]
        self.bgp_routers = self.RI["bgp_routers"] if "bgp_routers" in self.RI else None
        self.route_target_refs = self.RI["route_target_refs"] if "route_target_refs" in self.RI else None
        self.static_route_entries = self.RI["static_route_entries"] if "static_route_entries" in self.RI else None
        self.virtual_machine_interface_back_refs = self.RI["virtual_machine_interface_back_refs"] if "virtual_machine_interface_back_refs" in self.RI else None
        self.created = self.RI["id_perms"]["created"] if "id_perms" in self.RI else None
        self.last_modified = self.RI["id_perms"]["last_modified"] if "id_perms" in self.RI else None'''