from yahoo_oauth import OAuth1
import xmltodict
import pandas as pd
import argparse
import datetime as dt

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-st', '--start_date', required=True)

_YEAR_TO_KEY = {2001: 16, 2002: 67, 2003: 95, 2004: 112, 2005: 131, 2006: 165,
				2007: 187, 2008: 211, 2009: 234, 2010: 249, 2011: 265, 2012: 304,
				2015: 353, 2016: 364} #2013: 'x', 2014: 'y',

start_date = parser.parse_args().start_date
end_date = (dt.datetime.today() - dt.timedelta(1)).strftime('%Y-%m-%d')

dates = pd.date_range(start=start_date, end=end_date)

oauth = OAuth1(None, None, from_file='yahoo_oauth1.json')

# Get 250 players
for date in dates:

	date = date.strftime('%Y-%m-%d')

	teams = range(1,15,1)

	rosters = []

	for team in teams:
		url = 'http://fantasysports.yahooapis.com/fantasy/v2/team/364.l.8091.t.' + str(team) + '/roster;date=' + date
		response = oauth.session.get(url)
		data = xmltodict.parse(response.text)
		count = data['fantasy_content']['team']['roster']['players']['@count']
		for each in xrange(int(count)):
			d = {}
			d['pid'] = data['fantasy_content']['team']['roster']['players']['player'][each]['player_id']
			d['name'] = data['fantasy_content']['team']['roster']['players']['player'][each]['name']['full']
			d['roster_spot'] = data['fantasy_content']['team']['roster']['players']['player'][each]['selected_position']['position']
			d['date'] = date
			d['team_key'] = data['fantasy_content']['team']['team_key']
			d['team_name'] = data['fantasy_content']['team']['name']

			df_new = pd.DataFrame(d, index=[len(rosters)])
			rosters.append(df_new)

	df = pd.concat(rosters)

	df.to_csv('./roster/' + date + '.csv', index=False, encoding='utf-8')