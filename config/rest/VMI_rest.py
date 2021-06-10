import json
import requests
from requests.auth import HTTPBasicAuth

import configparser

class VMRestManager(object):

    def __init__(self):        
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.API_PASSWORD = config['API_SERVER']['PASSWORD']
        self.VMIs_URL_PATH = config['API_SERVER']['URL_PATH'] + "virtual-machine-interfaces"
        self.VMI_URL_PATH = config['API_SERVER']['URL_PATH'] + "virtual-machine-interface/"
        self.VM_URL_PATH = config['API_SERVER']['URL_PATH'] + "virtual-machine/"
        self.SG_URL_PATH = config['API_SERVER']['URL_PATH'] + "security-group/"
        

    def getVMIs(self):
        response = requests.get(self.VMIs_URL_PATH, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        VMIs = response.json()
        VMIs_dict = {}
        for VMI in VMIs["virtual-machine-interfaces"]:
            VMI_detail = self.getVMI(VMI['uuid']) 
            #address = VMI_detail["virtual-machine-interface"]["instance_ip_address"]
            #review vn_ref and get the list as an IP can belong to multiple VNs
            #vn_ref = IP_detail["instance-ip"]["virtual_network_refs"][0]["to"]
            #vm_ref = self.getVM(VMI_detail["virtual-machine-interface"]["virtual_machine_refs"]["to"])
            compute_name = VMI_detail["virtual-machine-interface"]["virtual_machine_interface_bindings"]["key_value_pair"][0]["value"]
            mac = VMI_detail["virtual-machine-interface"]["virtual_machine_interface_mac_addresses"]
            VMIs_dict[VMI['uuid']] = {"compute": compute_name, "mac":mac, }
        return VMIs_dict

    def getVMI(self, uuid):
        response = requests.get(self.VMI_URL_PATH + uuid, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        if response.status_code == 200:
            return response.json()
        return {}
    def getVM(self, uuid):
        response = requests.get(self.VM_URL_PATH + uuid, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        if response.status_code == 200:
            return response.json()
        return {}

class VirtualMachineInterface(VMRestManager):

    def __init__(self, uuid):
        super().__init__()

        self.VMI = self.getVMI(uuid)["virtual-machine-interface"]
        self.mac = self.VMI["virtual_machine_interface_mac_addresses"]["mac_address"][0] #why list
        maclist = self.mac.split(":")
        self.tap = "tap" + "".join(maclist[1:len(maclist)-1]) + "-" + maclist[-1]
        self.compute = ""
        for kvp in self.VMI["virtual_machine_interface_bindings"]["key_value_pair"]:
            if kvp['key'] == "host_id":
                self.compute = kvp['value']

class SecurityGroup(VMRestManager):
    def __init__(self, uuid):
        super().__init__()

        self.SG = self.getSG(uuid)["security-group"]
        self.rules = self.SG["security_group_entries"]
        #TODO for rule in rules...

    def getSG(self, uuid):
        response = requests.get(self.SG_URL_PATH + uuid, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        if response.status_code == 200:
            return response.json()
        return {}