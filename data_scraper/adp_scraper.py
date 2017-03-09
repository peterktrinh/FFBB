from yahoo_oauth import OAuth1
import xmltodict
import pandas as pd
import time

_YEAR_TO_KEY = {2001: 16, 2002: 67, 2003: 95, 2004: 112, 2005: 131, 2006: 165,
				2007: 187, 2008: 211, 2009: 234, 2010: 249, 2011: 265, 2012: 304,
				2015: 353, 2016: 364} #2013: 'x', 2014: 'y', 


oauth = OAuth1(None, None, from_file='yahoo_oauth1.json')

# Get 250 players

starts = range(1,  626, 25)

players = []

for start in starts:
	url = 'http://fantasysports.yahooapis.com/fantasy/v2/league/364.l.8091/players;start=' + str(start)
	response = oauth.session.get(url)
	data = xmltodict.parse(response.text)
	players = players + ([player['player_key'] for player in data['fantasy_content']['league']['players']['player']])

df = []

for player in players:
	url = 'http://fantasysports.yahooapis.com/fantasy/v2/player/' + player + '/draft_analysis'
	response = oauth.session.get(url)
	data = xmltodict.parse(response.text)

	d = dict()

	d['name'] = data['fantasy_content']['player']['name']['full']
	d['pid'] = player

	if type(data['fantasy_content']['player']['eligible_positions']['position']) == type([]):
		pos = ",".join(data['fantasy_content']['player']['eligible_positions']['position'])
	else:
		pos = data['fantasy_content']['player']['eligible_positions']['position']
	d['pos'] = pos
	try:
		d['adp'] = float(data['fantasy_content']['player']['draft_analysis']['average_pick'])
		d['ave_round'] = float(data['fantasy_content']['player']['draft_analysis']['average_round'])
		d['ave_cost'] = float(data['fantasy_content']['player']['draft_analysis']['average_cost'])
		d['perc_drafted'] = float(data['fantasy_content']['player']['draft_analysis']['percent_drafted'])
	except ValueError:
		d['adp'] = 0
		d['ave_round'] = 0
		d['ave_cost'] = 0
		d['perc_drafted'] = 0

	df.append(pd.DataFrame(d, index=[len(df)]))

df = pd.concat(df)

df = df[['pid', 'adp', 'name', 'pos', 'ave_round', 'ave_cost', 'perc_drafted']]

df.sort_values('adp').to_csv('adp.csv', index=True)
