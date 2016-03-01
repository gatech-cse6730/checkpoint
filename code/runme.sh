#!/bin/sh
python sim_batch.py -c config/config1.json -p 55000 -v f -f ./paths/paths_2016-02-22.pickle >log1.log 2>&1 &
python sim_batch.py -c config/config4.json -p 55000 -v f -f ./paths/paths_2016-02-22.pickle >log2.log 2>&1 &
python sim_batch.py -c config/config7.json -p 55000 -v f -f ./paths/paths_2016-02-22.pickle >log3.log 2>&1 &
python sim_batch.py -c config/config8.json -p 55000 -v f -f ./paths/paths_2016-02-22.pickle >log4.log 2>&1 &
python sim_batch.py -c config/config2.json -p 55000 -v f >log5.log 2>&1 &
