#!/bin/sh
<<<<<<< HEAD
#python sim_batch.py -c config/config2.json -p 55000 -v f -f ./config2.pickle >config2.log 2>&1 &
#python sim_batch.py -c config/config3.json -p 55000 -v f -f ./config3.pickle >config3.log 2>&1 &
#python sim_batch.py -c config/config4.json -p 55000 -v f -f ./paths/paths_2016-02-22.pickle >config4.log 2>&1 &
python sim_batch.py -c config/config6.json -p 55000 -v f -f ./config6.pickle >config6.log 2>&1 &
=======
#python sim_batch.py -c config/config3.json -p 55000 -v f >log1.log 2>&1 &
#python sim_batch.py -c config/config5.json -p 55000 -v f >log2.log 2>&1 &
#python sim_batch.py -c config/config6.json -p 55000 -v f >log3.log 2>&1 &
#python sim_batch.py -c config/config9.json -p 55000 -v f >log4.log 2>&1 &
python sim_batch.py -c config/config2.json -p 55000 -v f -f config2.pickle >config2.log 2>&1 &
python sim_batch.py -c config/config5.json -p 55000 -v f -f config5.pickle >config5.log 2>&1 &
python sim_batch.py -c config/config10.json -p 55000 -v f -f config10.pickle >config10.log 2>&1 &
>>>>>>> 5d5d8200db365eb69e4d2449ca0ddfc09c784e65
