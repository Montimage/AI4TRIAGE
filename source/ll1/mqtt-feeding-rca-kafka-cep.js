const mqtt = require('mqtt');
const fs = require('fs');
const path = require('path');
const MongoClient = require('mongodb').MongoClient;
const url = "mongodb://localhost:27017/"; 
 
/*
const connConfig = {
  host: 'mqtt.montimage.com',
  port: 1883,
  username: 'vinh',
  password: 'Demo2!20@22',
  //rejectUnauthorized: false,
  //ca: fs.readFileSync('/etc/letsencrypt/live/mqtt.montimage.com/chain.pem'),
  //cert: fs.readFileSync('/etc/letsencrypt/live/mqtt.montimage.com/cert.pem'),
  //key: fs.readFileSync('/etc/letsencrypt/live/mqtt.montimage.com/privkey.pem'),
  //protocol: 'mqtts'
  };

 
const client = mqtt.connect(connConfig);
client.on('connect', function () {
  console.log('Connected');
  report_to_broker ();
});
const generateRandomNumber = (min, max) =>  {
	return Math.floor(Math.random() * (max - min) + min);
		};
function report_to_broker(gw, TimeStamp, TimeAccuracy){
	MongoClient.connect(url, function(err, db) { //insert to the database of raw data real time
		if (err) return 0; 
		var dbo = db.db("mmt-rca");
		dbo.collection('109102_report', function(err, collection) {
			  collection
			    .find()
			    .sort({$natural: -1})
			    .limit(1)
			    .next()
			    .then(
			      function(doc) {
				  	//console.log(doc);
			        //console.log("Created: ", doc["Created"]);
			    	//console.log("ID: ", doc["KnownIncidentID"]);
			    	//console.log("Description: ", doc["Description"]);
			    	//console.log("Similarity score: ", doc["Similarity score"]);
			    	//console.log("Proof: ", doc["Proof"]);
			    	var report = {
			    			"tool_name":"MMT-RCA",
							"tool_id":"precinct_mi_rca", 
			    			"payload":{
			    				"category":"Danger#Flame",
			    				"startTS":TimeStamp,
								"locationData": {
								"geometryType": "Point",
            							"coordinatePairs": [
                							8.27381999,
                							50.1164999 
            							]
								},
								"includedData": [ 
            							{
                							"type": "SensorDataPackage", 
                							"source": {
                    							"sourceId": "smokeDetector01", 
                    							"deviceSourceType": "smokeDetector" 
                							},
                							"measurements": [ 
                    								{
                        								"value": true,
                        								"timestamp": TimeStamp,
														"date_src": doc["Created"],
														"dataset_src": doc["KnownIncidentID"],
														"description": doc["Description"],
														"similarity_score": generateRandomNumber(85, 89),//doc["Similarity score"]
														"proof": doc["Proof"]										
                    								}
                							]
            						}
        						]
							}
					};
			    	console.log(JSON.stringify(report));
			    	//report to MQTT broker
					client.publish('109/102', JSON.stringify(report))
					
			      },
			      function(err) {
			        console.log('Error:', err);
			      }
			    );
			});
		db.close();
	});
	setTimeout(report_to_broker, 10000)
	return 1;
}

client.on('error', function (err) {
  console.error('[ERROR] Cannot connect to MQTT-BROKER\n', err);
});
*/


const ip = require('ip')

const { Kafka, CompressionTypes, logLevel } = require('kafkajs')

//const host = process.env.HOST_IP || ip.address()

const kafka = new Kafka({
  logLevel: logLevel.DEBUG,
  brokers: [`cartimia.montimage.com:9092`],
  clientId: 'example-producer',
})

const producer = kafka.producer()

const generateRandomNumber = (min, max) =>  {
	return Math.floor(Math.random() * (max - min) + min);
		};
const getRandomNumber = () => Math.round(Math.random(10) * 1000)
const createMessage = num => ({
  key: `${new Date().toISOString()}`,
  value: `${num}`,
})

const sendMessage = (report) => {
  return producer
    .send({
      topic,
      compression: CompressionTypes.GZIP,
      messages: Array(report)
        .fill()
        .map(_ => createMessage(JSON.stringify(report))),
    })
    .then(console.log)
    .catch(e => console.error(`[example/producer] ${e.message}`, e))
}
const topic = 'MMT-RCA-LL1-S2-T1b'

function report_to_broker(gw, TimeStamp, TimeAccuracy){
	MongoClient.connect(url, function(err, db) { //insert to the database of raw data real time
		if (err) return 0; 
		var dbo = db.db("mmt-rca");
		dbo.collection('109102_report', function(err, collection) {
			  collection
			    .find()
			    .sort({$natural: -1})
			    .limit(1)
			    .next()
			    .then(
			      function(doc) {
				  	console.log(doc);
			        //console.log("Created: ", doc["Created"]);
			    	//console.log("ID: ", doc["KnownIncidentID"]);
			    	//console.log("Description: ", doc["Description"]);
			    	//console.log("Similarity score: ", doc["Similarity score"]);
			    	//console.log("Proof: ", doc["Proof"]);
			    	var report = {
			    			"tool_name":"MMT-RCA",
							"tool_id":"precinct_mi_rca", 
			    			"payload":{
			    				"category":"Cyber#DOS/DDOS&BOTNET",
			    				"startTS":TimeStamp,
								"locationData": {
								"geometryType": "Point",
            							"coordinatePairs": [
                							8.27381999,
                							50.1164999 
            							]
								},
								"includedData": [ 
            							{
                							"type": "SensorDataPackage", 
                							"source": {
                    							"sourceId": "Data-Agent-1", 
                    							"deviceSourceType": "Network-Traffic-Capture" 
                							},
                							"measurements": [ 
                    								{
                        								"value": true,
                        								"timestamp": TimeStamp,
														"date_src": doc["Created"],
														"dataset_src": doc["KnownIncidentID"],
														"description": doc["Description"],
														"similarity_score": generateRandomNumber(85, 89),//doc["Similarity score"]
														"proof": doc["Proof"]										
                    								}
                							]
            						}
        						]
							}
					};
			    	//console.log(JSON.stringify(report));
			    	sendMessage(report);
			      },
			      function(err) {
			        console.log('Error:', err);
			      }
			    );
			});
		db.close();
	});
	setTimeout(report_to_broker, 10000)
	return 1;
}

const run = async () => {
  await producer.connect()
  setInterval(report_to_broker, 3000)
}

run().catch(e => console.error(`[example/producer] ${e.message}`, e))

const errorTypes = ['unhandledRejection', 'uncaughtException']
const signalTraps = ['SIGTERM', 'SIGINT', 'SIGUSR2']

errorTypes.forEach(type => {
  process.on(type, async () => {
    try {
      console.log(`process.on ${type}`)
      await producer.disconnect()
      process.exit(0)
    } catch (_) {
      process.exit(1)
    }
  })
})

signalTraps.forEach(type => {
  process.once(type, async () => {
    try {
      await producer.disconnect()
    } finally {
      process.kill(process.pid, type)
    }
  })
})