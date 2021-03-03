import json
import requests
from requests.auth import HTTPBasicAuth

import configparser

class VNResManager(object):

    def __init__(self, args='', api_args=''):        
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.API_PASSWORD = config['API_SERVER']['PASSWORD']
        self.VN_URL_PATH = config['API_SERVER']['URL_PATH'] + "virtual-network/"
        self.VNs_URL_PATH = config['API_SERVER']['URL_PATH'] + "virtual-networks"
        self.VNs = self.getVNs()
        #self.VNs = self.getVNsSummary()
        
    def getVNs(self):
        #VNs {uuid:{name:fq_name}} dict
        #VNs {uuid:[name:fq_name]} TODO explore as option
        response = requests.get(self.VNs_URL_PATH, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        VNs = response.json()
        #VNsSummary = self.getVNsSummary()
        VNs_dict = {}
        for VN in VNs["virtual-networks"]:
	        VNs_dict[VN["uuid"]] = {"name": VN["fq_name"]}
        return VNs_dict

    #TODO
    def getVNsSummary(self):
        response = requests.get(self.VNs_URL_PATH, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        VNs = response.json()
        VNs_dict = {}
        VN_summary_list = []
        for VN in VNs["virtual-networks"]:
            VN_summary_object = VirtualNetworkSummary(**VN)
            VN_summary_list.append(VN_summary_object)
        return VN_summary_list

    def getVN(self, uuid):
        response = requests.get(self.VN_URL_PATH+uuid, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        return response.json()

#TODO
class VirtualNetworkSummary():
    def __init__(self, uuid, fq_name, href):
        self.fq_name = fq_name
        self.uuid = uuid
        self.href = href

class VirtualNetworkManager():
    def __init__(self, VN):
        self.RT = VN["route_target_list"] if "route_target_list" in VN else None
        self.RT_export = VN["export_route_target_list"] if "export_route_target_list" in VN else None
        self.RT_import = VN["import_route_target_list"] if "import_route_target_list" in VN else None
        self.fq_name = VN["fq_name"] if "fq_name" in VN else None
        self.RI = VN["routing_instances"] if "routing_instances" in VN else None
        self.IPAM = VN["network_ipam_refs"] if "network_ipam_refs" in VN else None
        self.IIP = VN["instance_ip_back_refs"] if "instance_ip_back_refs" in VN else None
        self.VMI = VN["virtual_machine_interface_back_refs"] if "virtual_machine_interface_back_refs" in VN else None

    

    

