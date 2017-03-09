from yahoo_oauth import OAuth1
import xmltodict
import pandas as pd
import argparse
import time

parser = argparse.ArgumentParser(description='weekly stats scraper')
parser.add_argument('-w', '--week', default=None)
parser.add_argument('-lid', '--league_id', required=True)

lid = parser.parse_args().league_id
if parser.parse_args().week is None:
	from os import listdir
	from os.path import isfile, join
	import numpy as np
	mypath = './weekly_stats/' + lid + '/'
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	week = str(np.max([int(x.split('.')[0]) for x in onlyfiles])+1)
else:
	week = parser.parse_args().week

oauth = OAuth1(None, None, from_file='yahoo_oauth1.json')
url = 'http://fantasysports.yahooapis.com/fantasy/v2/league/364.l.' + str(lid) + '/scoreboard;week=' + week
response = oauth.session.get(url)

data = xmltodict.parse(response.text)

df = []

for each in data['fantasy_content']['league']['scoreboard']['matchups']['matchup']:
	for next in each['teams']['team']:
		d = {}
		d['team_key'] = next['team_key']
		d['name'] = next['name']
		fgm, fga = next['team_stats']['stats']['stat'][0]['value'].split('/')
		d['fga'] = float(fga)
		d['fgm'] = float(fgm)
		ftm, fta = next['team_stats']['stats']['stat'][2]['value'].split('/')
		d['fta'] = float(fta)
		d['ftm'] = float(ftm)
		d['pts'] = float(next['team_stats']['stats']['stat'][5]['value'])
		d['reb'] = float(next['team_stats']['stats']['stat'][6]['value'])
		d['ast'] = float(next['team_stats']['stats']['stat'][7]['value'])
		d['stl'] = float(next['team_stats']['stats']['stat'][8]['value'])
		d['blk'] = float(next['team_stats']['stats']['stat'][9]['value'])
		d['tos'] = float(next['team_stats']['stats']['stat'][10]['value'])
		d['fgp'] = d['fgm']/d['fga']
		d['ftp'] = d['ftm']/d['fta']
		d['_3p'] = float(next['team_stats']['stats']['stat'][4]['value'])

		df_new = pd.DataFrame(d, index=[len(df)])
		df.append(df_new)

df = pd.concat(df)
df['week'] = week
df = df[['week', 'team_key', 'name', 'ftm', 'fta', 'ftp', 'fgm', 'fga', 'fgp', '_3p', 'pts', 'reb', 'ast', 'stl', 'blk', 'tos']]

up_cats = ['ftp', 'fgp', '_3p', 'pts', 'reb', 'ast', 'stl', 'blk']
down_cats = ['tos']

up_ranks = df[up_cats].rank(ascending=False).rename(columns={x: x + '_rank' for x in up_cats})
down_ranks = df[down_cats].rank(ascending=True).rename(columns={x: x + '_rank' for x in down_cats})

df = pd.concat([df, up_ranks, down_ranks], axis=1)

rank_cats = [x + '_rank' for x in up_ranks]

cats = ['ftp_rank', 'fgp_rank', '_3p_rank', 'pts_rank', 'reb_rank', 'ast_rank', 'stl_rank', 'blk_rank', 'tos_rank']

df['power_rank'] = df[cats].mean(axis=1)

df = df.sort_values('power_rank')

df.to_csv('./weekly_stats/' + str(lid) + '/' + week + '.csv', encoding='utf-8')