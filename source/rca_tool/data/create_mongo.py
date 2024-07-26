import sys
import random
import datetime
import pymongo
import json



nb_rows = int(sys.argv[1])
nb_attributes = int(sys.argv[2])

incidents = ['Gateway G1 failed due to high CPU usage. Confidence: 927','Gateway G2 failed due to high CPU usage. Confidence: 927', 'Gateway G3 failed', 'Gateway G4 failed', 'Hello-flooding at G1', 'Hello-flooding at G2', 'Hello-flooding at G3', 'Hello-flooding at G4', 'SYN-flooding at G1', 'SYN-flooding at G2', 'SYN-flooding at G3', 'SYN-flooding at G4']

mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
db = mongoClient["mmt-rca"]
collection = db["data_knowledge"]
for incident in incidents:
        row = '{'
        now = datetime.datetime.now()
        row += '"_id": "INCT_' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond) + '",'
        row += '"description": "' + incident + '",'
        row += '"attributes": {'
        for j in range(nb_attributes):
                row += '"TEST_' + str(j) + '" : "' + str(random.random()) + '",'
        row = row[:-1]
        row += '}, "timestamp": "' + str(now) + '"}'
        print row
        collection.insert_one(json.loads(row))
