#!/bin/bash

cd ~/Dropbox/FFBB/data_scraper/

echo $PATH

python transactions_scraper.py
python roster_scraper.py
python fee_calculator.py

echo $PATH