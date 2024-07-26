# AI4TRIAGE dashboard (frontend)

### Install docker if needed:  
For example with Ubuntu:  

$ sudo apt-get install docker.io 

### Pull the docker image from Docker Hub:  
$ sudo docker pull vinhhoala/mmt-rca   

### AI4TRIAGE configuration (flows, dashboards, tabs, MQTT broker, etc., ):  

$ git clone https://github.com/Montimage/AI4TRIAGE.git
$ cd AI4TRIAGE/GUI  

$ cp -rf ai4triage-node-red-data /home/<user_name>/  

E.g., cp -rf ai4triage-node-red-data /home/ubuntu/

### Run the docker container and name it mmt-rca:  
$ sudo docker run -it -p 8080:1880 -v /home/<user_name>/ai4triage-node-red-data:/data --name ai4triage vinhhoala/mmt-rca  
  
NOTE: The repository ai4triage-node-red-data contains the configuration files for AI4TRIAGE and needs to be mounted to /data of the docker container. It is necessary to mount an absolute path (e.g., /home/ubuntu/ai4triage-node-red-data)

Interupt by CTRL + C then restart the container: 
$ sudo docker start ai4triage 

From now on to start and stop ai4triage:  
$ sudo docker <start/stop> ai4triage 

### View the dashboards:
http://<docker_host>:8080/ui  
E.g., http://localhost:8080/ui

### Note:  
By default the flows are pre-configured to receive data feeding by the 5G-IoT Industrial Campus of Montimage.  
Depending on the use case, re-configuration will be needed to integrate new data flows.  






