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
  feed_statistics ();
});
const generateRandomNumber = (min, max) =>  {
	return Math.floor(Math.random() * (max - min) + min);
	  };
function feed_statistics(gw, TimeStamp, TimeAccuracy){
	MongoClient.connect(url, function(err, db) { //insert to the database of raw data real time
		if (err) return 0; 
		var dbo = db.db("industrial_campus_2022_2_15_19");
		dbo.collection('hardware', function(err, collection) {
			  collection
			    //.find()
				.aggregate([ { $sample: { size: 1 } } ]) //1 random sample 
			    //.sort({$natural: -1})
			    .limit(1)
			    .next()
			    .then(
			      function(doc) {
				  	console.log(doc);
			    	client.publish('109/101/0/0/500/100/101/0/0', JSON.stringify(doc))
			      },
			      function(err) {
			        console.log('Error:', err);
			      }
			    );
			});
			dbo.collection('security', function(err, collection) {
				collection
				  //.find()
				  .aggregate([ { $sample: { size: 1 } } ]) //1 random sample 
				  //.sort({$natural: -1})
				  .limit(1)
				  .next()
				  .then(
					function(doc) {
					  console.log(doc);
					  client.publish('109/100/0/0/500/100/101/0/0', JSON.stringify(doc))
					},
					function(err) {
					  console.log('Error:', err);
					}
				  );
			  });
		db.close();
	});
	setTimeout(feed_statistics, 1000)
	return 1;
}




client.on('error', function (err) {
  console.error('[ERROR] Cannot connect to MQTT-BROKER\n', err);
});
