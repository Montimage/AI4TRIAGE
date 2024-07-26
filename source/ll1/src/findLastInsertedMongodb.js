const mqtt = require('mqtt');
const fs = require('fs');
const path = require('path');
const MongoClient = require('mongodb').MongoClient;
const url = "mongodb://localhost:27017/";


MongoClient.connect(url, function(err, db) { //insert to the database of raw data real time
	if (err) throw err; 
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
		      },
		      function(err) {
		        console.log('Error:', err);
		      }
		    );
		});
});
