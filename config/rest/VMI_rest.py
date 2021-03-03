import json
import requests
from requests.auth import HTTPBasicAuth

import configparser

class VMIRestManager(object):
    VMIs_URL_PATH = 'http://localhost:8095/virtual-machine-interfaces'
    VMI_URL_PATH = 'http://localhost:8095/virtual-machine-interface/'
    VM_URL_PATH = 'http://localhost:8095/virtual-machine/'
    API_PASSWORD = 'vj2q9QvhPHUupDaXmBXXXF6Aj'

    def __init__(self):
        
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.API_PASSWORD = config['API_SERVER']['PASSWORD']
        self.VMIs_URL_PATH = config['API_SERVER']['URL_PATH'] + "virtual-machine-interfaces"
        self.VMI_URL_PATH = config['API_SERVER']['URL_PATH'] + "virtual-machine-interface/"
        self.VM_URL_PATH = config['API_SERVER']['URL_PATH'] + "virtual-machine/"
        

    def getVMIs(self):
        response = requests.get(self.VMIs_URL_PATH, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        VMIs = response.json()
        VMIs_dict = {}
        for VMI in VMIs["virtual-machine-interfaces"]:
            VMI_detail = self.getVMI(VMI['uuid']) 
            address = IP_detail["virtual-machine-interface"]["instance_ip_address"]
            #review vn_ref and get the list as an IP can belong to multiple VNs
            #vn_ref = IP_detail["instance-ip"]["virtual_network_refs"][0]["to"]
            vm_ref = self.getVM(VMI_detail["virtual-machine-interface"]["virtual_machine_refs"]["to"])
            compute_name = VMI_detail["virtual-machine-interface"]["virtual_machine_interface_bindings"]["key_value_pair"][0]["value"]
            mac = VMI_detail["virtual-machine-interface"]["virtual_machine_interface_mac_addresses"]

            VMIs_dict[VMI['uuid']] = {"compute": compute_name, "mac":mac, }
        return IPs_dict

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