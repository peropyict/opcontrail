#https://github.com/tnaganawa/tungstenfabric-docs/blob/master/TungstenFabricPrimer.md
import json

#from tabCompletion import Tabcomplete
from prompt_toolkit import prompt
import readline

from rest.RI_res import RIManager

RIManager = RIManager()
RIs = RIManager.getRIs()

RI_UUID = ''

def completeRI(text, state):
    for p_id, p_info in RIs.items():
        global RI_UUID
        RI_UUID = p_id       
        if text in str(p_info['name'][0]+"."+p_info['name'][1]+"."+p_info['name'][2]):
            if not state:
                return p_info['name'][0]+"."+p_info['name'][1]+"."+p_info['name'][2]
            else:
                state -= 1

readline.set_completer_delims("\n")
readline.parse_and_bind("tab: complete")
readline.set_completer(completeRI)
RI_name  = input("VN/RI Name: ")

print(RI_name)
print(RI_UUID)

RI_obj = RIManager.getRI(RI_UUID)
RTs = RIManager.getRTs(RI_obj)
print("route targets: ")
for rt in RTs:
    print(rt)
#RIs[RIs.keys()[0]] = {"RTs": RTs}



def print_RIs(RIs):
    for p_id, p_info in RIs.items():
        print("RI ID:", p_id)
        for key in p_info:
            print(key + ':', p_info[key])
	    #if p_info[key] in p_info[key]:
		#    print('RI uuid is: ' + p_id)
        #break
        break


#print_RIs(RIs)

#print(RI_obj)

#print(RIs.values())
