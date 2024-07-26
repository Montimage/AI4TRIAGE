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
import time
from scipy.optimize._tstutils import description


###################################################
def cosine_similarity(a1,a2):
        return 1-spatial.distance.cosine(a1,a2)
##################################################
def adjusted_cosine_similarity(a1, a2):
        mean_a1a2 = (np.sum(a1+a2))/(len(a1)+len(a2))
        return (1-spatial.distance.cosine(a1-mean_a1a2,a2-mean_a1a2))

##################################################
def jaccard_distance(a,b): 
	return jaccard(a,b)
##################################################
def minkowski_distance(a,b): 
	return minkowski(a,b)
##################################################
def euclidean_distance(a1,a2): 
	return distance.euclidean(a1,a2)
##################################################
def manhattan_distance(a,b): 
	return cityblock(a,b)
##################################################
#standard deviation of an array
def stdev (a): 
    return np.std(a)
################################
#calculate the stadardized value of a variable a knowing the mean and the standard deviation
def standardized (a, mean, stdev): 
    if stdev > 0:
        return (a-mean)/stdev
    else: 
        return 0
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
    if (a_max_standardized==a_min_standardized) : 
        return 0 
    else: 
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

while 1:
    mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
    #db_source = "rca_its_2021_2_9_13"
    db_d = "mmt-rca"
    db_dest = mongoClient[db_d]
    known_state = db_dest["data_knowledge_inc"]
    learning_indicators = db_dest["learning_indicators"] #indicators to normalised monitoring data in real time
    new_state = db_dest["data_real_time"] #normalised data
    new_state_raw = db_dest["raw_data_real_time"]#raw data before being normalised
    report = db_dest["109102_report"] #Report back to INDRA's MQTT broker
    known_incident_id = ""
    max_sim_score = 0 #to include to 109102 report
    sim_score = 0
    created = ""
    description = ""
    for raw_state in new_state_raw.find({}).sort([('timestamp', -1)]).limit(1): 
        for indicators in learning_indicators.find({}): 
            #print raw_state
            curr_raw_state = [] 
            curr_normalised_state = []
            for gw in [1000501, 1000502, 1000503, 1000504, 1000505, 1000506, 1000507, 1000508, 1000509, 1000510, 1000511]: 
                #print raw_state[str(gw)+"_CPU"]
                for attribute in ["_CPU", "_RAM", "_POW", "_DISK", "_NB_CONN", "_NB_CONN_UP", "_AVG_PUB_SIZE", "_AVG_RECV_SIZE", "_PUB_RATE", "_RECV_RATE", "_MS_DELAY"]:
                    curr_raw_state.append(raw_state[str(gw) + attribute])
                    mean_a = float(indicators[str(gw) + attribute + "_MEAN"])
                    stdev_a = float(indicators[str(gw) + attribute + "_STDEV"])
                    max_a = float(indicators[str(gw) + attribute + "_MAX"])
                    min_a = float(indicators[str(gw) + attribute + "_MIN"])
                    index = str(gw) + attribute
                    curr_normalised_state.append(normalized(raw_state[index], mean_a, stdev_a, max_a, min_a)) #to be compared with old normalized states
            for a_known_state in known_state.find():
                normalised_known_state = []
                for gw in [1000501, 1000502, 1000503, 1000504, 1000505, 1000506, 1000507, 1000508, 1000509, 1000510, 1000511]:
                    for attribute in ["_CPU", "_RAM", "_POW", "_DISK", "_NB_CONN", "_NB_CONN_UP", "_AVG_PUB_SIZE", "_AVG_RECV_SIZE", "_PUB_RATE", "_RECV_RATE", "_MS_DELAY"]:
                        normalised_known_state.append(float(a_known_state["attributes"][str(gw)+attribute]))
                sim_score = abs(adjusted_cosine_similarity(curr_normalised_state, normalised_known_state))
                if (sim_score > max_sim_score): 
                    max_sim_score = sim_score; 
                    known_incident_id = a_known_state["_id"]
                    created = a_known_state["timestamp"]
                    description = a_known_state["description"]
        #print max_sim_score
        #print known_incident_id
        new_report = {"KnownIncidentID" : known_incident_id, "Created": created, "Description" : description, "Similarity score": max_sim_score, "Proof": raw_state}
        report.insert_one(new_report)
        print new_report
        #new_state_raw.drop()
    time.sleep(5) 
   