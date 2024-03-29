import json
import requests
from requests.auth import HTTPBasicAuth

import configparser

class RIManager(object):
    
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.API_PASSWORD = config['API_SERVER']['PASSWORD']
        self.RIs_URL_PATH = config['API_SERVER']['URL_PATH'] + 'routing-instances'
        self.RI_URL_PATH = config['API_SERVER']['URL_PATH'] + 'routing-instance/'

    def getRIs(self):
        response = requests.get(self.RIs_URL_PATH, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        RIs = response.json()
        RI_dict = {}
        for RI in RIs["routing-instances"]:
	        RI_dict[RI["uuid"]] = {"name": RI["fq_name"]}
        return RI_dict

    def getRI(self, uuid):
        response = requests.get(self.RI_URL_PATH + uuid, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        return response.json()

    def getVMIs(self, RI):
        if "virtual_machine_interface_back_refs" not in RI["routing-instance"]:
            return []
        else:
            return RI["routing-instance"]["virtual_machine_interface_back_refs"]

class RoutingInstance(RIManager):

    def __init__(self, uuid):
        super().__init__()

        self.RI = self.getRI(uuid)["routing-instance"]
        self.fq_name = self.RI["fq_name"]
        self.bgp_routers = self.RI["bgp_routers"] if "bgp_routers" in self.RI else None
        self.route_target_refs = self.RI["route_target_refs"] if "route_target_refs" in self.RI else None
        self.static_route_entries = self.RI["static_route_entries"] if "static_route_entries" in self.RI else None
        self.virtual_machine_interface_back_refs = self.RI["virtual_machine_interface_back_refs"] if "virtual_machine_interface_back_refs" in self.RI else None
        self.created = self.RI["id_perms"]["created"] if "id_perms" in self.RI else None
        self.last_modified = self.RI["id_perms"]["last_modified"] if "id_perms" in self.RI else None
