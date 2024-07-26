#!/bin/bash
#sudo mount /dev/sdb2 /media/usb
pkill node 
sleep 5
sudo service mongod start
sudo sleep 15

#traffic delayed
python /home/montimage/vinh/root_cause_analysis/rca_tool/ll1_learning_inct_traffic_delayed.py ll1_2023_04_24_09  
python /home/montimage/vinh/root_cause_analysis/rca_tool/ll1_monitoring_critical.py & sleep 60; pkill python
node /home/montimage/vinh/root_cause_analysis/ll1/traffic_delayed.js & sleep 120; pkill node
#forever start /home/montimage/vinh/root_cause_analysis/ll1/traffic_delayed.js & sleep 20; pkill node

#telecom and electricity affected
python /home/montimage/vinh/root_cause_analysis/rca_tool/ll1_learning_inct_telecom_electricity_affected.py ll1_2023_04_24_10 
python /home/montimage/vinh/root_cause_analysis/rca_tool/ll1_monitoring_critical.py & sleep 60; pkill python
node /home/montimage/vinh/root_cause_analysis/ll1/telecom_electricity.js & sleep 120; pkill node
#forever start /home/montimage/vinh/root_cause_analysis/ll1/telecom_electricity.js & sleep 20; pkill node

#critical services affected 
python /home/montimage/vinh/root_cause_analysis/rca_tool/ll1_learning_inct_critical_services.py ll1_2023_04_24_11
python /home/montimage/vinh/root_cause_analysis/rca_tool/ll1_monitoring_critical.py & sleep 60; pkill python
node /home/montimage/vinh/root_cause_analysis/ll1/critical_services.js & sleep 120; pkill node
#forever start /home/montimage/vinh/root_cause_analysis/ll1/critical_services.js & sleep 20; pkill node

#malware
python /home/montimage/vinh/root_cause_analysis/rca_tool/ll1_learning_inct_malware.py ll1_2023_04_24_12
python /home/montimage/vinh/root_cause_analysis/rca_tool/ll1_monitoring_critical.py & sleep 60; pkill python
node /home/montimage/vinh/root_cause_analysis/ll1/malware.js & sleep 120; pkill node
#forever start /home/montimage/vinh/root_cause_analysis/ll1/malware.js & sleep 20; pkill node


python /home/montimage/vinh/root_cause_analysis/rca_tool/ll1_learning_inct_DoS.py ll1_2023_04_24_13
python /home/montimage/vinh/root_cause_analysis/rca_tool/ll1_monitoring_critical.py & sleep 60; pkill python
node /home/montimage/vinh/root_cause_analysis/ll1/DoS.js 
#forever start /home/montimage/vinh/root_cause_analysis/ll1/DoS.js & sleep 120; pkill node

