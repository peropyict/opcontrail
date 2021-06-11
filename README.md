This is a code example to query Contrail API to list, seach and get object details. It supports Virtual Networks, Route Targets, VMs IP address list and search with tab autocompletion.
Virtual Networks details include: name & uuid, system & user created route target, ipam details with subnets, all VM IPs available in the subnets, compute nodes hosting VMs with tap interface names


Usage:
git clone https://github.com/peropyict/opcontrail.git
cd opcontrail
sudo apt install python3-pip
sudo pip3 install -r requirements.txt

The script requires connection to contrail api localhost 8095 port. Tunnel example for Contrail with RHOSP: ssh -J root@10.219.117.11,stack@192.168.122.241 heat-admin@192.168.24.6 -L8083:127.0.0.1:8083 -L8087:127.0.0.1:8087 -L15673:127.0.0.1:15673 -L8095:127.0.0.1:8095


./show.py config --help
usage: show config [-h] {vn,ip,ri,rt} ...

positional arguments:
  {vn,ip,ri,rt}
    vn           Show Virtual Network
    ip           Show IP adresses
    ri           Show Routing Instance
    rt           Show Route Target

optional arguments:
  -h, --help     show this help message and exit


Examples:

Enter to list objects: 
Example:
$ ./show.py config rt
Search for a RT Name: 
RI fqname: ['target', '64512', '8000005'] .... uuid(c58403c6-4caf-4d5b-8337-3e82e566e4bf)
RI fqname: ['target', '64512', '8000002'] .... uuid(5d2f6021-18a1-4097-b31f-1245b6c43658)
RI fqname: ['target', '64512', '8000004'] .... uuid(7f77e4d3-ad2f-4f31-a077-661c406197df)
RI fqname: ['target', '64512', '99'] .... uuid(47afe55a-e281-4880-845f-eaecb7f66ba4)
RI fqname: ['target', '64512', '1000'] .... uuid(8d34f2bf-76f3-4000-ab83-53047c5542d7)
RI fqname: ['target', '64512', '8000006'] .... uuid(d3483134-fc76-4525-96db-a5819c5c7cb4)
RI fqname: ['target', '64512', '8000000'] .... uuid(6b60430d-5931-4ef1-a72a-6bd46c648e2c)
RI fqname: ['target', '64512', '8000001'] .... uuid(e0e45fe7-095d-40f9-8e54-e0a3f2b724a7)
RI fqname: ['target', '64512', '8000003'] .... uuid(d3191384-cf95-46e0-b731-b4541c0413f4)


Type + Enter to search objects 
get
$ ./show.py config vn
Search for a VN Name: pub
-----------------------------------------
VN fqname: ['default-domain', 'admin', 'publicVN']
VN UUID: 983118bb-d11d-4281-9302-4e4bb1b1d137
Route Targets: ---
import route targets: {}
export route_targets: {}
system generated route target: ['target:64512:8000005']
user defined route target: ['target:64512:1000']
Network IPAM: ---
['default-domain', 'default-project', 'default-network-ipam']
Network subnets: 
10.219.140.0/28
IP Instances: ---
IP : 10.219.140.4
compute node: overcloud-novacompute-0.localdomain
interface: [02:4a:87:eb:8f:6a | tap4a87eb8f-6a]
IP : 10.219.140.3
compute node: overcloud-novacompute-0.localdomain
interface: [02:94:ce:f0:32:41 | tap94cef032-41]
IP : 10.219.140.6
compute node: 
interface: [02:22:6b:2e:f2:2b | tap226b2ef2-2b]


Type + Tab to search objects 
$ ./show.py config rt
Search for a RT Name: target.64512.1000
-----------------------------------------
RT fqname: ['target', '64512', '1000']
RT UUID: 8d34f2bf-76f3-4000-ab83-53047c5542d7
Routing instances: 
['default-domain', 'admin', 'publicVN', 'publicVN']
