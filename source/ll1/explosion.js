const mqtt = require('mqtt');
const fs = require('fs');
const path = require('path');
const MongoClient = require('mongodb').MongoClient;
const url = "mongodb://localhost:27017/"; 


const ip = require('ip')


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
});

const { Kafka, CompressionTypes, logLevel } = require('kafkajs')

//const host = process.env.HOST_IP || ip.address()

const kafka = new Kafka({
  logLevel: logLevel.DEBUG,
  brokers: [`precinct.eng.it:9093`],
  clientId: 'example-producer',
  ssl: {
    rejectUnauthorized: false,
    ca: [fs.readFileSync('/home/montimage/vinh/MON/MON.crt', 'utf-8')],
    key: fs.readFileSync('/home/montimage/vinh/MON/MON.private_key.pem', 'utf-8'),
    cert: fs.readFileSync('/home/montimage/vinh/MON/MON.crt', 'utf-8')
  },
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

const topic = 'MMT-RCA-LL1-S1-T0'

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
			    				"category":"TechnologicalAccidents#Explosion",
								"node_id": 37,
			    				"startTS":TimeStamp,
								"locationData": {
								"geometryType": "Point",
            							"coordinatePairs": [
                							46.05873518,
                							14.50652707 
            							]
								},
								"includedData": [ 
            							{
                							"type": "SensorDataPackage", 
                							"source": {
                    							"sourceId": "37", 
                    							"deviceSourceType": "MQTT-feeds" 
                							},
                							"measurements": [ 
                    								{
                        								"src_host": "89.143.231.146",
														"dst_host": "45.80.24.27",
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
					
				var report3 = {
					"ServiceID":109102,
					"Root":{
						"Gateway":gw,
						"Source":0,
						"TimeStamp":TimeStamp},
					"Nodes":[{
						"Safety":true,
						"NodeID":1,
						"TimeStamp":TimeStamp,
						"TimeAccuracy":TimeAccuracy,
						"Sensors-Actuators":[
							{
							"SensorID":3333,
							"TimeStamp":TimeStamp,
							"TimeAccuracy":TimeAccuracy,
							"Resources":{
								"5506":doc["Created"]}
							},
							{
							"SensorID":3341,
							"TimeStamp":TimeStamp,
							"TimeAccuracy":TimeAccuracy,
							"Resources":{
								"5527": doc["KnownIncidentID"]
									}
							},
							{
							"SensorID":3341,
							"TimeStamp":TimeStamp,
							"TimeAccuracy":TimeAccuracy,
							"Resources":{
								"5527": doc["Description"]
									}
							},
							{
							"SensorID":3300,
							"TimeStamp":TimeStamp,
							"TimeAccuracy":TimeAccuracy,
							"Resources":{
								//"5700": doc["Similarity score"]
								"5700": generateRandomNumber(85, 89)
								}
							},
							{
							"SensorID":3341,
							"TimeStamp":TimeStamp,
							"TimeAccuracy":TimeAccuracy,
							"Resources":{
								"5527": doc["Proof"]
									}
							},
							{
							"SensorID":3333,
							"TimeStamp":TimeStamp,
							"TimeAccuracy":TimeAccuracy,
							"Resources":{
								"5506":doc["Created"]
								}
							}
							],
							"CRC":3285226955}],
						"CRC":2986263130
						};
			
			       console.log(JSON.stringify(report));
			    	//sendMessage(report);
					client.publish('109/102/0/0/124/100/100/0/0', JSON.stringify(report3));
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
  setInterval(report_to_broker, 8000) //report every 8 seconds
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
