# IP PUBLISHER SERVER
import threading
from flask import Flask
from flask import request
from flask import jsonify
import json
from flask import abort, redirect, url_for, jsonify
import os
import sys
import time


application = Flask(__name__)

@application.route("/", methods=['GET','POST'])
def hello():
	return "Welcome to Cloudbook IP Publisher Service"

#Processes the request to post agent id and ip address
@application.route("/post", methods=['GET','POST'])
def read_request():

	circle_id=request.args.get('circle_id')
	agent_id=request.args.get('agent_id')
	ip_addr=request.args.get('ip_addr')

	#Security inputs check
	#if len(circle_id)!=20 or len(agent_id)!=20:
	#	return "Wrong input format"
	#if r'\W' in agent_id or circle_id:
	#	return "Wrong input format"
	 
	print ("-----------")
	print (circle_id)
	print (agent_id) 
	print (ip_addr)
	print ("-----------")
	dumpJSON(circle_id ,agent_id, ip_addr)
	return "You belong to circle " + circle_id+ ". Saved your id " + agent_id + " and your IP " + ip_addr



#Generates a file for each circle_id
#Generates JSON file containing agents ids and their ip addresses, if the agent id already exists 
#in the file, its ip address is updated
def dumpJSON(circle, agent, ip):
	timestamp = time.time()

	#Checking if file exists, if not, create.
	file_exists = os.path.isfile("./directories/"+circle+".json")
	if not file_exists:
		fo = open("./directories/"+circle+".json", 'w')
		fo.close()
	
	#Checking if file is empty
	if os.stat("./directories/"+circle+".json").st_size==0:
		fo = open("./directories/"+circle+".json", 'w')
		data={}
		data[agent]={}
		data[agent]={}
		data[agent]["IP"]=ip
		data[agent]["timestamp"]=timestamp
		json_data=json.dumps(data)
		fo.write(json_data)	
		fo.close()
	#If file is not empty, looks for agent_id to update info, if it's not found, creates it.
	else:
		fr = open("./directories/"+circle+".json", 'r')
		directory = json.load(fr)
		print ("-----------")
		print (repr(directory))
		if agent in directory:
			directory[agent]["IP"]=ip
			directory[agent]["timestamp"]=timestamp
			print (repr(directory))
			print ("-----------")
			fo = open("./directories/"+circle+".json", 'w')
			directory= json.dumps(directory)
			fo.write(directory)
			fo.close()
			return
		
		fr = open("./directories/"+circle+".json", 'r')
		directory = json.load(fr)
		directory[agent]={}
		directory[agent]["IP"]=ip
		directory[agent]["timestamp"]=timestamp
		print (repr(directory))
		fo = open("./directories/"+circle+".json", 'w')
		directory= json.dumps(directory)
		fo.write(directory)
		fo.close()
	return



#Generates a JSON file of a complete certain circle to be posted in the website
@application.route("/getCircle", methods=['GET','POST'])
def get_circle():
	circle_id=request.args.get('circle_id')

	timestamp = time.time()
	
	#Security inputs check
	#if len(circle_id)!=20:
	#	return "Wrong input format"
	#if r'\W' in circle_id:
	#	return "Wrong input format"

	#Checking if file exists, if not circle_id is wrong.
	if not os.path.isfile("./directories/"+circle_id+".json"):
		return "Error"
	#If found, return it.
	else:
		fr = open("./directories/"+circle_id+".json", 'r')
		directory = json.load(fr)
		for agent in directory:
			#Timestamp already changed, jumps to next
			if directory[agent]["IP"]=="None":
				continue
			#Timestamp hasn't changed during 5 minutes. IP not valid.
			if directory[agent]["timestamp"]+300<=timestamp:
				directory[agent]["IP"]="None"
		return jsonify(directory)

#URL format
# http://localhost:3100/getCircle?circle_id=AAA



#Returns the IP address of a certain agent
@application.route("/getAgentIP", methods=['GET', 'POST'])
def get_agent():
	circle_id=request.args.get('circle_id')
	agent_id=request.args.get('agent_id')

	timestamp = time.time()
	
	#Security inputs check
	#if len(circle_id)!=20 or len(agent_id)!=20:
	#	return "Wrong input format"
	#if r'\W' in agent_id or circle_id:
	#	return "Wrong input format"

	#Checking if file exists, if not circle_id is wrong.
	if not os.path.isfile("./directories/"+circle_id+".json"):
		return "Error"
	#If file exists, looks for agent_id, else, agent_id is wrong.
	else:
		fr = open("./directories/"+circle_id+".json", 'r')
		directory = json.load(fr)
		if agent_id in directory:
			if directory[agent_id]["timestamp"]+300<=timestamp:
				directory[agent_id]["IP"]="None"
			data={}
			data[directory[agent_id]["IP"]]={}
			return jsonify(data)
	return "Error"

#URL format
# http://localhost:3100/getAgentIP?circle_id=AAA&agent_id=NJMAYVW7JR6PGLTEPK94



#Deletes IP address if not refresed every 5 minutes.
#f refresh_IPs():
#while(True):
#	print("Checking valid IPs...")
#	#actual time
#	timestamp = time.time()
#	#print (os.listdir("./directories/"))
#	#list of all files
#	files=os.listdir("./directories/")
#	if len(files) == 0:
#		continue
#	for key in files:
#		#Only analyses JSON files
#		if os.stat("./directories/"+key).st_size==0:
#			continue
#		if key[-5:] == ".json":
#			fr = open("./directories/"+key, 'r')
#			try:
#				directory=json.load(fr)
#			except:
#				print ("Invalid file, continuing...")
#				fr.close()
#				continue
#			for agent in directory:
#				#Timestamp already changed, jumps to next
#				if directory[agent]["IP"]=="None":
#					continue
#				#Timestamp hasn't changed during 5 minutes. IP not valid.
#				if directory[agent]["timestamp"]+300<=timestamp:
#					directory[agent]["IP"]="None"
#		
#		#Write changes
#		fo = open("./directories/"+key, 'w')
#		directory= json.dumps(directory)
#		fo.write(directory)
#		fo.close()
#	time.sleep(10)



def flaskRun():
	print("Starting Flask...")
	application.run(debug=False, host="0.0.0.0", port=80, threaded=True)



if __name__ == "__main__":
	#Runs a Thread that checks the IPs that hasn't been updated
	#threading.Thread(target=refresh_IPs).start()
	#Runs Flask
	flaskRun()
