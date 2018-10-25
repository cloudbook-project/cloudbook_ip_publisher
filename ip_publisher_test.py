import json
import os
import sys
import urllib.request # this import requires pip install requests
import logging
import random, string
from pynat import get_ip_info
import loader

my_agent_ID = "None"
my_circle_ID = "None"
agents_ip = {}
config_dict={}
config_dict=loader.load_dictionary("config_agent.json")

#Creates an agent ID and connects to the directory server to indicate its public IP, agent_id and circle_id
def createAgentID():
	global my_agent_ID
	global my_circle_ID
	#Random agent_id if it doesn't exist
	my_agent_ID= ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
	if config_dict["AGENT_ID"]=="0":
		config_dict["AGENT_ID"]=my_agent_ID
	else:
		my_agent_ID=config_dict["AGENT_ID"]
	my_circle_ID=config_dict["CIRCLE_ID"]
	fo = open("config_agent.json", 'w')
	json_data=json.dumps(config_dict)
	fo.write(json_data)
	fo.close()

#Announces agent information to the IP Publisher test
def announceAgent():
	#It uses STUN to get information about the public IP
	topology, external_ip, ext_port = get_ip_info()
	#external_ip="localhost"
	#external_port = al puerto que abramos para que corra el agent (parece que 3000+loquesea)
	url = "http://localhost:3100/post?circle_id="+str(my_circle_ID)+"&agent_id="+str(my_agent_ID)+"&ip_addr="+str(external_ip)#+":"+external_port
	print (url)
	try:
		urllib.request.urlopen(url)
	except:
		print ("Error connecting with IP Publisher Server")


def getAgentIP(agent_id):
	if agent_id in agents_ip:
		return agents_ip[agent_id]
	else:
		url = "http://localhost:3100/getAgentIP?circle_id=AAA&agent_id="+agent_id
		with urllib.request.urlopen(url) as res:
				data = json.loads(res.read().decode())
				f, v =list(data.items())[0]
				print (f)

createAgentID()
announceAgent()
#getAgentIP("")