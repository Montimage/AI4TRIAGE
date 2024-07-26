from scipy import spatial
from scipy.spatial import distance
from scipy.spatial.distance import jaccard
from scipy.spatial.distance import minkowski
from scipy.spatial.distance import cityblock
from sklearn import preprocessing
import numpy as np
import sys
import pymongo
import json
import datetime
import random
################################################################
#mean of an array 
def mean (a):
	avg = float(sum(a))/float(len(a))
        return avg
################################
#standard deviation of an array
def stdev (a): 
	return np.std(a)
################################
#calculate the stadardized value of a variable a knowing the mean and the standard deviation
def standardized (a, mean, stdev): 
	return (a-mean)/stdev
################################
#calculate the normalized value (standardized + rescaled between o and 1) 
def normalized (a, mean, stdev, a_max, a_min): 
	if not (a < a_max): 
		return 1
	if not (a > a_min):
		return 0
	a_standardized = standardized(a, mean, stdev)
	a_max_standardized = standardized(a_max, mean, stdev)
	a_min_standardized = standardized(a_min, mean, stdev)
	return (a_standardized-a_min_standardized)/(a_max_standardized-a_min_standardized)
#calculate a standardized array 
def standardized_a (a): 
	a_standardized = []
	for value in a: 
		value_standardized = standardized(value, mean(a), stdev(a))
		a_standardized.append(value_standardized)
	return a_standardized
################################
def normalized_a (a): 
	a_normalized = []
	for value in a: 
		value_normalized = normalized(value, mean(a), stdev(a), max(a), min(a))
		a_normalized.append(value_normalized)
	return a_normalized
#################################################################
mongoClient = pymongo.MongoClient("mongodb://localhost:27017") #tunnel to the server hosting the GUI
#db_source = "rca_its_2021_2_9_13"
db_source = sys.argv[1]
db = mongoClient[db_source]
hardware = db["hardware"]
security = db["security"]

db_d = "mmt-rca"
db_dest = mongoClient[db_d]
#known_state = db_dest["data_knowledge_inc"]
known_state = db_dest["data_knowledge_inc"]
known_state.drop()
learning_indicators = db_dest["learning_indicators"]
new_state = db_dest["data_real_time"]

#known event/state/incident
row = '{'
now = datetime.datetime.now()
#ID = '"STANDARD' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond)
ID = '"INCT' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond)
row += '"_id": ' + ID + '",'
row += '"attributes": {'
indicators = '{"_id": ' + ID + '",'

for gw in [1000501, 1000502, 1000503, 1000504, 1000505, 1000506, 1000507, 1000508, 1000509, 1000510, 1000511]: 
	CPU = []
	RAM = []
	POW = []
	DISK = []
	for hw in hardware.find({'Root.Gateway': gw}):
		CPU.append(float(hw['Nodes'][0]['Sensors-Actuators'][0]['Resources']['5700']))
		RAM.append(float(hw['Nodes'][0]['Sensors-Actuators'][1]['Resources']['5700']))
		POW.append(float(hw['Nodes'][0]['Sensors-Actuators'][2]['Resources']['5700']))
		DISK.append(float(hw['Nodes'][0]['Sensors-Actuators'][3]['Resources']['5700']))
	NB_CONN = []
	NB_CONN_UP = []
	AVG_PUB_SIZE = []
	AVG_RECV_SIZE = []
	PUB_RATE = []
	RECV_RATE = []
	MS_DELAY = []
	for sec in security.find({'Root.Gateway': gw}):
		NB_CONN.append(int(sec['Nodes'][0]['Sensors-Actuators'][0]['Resources']['5700']))
		NB_CONN_UP.append(int(sec['Nodes'][0]['Sensors-Actuators'][1]['Resources']['5700']))
		AVG_PUB_SIZE.append(int(sec['Nodes'][0]['Sensors-Actuators'][2]['Resources']['5700']))
		AVG_RECV_SIZE.append(int(sec['Nodes'][0]['Sensors-Actuators'][3]['Resources']['5700']))
		PUB_RATE.append(float(sec['Nodes'][0]['Sensors-Actuators'][4]['Resources']['5700']))
		RECV_RATE.append(float(sec['Nodes'][0]['Sensors-Actuators'][5]['Resources']['5700']))
		MS_DELAY.append(int(sec['Nodes'][0]['Sensors-Actuators'][6]['Resources']['5700'])) 
	row += '"' + str(gw) + '_CPU" : "' + str(mean(normalized_a(CPU))) + '",'
	row += '"' + str(gw) + '_RAM" : "' + str(mean(normalized_a(RAM)))  + '",'
	row += '"' + str(gw) + '_POW" : "' + str(mean(normalized_a(POW)))  + '",'
	row += '"' + str(gw) + '_DISK" : "' + str(mean(normalized_a(DISK)))  + '",'
	row += '"' + str(gw) + '_NB_CONN" : "' + str(mean(normalized_a(NB_CONN)))  + '",'
	row += '"' + str(gw) + '_NB_CONN_UP" : "' + str(mean(normalized_a(NB_CONN_UP)))  + '",'
	row += '"' + str(gw) + '_AVG_PUB_SIZE" : "' + str(mean(normalized_a(AVG_PUB_SIZE)))  + '",'
	row += '"' + str(gw) + '_AVG_RECV_SIZE" : "' + str(mean(normalized_a(AVG_RECV_SIZE)))  + '",'
	row += '"' + str(gw) + '_PUB_RATE" : "' + str(mean(normalized_a(PUB_RATE)))  + '",'
	row += '"' + str(gw) + '_RECV_RATE" : "' + str(mean(normalized_a(RECV_RATE)))  + '",'
	row += '"' + str(gw) + '_MS_DELAY" : "' + str(mean(normalized_a(MS_DELAY)))  + '",'
	indicators += '"' + str(gw) + '_CPU_MEAN" : "' + str(mean(CPU)) + '",'
	indicators += '"' + str(gw) + '_CPU_STDEV" : "' + str(stdev(CPU)) + '",'
	indicators += '"' + str(gw) + '_CPU_MAX" : "' + str(max(CPU)) + '",'
	indicators += '"' + str(gw) + '_CPU_MIN" : "' + str(min(CPU)) + '",'
	indicators += '"' + str(gw) + '_RAM_MEAN" : "' + str(mean(RAM)) + '",'
	indicators += '"' + str(gw) + '_RAM_STDEV" : "' + str(stdev(RAM)) + '",'
	indicators += '"' + str(gw) + '_RAM_MAX" : "' + str(max(RAM)) + '",'
	indicators += '"' + str(gw) + '_RAM_MIN" : "' + str(min(RAM)) + '",'
	indicators += '"' + str(gw) + '_POW_MEAN" : "' + str(mean(POW)) + '",'
	indicators += '"' + str(gw) + '_POW_STDEV" : "' + str(stdev(POW)) + '",'
	indicators += '"' + str(gw) + '_POW_MAX" : "' + str(max(POW)) + '",'
	indicators += '"' + str(gw) + '_POW_MIN" : "' + str(min(POW)) + '",'
	indicators += '"' + str(gw) + '_DISK_MEAN" : "' + str(mean(DISK)) + '",'
	indicators += '"' + str(gw) + '_DISK_STDEV" : "' + str(stdev(DISK)) + '",'
	indicators += '"' + str(gw) + '_DISK_MAX" : "' + str(max(DISK)) + '",'
	indicators += '"' + str(gw) + '_DISK_MIN" : "' + str(min(DISK)) + '",'
	indicators += '"' + str(gw) + '_NB_CONN_MEAN" : "' + str(mean(NB_CONN)) + '",'
	indicators += '"' + str(gw) + '_NB_CONN_STDEV" : "' + str(stdev(NB_CONN)) + '",'
	indicators += '"' + str(gw) + '_NB_CONN_MAX" : "' + str(max(NB_CONN)) + '",'
	indicators += '"' + str(gw) + '_NB_CONN_MIN" : "' + str(min(NB_CONN_UP)) + '",'
	indicators += '"' + str(gw) + '_NB_CONN_UP_MEAN" : "' + str(mean(NB_CONN_UP)) + '",'
	indicators += '"' + str(gw) + '_NB_CONN_UP_STDEV" : "' + str(stdev(NB_CONN_UP)) + '",'
	indicators += '"' + str(gw) + '_NB_CONN_UP_MAX" : "' + str(max(NB_CONN_UP)) + '",'
	indicators += '"' + str(gw) + '_NB_CONN_UP_MIN" : "' + str(min(NB_CONN_UP)) + '",'
	indicators += '"' + str(gw) + '_AVG_PUB_SIZE_MEAN" : "' + str(mean(AVG_PUB_SIZE)) + '",'
	indicators += '"' + str(gw) + '_AVG_PUB_SIZE_STDEV" : "' + str(stdev(AVG_PUB_SIZE)) + '",'
	indicators += '"' + str(gw) + '_AVG_PUB_SIZE_MAX" : "' + str(max(AVG_PUB_SIZE)) + '",'
	indicators += '"' + str(gw) + '_AVG_PUB_SIZE_MIN" : "' + str(min(AVG_PUB_SIZE)) + '",'
	indicators += '"' + str(gw) + '_AVG_RECV_SIZE_MEAN" : "' + str(mean(AVG_RECV_SIZE)) + '",'
	indicators += '"' + str(gw) + '_AVG_RECV_SIZE_STDEV" : "' + str(stdev(AVG_RECV_SIZE)) + '",'
	indicators += '"' + str(gw) + '_AVG_RECV_SIZE_MAX" : "' + str(max(AVG_RECV_SIZE)) + '",'
	indicators += '"' + str(gw) + '_AVG_RECV_SIZE_MIN" : "' + str(min(AVG_RECV_SIZE)) + '",'
	indicators += '"' + str(gw) + '_PUB_RATE_MEAN" : "' + str(mean(PUB_RATE)) + '",'
	indicators += '"' + str(gw) + '_PUB_RATE_STDEV" : "' + str(stdev(PUB_RATE)) + '",'
	indicators += '"' + str(gw) + '_PUB_RATE_MAX" : "' + str(max(PUB_RATE)) + '",'
	indicators += '"' + str(gw) + '_PUB_RATE_MIN" : "' + str(min(PUB_RATE)) + '",'
	indicators += '"' + str(gw) + '_RECV_RATE_MEAN" : "' + str(mean(RECV_RATE)) + '",'
	indicators += '"' + str(gw) + '_RECV_RATE_STDEV" : "' + str(stdev(RECV_RATE)) + '",'
	indicators += '"' + str(gw) + '_RECV_RATE_MAX" : "' + str(max(RECV_RATE)) + '",'
	indicators += '"' + str(gw) + '_RECV_RATE_MIN" : "' + str(min(RECV_RATE)) + '",'
	indicators += '"' + str(gw) + '_MS_DELAY_MEAN" : "' + str(mean(MS_DELAY)) + '",'
	indicators += '"' + str(gw) + '_MS_DELAY_STDEV" : "' + str(stdev(MS_DELAY)) + '",'
	indicators += '"' + str(gw) + '_MS_DELAY_MAX" : "' + str(max(MS_DELAY)) + '",'
	indicators += '"' + str(gw) + '_MS_DELAY_MIN" : "' + str(min(MS_DELAY)) + '",'
row = row[:-1]
indicators = indicators[:-1]
#row += '}, "timestamp": "' + str(now) + '", "description": "Incident learned: Central gateway receiving messages at the rate significantly lower than usual. Probable root-cause: failure in reporting data from users. Action: Check the connection to the users | Source/ Dataset: '+ db_source +' | Confidence (number of relevant reports): ' + str(len(NB_CONN)+len(MS_DELAY)) +'"}'
row += '}, "timestamp": "' + str(now) + '", "description": "Security door opened following a brute force attack. Probable root-cause: Potential intrusion. Action: Verify the intrusion if any | Source/ Dataset: '+ db_source +' | Confidence (number of relevant reports): ' + str(len(NB_CONN)+len(MS_DELAY)) +'"}'
indicators += '}'
print row 
print indicators
known_state = db_dest["data_knowledge_inc"]
known_state.insert_one(json.loads(row))
learning_indicators.insert_one(json.loads(indicators))
