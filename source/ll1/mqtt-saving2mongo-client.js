const mqtt = require('mqtt');
const fs = require('fs');
const path = require('path');
const MongoClient = require('mongodb').MongoClient;
const url = "mongodb://localhost:27017/";

const connConfig = {
  host: '34.255.17.2',
  port: 8886,
  username: 'lnguyen',
  password: 'Enact2019',
  rejectUnauthorized: false,
  ca: fs.readFileSync(path.join(__dirname,'indra-certs/Public-ca-chain.cert.pem')),
  cert: fs.readFileSync(path.join(__dirname,'indra-certs/lnguyen.cert.pem')),
  key: fs.readFileSync(path.join(__dirname,'indra-certs/lnguyen.key.pem')),
  protocol: 'mqtts'
};

const client = mqtt.connect(connConfig);

client.subscribe('#');
// client.publish('messages', 'Current time is: ' + new Date())
client.on("message", onMessageReceived);

function seconds_since_epoch(d){  
    return Math.floor( d / 1000 );  
} 

function onMessageReceived(topic, message) {
	var msg = JSON.parse(message.toString());
	var ServiceID = msg.ServiceID;
	//console.log('Service ID: ');
	//console.log(ServiceID);
	//console.log('Gateway ID: ');
	//console.log(msg.Root.Gateway);
	//console.log('Timestamp: ' + msg.Root.TimeStamp);
	//var ts_now = new Date();
        //var sec_now = seconds_since_epoch(ts_now);
        //console.log('Now: '+sec_now );
        //console.log(sec_now);
	if (ServiceID == 109100){ //Security Metadata 
		MongoClient.connect(url, function(err, db) {
			if (err) throw err; 
			var ts = new Date();
                        //console.log(ts.getFullYear(), ts.getMonth()+1, ts.getDate(), ts.getHours());                  
                        var sec = seconds_since_epoch(ts);
                        //console.log('Now: ');
                        //console.log(sec);
			var dbo = db.db("rca_its_" + ts.getFullYear().toString() + "_" + (ts.getMonth()+1).toString() + "_" + ts.getDate().toString() + "_" + ts.getHours().toString());
			dbo.collection("security").insertOne(msg, function(error, res) {
   			if (error) throw error;
   			//var report = {"ServiceID": 109102, "Created": "2020-09-03 16:46:10.165596", "Most similar event": {"ID":  "INCT_202092163626998737", "description": "Gateway XXX failure", "similarity_score" : "0.983745998486"}, "Proof": msg, "Confidence": 1000, "Updated": "2020-09-01 16:46:10.165596"}; 
   			//var report = {"ServiceID":109102,"Root":{"Gateway":0,"Source":0,"TimeStamp":sec},"Nodes":[{"Safety":true,"NodeID":1,"TimeStamp":1536230850,"TimeAccuracy":143567890,"Sensors-Actuators":[{"SensorID":3333,"TimeStamp":1536230220,"TimeAccuracy":143567890,"Resources":{"5506":1600243082}},{"SensorID":3341,"TimeStamp":1536780450,"TimeAccuracy":143567890,"Resources":{"5527":"Indicent identification"}},{"SensorID":3341,"TimeStamp":1536780450,"TimeAccuracy":143567890,"Resources":{"5527":"Indicent description"}},{"SensorID":3300,"TimeStamp":1536230330,"TimeAccuracy":143567890,"Resources":{"5700":0.983745998486}},{"SensorID":3341,"TimeStamp":1536780450,"TimeAccuracy":143567890,"Resources":{"5527":"Proof description"}},{"SensorID":3333,"TimeStamp":1536230220,"TimeAccuracy":143567890,"Resources":{"5506":1600243082}}],"CRC":3285226955}],"CRC":2986263130};
   			//console.log(sec);
			//console.log(report);
			//console.log(JSON.stringify(report));
   			//client.publish('109/102/0/0/124/100/100/0/0', JSON.stringify(report))
			//console.log(msg);
			});
			db.close();
		});
	}
	else if (ServiceID == 109101){ //Hardware Metadata
		MongoClient.connect(url, function(err, db) {
			if (err) throw err; 
			var ts = new Date();
                        //console.log(ts.getFullYear(), ts.getMonth()+1, ts.getDate(), ts.getHours());                  
                        var sec = seconds_since_epoch(ts);
                        //console.log('Now: ');
                        //console.log(sec);
                        var dbo = db.db("rca_its_" + ts.getFullYear().toString() + "_" + (ts.getMonth()+1).toString() + "_" + ts.getDate().toString() + "_" + ts.getHours().toString());
			dbo.collection("hardware").insertOne(msg, function(error, res) {
   			if (error) throw error;
   			//var report = {"ServiceID": 109102, "Created": "2020-09-03 16:46:10.165596", "Most similar event": {"ID":  "INCT_202092163626998737", "description": "Gateway XXX failure", "similarity_score" : "0.983745998486"}, "Proof": msg, "Confidence": 1000, "Updated": "2020-09-01 16:46:10.165596"}; 
   			//var report = {"ServiceID":109102,"Root":{"Gateway":0,"Source":0,"TimeStamp":sec},"Nodes":[{"Safety":true,"NodeID":1,"TimeStamp":1536230850,"TimeAccuracy":143567890,"Sensors-Actuators":[{"SensorID":3333,"TimeStamp":1536230220,"TimeAccuracy":143567890,"Resources":{"5506":1600243082}},{"SensorID":3341,"TimeStamp":1536780450,"TimeAccuracy":143567890,"Resources":{"5527":"Indicent identification"}},{"SensorID":3341,"TimeStamp":1536780450,"TimeAccuracy":143567890,"Resources":{"5527":"Indicent description"}},{"SensorID":3300,"TimeStamp":1536230330,"TimeAccuracy":143567890,"Resources":{"5700":0.983745998486}},{"SensorID":3341,"TimeStamp":1536780450,"TimeAccuracy":143567890,"Resources":{"5527":"Proof description"}},{"SensorID":3333,"TimeStamp":1536230220,"TimeAccuracy":143567890,"Resources":{"5506":1600243082}}],"CRC":3285226955}],"CRC":2986263130};
   			//client.publish('109/102/0/0/124/100/100/0/0', JSON.stringify(report))
//			console.log("1 document inserted");
			});
			db.close();
		});
	}
	else if (ServiceID == 100999){ //Operation Status and Heartbeat
		MongoClient.connect(url, function(err, db) {
			if (err) throw err; 
			var ts = new Date();
                        //console.log(ts.getFullYear(), ts.getMonth()+1, ts.getDate(), ts.getHours());                  
                        var sec = seconds_since_epoch(ts);
                        //console.log('Now: ');
                        //console.log(sec);
                        var dbo = db.db("rca_its_" + ts.getFullYear().toString() + "_" + (ts.getMonth()+1).toString() + "_" + ts.getDate().toString() + "_" + ts.getHours().toString());
			dbo.collection("operation").insertOne(msg, function(error, res) {
   			if (error) throw error;
   			//var report = {"ServiceID": 109102, "Created": "2020-09-03 16:46:10.165596", "Most similar event": {"ID":  "INCT_202092163626998737", "description": "Gateway XXX failure", "similarity_score" : "0.983745998486"}, "Proof": msg, "Confidence": 1000, "Updated": "2020-09-01 16:46:10.165596"}; 
   			//var report = {"ServiceID":109102,"Root":{"Gateway":0,"Source":0,"TimeStamp":sec},"Nodes":[{"Safety":true,"NodeID":1,"TimeStamp":1536230850,"TimeAccuracy":143567890,"Sensors-Actuators":[{"SensorID":3333,"TimeStamp":1536230220,"TimeAccuracy":143567890,"Resources":{"5506":1600243082}},{"SensorID":3341,"TimeStamp":1536780450,"TimeAccuracy":143567890,"Resources":{"5527":"Indicent identification"}},{"SensorID":3341,"TimeStamp":1536780450,"TimeAccuracy":143567890,"Resources":{"5527":"Indicent description"}},{"SensorID":3300,"TimeStamp":1536230330,"TimeAccuracy":143567890,"Resources":{"5700":0.983745998486}},{"SensorID":3341,"TimeStamp":1536780450,"TimeAccuracy":143567890,"Resources":{"5527":"Proof description"}},{"SensorID":3333,"TimeStamp":1536230220,"TimeAccuracy":143567890,"Resources":{"5506":1600243082}}],"CRC":3285226955}],"CRC":2986263130};
   			//client.publish('109/102/0/0/124/100/100/0/0', JSON.stringify(report))
//			console.log("1 document inserted");
			});
			db.close();
		});
	}
}
/*client.on('connect', function () {
  console.log('Connected');
});
*/
client.on('error', function (err) {
  console.error('[ERROR] Cannot connect to MQTT-BROKER\n', err);
});
