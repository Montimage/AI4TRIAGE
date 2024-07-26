from scipy import spatial
import numpy as np
import sys
import pymongo
import json
import datetime
import random

###################################################
def cosine_similarity(a1,a2):
        return 1-spatial.distance.cosine(a1,a2)
##################################################
def adjusted_cosine_similarity(a1, a2):
        mean_a1a2 = (np.sum(a1+a2))/(len(a1)+len(a2))
        return (1-spatial.distance.cosine(a1-mean_a1a2,a2-mean_a1a2))
##################################################
nb_rows = 1 #new record
nb_attributes = len(sys.argv) -1
attributes = [float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8]), float(sys.argv[9]), float(sys.argv[10])]

mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
db = mongoClient["mmt-rca"]
known_inct = db["data_knowledge"]
new_inct = db["data_real_time"]

for i in range(1):
        state = [] #state of the system identified by the captured attributes
        row = '{'
        now = datetime.datetime.now()
        row += '"_id": "INCT_' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond) + '",'
        row += '"attributes": {'
        for j in range(nb_attributes-1):
                attr = attributes[j]
                state.append(attr)
                row += '"attribute_' + str(j) + '" : "' + str(attr) + '",'
        attr = attributes[nb_attributes-1]
        state.append(attr)
        row += '"attribute_' + str(nb_attributes-1) + '" : "' + str(attr) + '"}, '
        row += '"similarity_score": {'
        inct_index = 0
        for inct in known_inct.find():
                #print inct
                inct_index += 1
                state_known = [] #known state of a known incident
                _id = inct["_id"]
                for k in range(nb_attributes):
                        att = 'attribute_'+str(k)
                        state_known.append(float(inct["attributes"][att]))
                #sim_score = cosine_similarity (state, state_known) #similarity score
                sim_score = abs(adjusted_cosine_similarity(state, state_known)) #similarity score
                row += '"'+ _id +'":"'+ str(sim_score) + '",'
        row = row[:-1]
        row += '},'
        row += '"timestamp": "' + str(now) + '"}'
        #print row
        new_inct.insert_one(json.loads(row))
