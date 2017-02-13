from yahoo_oauth import OAuth1
import xmltodict
import pandas as pd
import time
oauth = OAuth1(None, None, from_file='yahoo_oauth1.json')
url = 'http://fantasysports.yahooapis.com/fantasy/v2/league/364.l.8091/transactions'
response = oauth.session.get(url)

data = xmltodict.parse(response.text)

transactions = data['fantasy_content']['league']['transactions']['transaction']

columns = ['timestamp','team','type','last_name','first_name','position','team']
rows_list = []
for trans in transactions:
    if (trans['status'] == 'successful') & (trans['type'] in {'add/drop'}):
        for player_trans in trans['players']['player']:
             d = {}
             d['last_name'] = player_trans['name']['last']
             d['first_name'] = player_trans['name']['first']
             d['position'] = player_trans['display_position']
             d['type'] = player_trans['transaction_data']['type']
             if d['type'] == 'add':
                 d['team'] = player_trans['transaction_data']['destination_team_name']
                 d['team_key'] = player_trans['transaction_data']['destination_team_key']
             elif d['type'] == 'drop':
                 d['team'] = player_trans['transaction_data']['source_team_name']
                 d['team_key'] = player_trans['transaction_data']['source_team_key']
             d['timestamp'] = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime(float(trans['timestamp'])))
             d['date'] = time.strftime("%Y-%m-%d",time.localtime(float(trans['timestamp'])))
             rows_list.append(d)
    elif (trans['status'] == 'successful') & (trans['type'] in {'add','drop'}):
        d = {}
        d['last_name'] = trans['players']['player']['name']['last']
        d['first_name'] = trans['players']['player']['name']['first']
        d['position'] = trans['players']['player']['display_position']
        d['type'] = trans['players']['player']['transaction_data']['type']
        if d['type'] == 'add':
            d['team'] = trans['players']['player']['transaction_data']['destination_team_name']
            d['team_key'] = trans['players']['player']['transaction_data']['destination_team_key']
        elif d['type'] == 'drop':
            d['team'] = trans['players']['player']['transaction_data']['source_team_name']
            d['team_key'] = trans['players']['player']['transaction_data']['source_team_key']
        d['timestamp'] = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime(float(trans['timestamp'])))
        d['date'] = time.strftime("%Y-%m-%d",time.localtime(float(trans['timestamp'])))
        rows_list.append(d)

df = pd.DataFrame(rows_list)
df.to_csv('./transactions/transactions.csv',index=False,sep=',', encoding='utf-8')