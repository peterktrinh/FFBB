#!/bin/bash

cd ~/Dropbox/FFBB/data_scraper/

python weekly_stats_scraper.py -lid 8091
python power_ranker.py -lid 8091