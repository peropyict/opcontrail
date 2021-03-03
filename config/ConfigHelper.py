import readline

import json
import requests
from requests.auth import HTTPBasicAuth

class HelperClass(object):
    API_PASSWORD = 'vj2q9QvhPHUupDaXmBXXXF6Aj'
    def __init__(self, dict_object, search_object_by = 'fq_name'):
        #HelperClass takes dict object as argument which can be searched by search_object_attribute 
        #default key to search in is fq_name
        #in some cases, like for IP address, we can't search by fqname
        #last_search_text is null by default and it gets populated in complete method with the last searched text
        self.dict_object = dict_object
        self.search_object_by = search_object_by
        self.search_result_list = []
        self.last_search_text = ''
        self.uuid = ''

    def fqname_to_uuid(self, fq_name, obj_type):
        #return uuid for a given fqname and type
        data = {"fq_name": fq_name, "type": obj_type}
        headers = {'Content-type': 'application/json'}
        response = requests.post('http://localhost:8095/fqname-to-id', auth=HTTPBasicAuth('admin', self.API_PASSWORD), json=data, headers=headers)
        if response.status_code == 200:
            return response.json()['uuid']       
        return None

    def completeNew(self, text, state):
        #complete method implements filtering functionality for a given dictionary of objects 
        if len(text) > len(self.last_search_text):
            self.last_search_text = text
            self.search_result_list = []
        if self.search_object_by == 'fq_name':
            #print([item for item in self.dict_object if text in str(item.fq_name)])
            #for item in self.dict_object if text in str(item.fq_name):
            for item in self.dict_object:
                if text in str(item.fq_name):
                    if not state:
                        self.search_result_list.append(item)                                          
                        return item
                    else:
                        state -= 1

    def complete(self, text, state):
        #complete method implements filtering functionality for a given dictionary of objects 
        if len(text) > len(self.last_search_text):
            self.last_search_text = text
            self.search_result_list = []
        if self.search_object_by == 'fq_name':
            for p_id, p_info in self.dict_object.items():                 
                if text in str(p_info['name'][0]+"."+p_info['name'][1]+"."+p_info['name'][2]):
                    if not state:   
                        self.search_result_list.append(p_info['name'][0]+"."+p_info['name'][1]+"."+p_info['name'][2])                                          
                        return p_info['name'][0]+"."+p_info['name'][1]+"."+p_info['name'][2]
                    else:
                        state -= 1
        else:
            for p_id, p_info in self.dict_object.items():                 
                if text in str(p_info[self.search_object_by]):
                    if not state: 
                        if p_info[self.search_object_by] not in str(self.search_result_list):
                            self.search_result_list.append(p_info[self.search_object_by])   
                        return p_info[self.search_object_by]
                    else:
                        state -= 1

    #def searchHelper(self, searchText)       
    '''
    def completeCLI(self, text, state):
        for p_id, p_info in self.dict_object.items():                 
            if text in str(p_info['name'][0]+"."+p_info['name'][1]+"."+p_info['name'][2]):
                if not state:                    
                    return p_info['name'][0]+"."+p_info['name'][1]+"."+p_info['name'][2]
                else:
                    state -= 1
    def completeCLIIP(self, text, state):
        for p_id, p_info in self.dict_object.items():                 
            if text in str(p_info[self.search_object_attribute]):
                if not state:    
                    return p_info[self.search_object_attribute]
                else:
                    state -= 1
    '''