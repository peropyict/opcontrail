import json
import requests
from requests.auth import HTTPBasicAuth
import configparser
import paramiko

import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from config.rest.VMI_rest import VMRestManager, VMRestManager



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
        VM_rest = VMRestManager()
        IP = self.getIP(uuid)
        IPs_dict = {}
        address = IP['instance-ip']['instance_ip_address']
        vn_ref = IP['instance-ip']['virtual_network_refs']
        #review vn_ref and get the list as an IP can belong to multiple VNs
        #vn_ref = IP_detail["instance-ip"]["virtual_network_refs"][0]["to"]
        VMI_details = VM_rest.getVMI(IP['instance-ip']['virtual_machine_interface_refs'][0]['uuid'])
        VM_details = VM_rest.getVM(VMI_details['virtual-machine-interface']['virtual_machine_refs'][0]['uuid'])

        IPs_dict[uuid] = {'address': address, 
                        'VN':vn_ref, 
                        'VMI': VMI_details['virtual-machine-interface']['virtual_machine_interface_mac_addresses'],
                        'compute': VMI_details['virtual-machine-interface']['virtual_machine_interface_bindings']['key_value_pair'][0]['value'],
                        'VM': VM_details['virtual-machine']['fq_name']}
        
        
        
        return IPs_dict
        IPs_list = []
        IPs_list.append()




        '''
        >>> from fabric import *
        >>> sdn1='10.219.117.11'
        >>> sdn1user='root'
        >>> undercloud='192.168.122.241'
        >>> underclouduser='stack'
        >>> compute0='192.168.24.22'
        >>> compute_user='heat-admin'
        
        >>> sdn1_con = Connection(sdn1, sdn1user, port=22)
        >>> undercloud_con = Connection(undercloud, underclouduser, port=22, gateway=sdn1_con)
        >>> compute0_con = Connection(compute0, compute_user, port=22, gateway=undercloud_con)'''
        #>>> result = undercloud_con.run(f'''ls -al''', hide=True)'''
        #>>> result = compute0_con.run(f'''sudo docker exec contrail_vrouter_agent flow -l  --match 10.219.140.3''', hide=True)
        '''>>> result.stdout

        ssh=paramiko.SSHClient() 
        ssh.connect (host, 22, user, password)
        stdin, stdout, stderr=ssh.exec_command(command)
        for line in stdout.read().splitlines():
            print(line). 
        '''