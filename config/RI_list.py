import json
import requests
uuids=["6c1fabfd-35b5-44eb-a410-3bd51ca837a0","bdaabeb7-ecdf-45e2-91cd-13672c1e3afb","9a7dbcf3-6160-4126-b3ba-d75faef918e1","d21ef97e-2ee4-495b-a19c-7304df6cad6c","59cad79b-d901-4e62-a6c3-cdd14b8e2f2d","ef8849dc-c094-4028-beff-008a1ac9f8c3","ac0d5271-11a4-415b-b197-1fe71902abc0","eee4ff1d-6e74-48fd-bea2-1d7a3d13fc4b","ef686a81-0591-4759-9734-4e2985b88bf1","02aa8d5e-e8f8-4c94-9774-b0fb5f75ae43","8e4dd2b3-4acd-46a0-8b06-54d639897349","0113da79-a482-4051-818f-a1056029ed53","27fd5f80-9ed3-4c24-b012-d85ff458b8ce","b0d7fff1-b0e6-4bde-8aa0-a5805a211731","87fa4dc4-e48b-4232-9324-576738c6d282","0375f4ae-a38a-431c-bc8d-cbf1b79e0cea"]

for id in uuids:
    print
    response = requests.get('http://localhost:8095/routing-instance/'+id)
    data = response.json()
    print "RI UUID:" + id + "   fqname:" + data["routing-instance"]["display_name"]
    if "virtual_machine_interface_back_refs" not in data["routing-instance"]:
        print "There is NO VMIs in this VN"
    else:
        print data["routing-instance"]["virtual_machine_interface_back_refs"]
    if "route_target_refs" not in data["routing-instance"]:    
        print "There is NO RTs in this RI"
    else:
        #print data["routing-instance"]["route_target_refs"]["route_target_refs"][0]["to"][0]
        RT_response = requests.get(data["routing-instance"]["route_target_refs"][0]["href"])
        RT_data = RT_response.json()
        RT_RI_refs = RT_data["route-target"]["routing_instance_back_refs"]
        print "RI's system RT:" + data["routing-instance"]["route_target_refs"][0]["to"][0] 
        print "RT " + RT_data["route-target"]["display_name"] + " RIs back references:"
        for rt_ri in RT_RI_refs:
            print rt_ri["to"]


