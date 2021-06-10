import json
import requests
from requests.auth import HTTPBasicAuth

import configparser




class RTRestManager(object):
    #RTs_URL_PATH = 'http://localhost:8095/route-targets'
    #RT_URL_PATH = 'http://localhost:8095/route-target/'
    #API_PASSWORD = 'vj2q9QvhPHUupDaXmBXXXF6Aj'
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.API_PASSWORD = config['API_SERVER']['PASSWORD']
        self.RTs_URL_PATH = config['API_SERVER']['URL_PATH'] + "route-targets"
        self.RT_URL_PATH = config['API_SERVER']['URL_PATH'] + "route-target/"
        #self.RTs = self.getRTs()

    def getRTs(self):
        response = requests.get(self.RTs_URL_PATH, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        RTs = response.json()
        RT_dict = {}
        for RT in RTs["route-targets"]:
	        RT_dict[RT["uuid"]] = {"name": RT["fq_name"]}
        return RT_dict

    def getRT(self, uuid):
        response = requests.get(self.RT_URL_PATH + uuid, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        if response.status_code == 200:
            return response.json()
        return {}

    

class RouteTargetManager():
    def __init__(self, RT):
        #self.RT = VN["route_target_list"] if "route_target_list" in VN else None
        #self.RT_export = VN["export_route_target_list"] if "export_route_target_list" in VN else None
        #self.RT_import = VN["import_route_target_list"] if "import_route_target_list" in VN else None
        self.fq_name = RT["fq_name"] if "fq_name" in RT else None
        self.RIs = RT["routing_instance_back_refs"] if "routing_instance_back_refs" in RT else None
        #self.IPAM = VN["network_ipam_refs"] if "network_ipam_refs" in VN else None
        #self.IIP = VN["instance_ip_back_refs"] if "instance_ip_back_refs" in VN else None
        #self.VMI = VN["virtual_machine_interface_back_refs"] if "virtual_machine_interface_back_refs" in VN else None