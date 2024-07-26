const mqtt = require('mqtt');
const fs = require('fs');
const path = require('path');
const MongoClient = require('mongodb').MongoClient;
const url = "mongodb://localhost:27017/";

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
  //report_to_broker ();
});

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
			        console.log("Created: ", doc["Created"]);
			    	console.log("ID: ", doc["KnownIncidentID"]);
			    	console.log("Description: ", doc["Description"]);
			    	console.log("Similarity score: ", doc["Similarity score"]);
			    	console.log("Proof: ", doc["Proof"]);
			    	var report = {
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
			    						"5700": doc["Similarity score"]
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
			    	//console.log(report);
			    	client.publish('109/102/0/0/124/100/100/0/0', JSON.stringify(report))
			      },
			      function(err) {
			        console.log('Error:', err);
			      }
			    );
			});
		db.close();
	});
	setTimeout(report_to_broker, 1000)
	return 1;
}




client.on('error', function (err) {
  console.error('[ERROR] Cannot connect to MQTT-BROKER\n', err);
});

