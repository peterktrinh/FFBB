import pandas as pd
import datetime as dt
import json
import glob
import numpy as np

config = json.loads(open('./config.json').read())
season_start_date = config['season_start_date']
playoff_start_date = config['playoff_start_date']
season_end_date = config['season_end_date']
league_fee = config['league_fee']
add_fee = config['add_fee']
playoff_add_fee = config['playoff_add_fee']
il_fee = config['il_fee']
il_days_per_fee = config['il_days_per_fee']

date = (dt.datetime.today() - dt.timedelta(1)).strftime('%Y-%m-%d')

df = pd.read_csv('./roster/' + date + '.csv').drop_duplicates('team_key').reset_index()[['team_key', 'team_name']]
df['reg_adds'] = 0
df['po_adds'] = 0
df['il_days'] = 0
df['free_add_from_trades'] = 0
transactions = pd.read_csv('./transactions/transactions.csv')

all_roster_files = glob.glob('./roster/*.csv')
rosters = []
for file in all_roster_files:
    roster_new = pd.read_csv(file,index_col=None, header=0)
    rosters.append(roster_new)

rosters = pd.concat(rosters).reset_index(drop=True)

il = rosters.query('roster_spot=="IL"')

df = df.set_index('team_key')

for team_key in df.index:
	df.ix[team_key, 'il_days'] = len(il.query('team_key==@team_key and date>=@season_start_date and date <=@season_end_date'))
	df.ix[team_key, 'reg_adds'] = len(transactions.query('team_key==@team_key and date>=@season_start_date and date<@playoff_start_date  and date <=@season_end_date and type=="add"'))
	df.ix[team_key, 'po_adds'] = len(transactions.query('team_key==@team_key and date>=@playoff_start_date  and date <=@season_end_date and type=="add"'))

players_out = transactions.query('type=="trade"').groupby(['transaction_id', 'to_team_key']).count()[['from_team_key']]
players_in = transactions.query('type=="trade"').groupby(['transaction_id', 'from_team_key']).count()[['to_team_key']]

trades = players_out
trades.columns = ['players_out']
trades['players_in'] = players_in['to_team_key']
trades.eval('credit = players_in - players_out', inplace=True)

trades['credit'][trades['credit']<=0] = 0

d = trades.reset_index().groupby('to_team_key').sum()['credit'].to_dict()

for team_key in df.index:
	try:
		df.ix[team_key, 'free_add_from_trades'] = d[team_key]
	except:
		df.ix[team_key, 'free_add_from_trades'] = 0

df.eval('league_fee = @league_fee', inplace=True)
df.eval('reg_add_fee = @add_fee * reg_adds', inplace=True)
df.eval('po_add_fee = @playoff_add_fee * po_adds', inplace=True)
df['il_fee_period_ceil'] = np.ceil(df['il_days']/7)
df.eval('il_fee = il_fee_period_ceil * @il_fee', inplace=True, truediv=False)
df.eval('trade_credit = @add_fee * (free_add_from_trades)', inplace=True, truediv=False)
df.eval('fees_accrued = il_fee + reg_add_fee + po_add_fee + league_fee - trade_credit', inplace=True)
df['date'] = date
df = df[['team_name', 'date', 'league_fee', 'reg_adds', 'po_adds', 'il_days', 'free_add_from_trades', 'reg_add_fee', 'po_add_fee', 'il_fee', 'trade_credit', 'fees_accrued']]
df.to_csv('fees_accrued.csv')