#!/bin/bash

python transactions_scraper.py -st $1
python roster_scraper.py -st $1
python fee_calculator.py

python weekly_stats_scraper.py -w $2
python power_ranker.py -w $2