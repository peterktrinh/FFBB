import pandas as pd
import datetime as dt
import json
import glob
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='compute power rank.')
parser.add_argument('-w', '--week', default=None)
parser.add_argument('-lid', '--league_id', required=True)

lid = parser.parse_args().league_id
if parser.parse_args().week is None:
	from os import listdir
	from os.path import isfile, join
	import numpy as np
	mypath = './weekly_stats/' + lid + '/'
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	week = str(np.max([int(x.split('.')[0]) for x in onlyfiles]))
else:
	week = parser.parse_args().week


week_ranks = glob.glob('./weekly_stats/' + str(lid) + '/*.csv')
ranks = []
for file in week_ranks[0:int(week)]:
    ranks_new = pd.read_csv(file,index_col=None, header=0, encoding='utf-8')
    ranks.append(ranks_new)

ranks = pd.concat(ranks)

cats = ['ftp_rank', 'fgp_rank', '_3p_rank', 'pts_rank', 'reb_rank', 'ast_rank', 'stl_rank', 'blk_rank', 'tos_rank']

df = ranks[['team_key', 'name'] + cats].groupby('team_key').mean()

df['power_rank'] = df[cats].mean(axis=1)

df['name'] = ranks_new.set_index('team_key')['name']

df = df[['name'] + cats + ['power_rank']]

df = df.sort_values('power_rank')

df.to_csv('./power_rank/' + str(lid) + '/' + week + '.csv', encoding='utf-8')
