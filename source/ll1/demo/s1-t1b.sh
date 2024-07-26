#!/bin/bash

#explosion 
python /home/montimage/vinh/root_cause_analysis/rca_tool/ll1_learning_inct_explosion.py industrial_campus_2022_2_15_14
python /home/montimage/vinh/root_cause_analysis/rca_tool/ll1_monitoring_critical.py & sleep 10; pkill python
node /home/montimage/vinh/root_cause_analysis/ll1/explosion.js

