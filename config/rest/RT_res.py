import json
import requests
from requests.auth import HTTPBasicAuth

import configparser




class RTManager(object):
    #RTs_URL_PATH = 'http://localhost:8095/route-targets'
    #RT_URL_PATH = 'http://localhost:8095/route-target/'
    #API_PASSWORD = 'vj2q9QvhPHUupDaXmBXXXF6Aj'
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.API_PASSWORD = config['API_SERVER']['PASSWORD']
        self.RTs_URL_PATH = config['API_SERVER']['URL_PATH'] + "route-targets"
        self.RT_URL_PATH = config['API_SERVER']['URL_PATH'] + "route-target"
    

    def getRTs(self):
        response = requests.get(RT_URL_PATH, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        RTs = response.json()
        RT_dict = {}
        for RT in RTs["route-target"]:
	        RT_dict[RT["uuid"]] = {"name": RT["display_name"]}
        return RT_dict

    def getRT(self, uuid):
        response = requests.get(RT_URL_PATH + uuid, auth=HTTPBasicAuth('admin', self.API_PASSWORD))
        if response.status_code == 200:
            return response.json()
        return {}

    

