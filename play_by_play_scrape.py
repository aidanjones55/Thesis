import bs4 as BS
import requests
import pandas as pd
from time import sleep

def date_convert_for_pbp(date):
    final = date.split('-')
    return ''.join(final) + '0'

def get_pbp_helper(suffix):
    #print(suffix)
    selector = f'#pbp'
    r = requests.get("https://www.basketball-reference.com/boxscores/pbp/{}.html".format(suffix))
    if r.status_code==200:
        soup = BS.BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', attrs={'id': 'pbp'})
        #print(table)
        return pd.read_html(str(table))[0]

def format_df(df1):
    df1.columns = list(map(lambda x: x[1], list(df1.columns)))
    t1 = list(df1.columns)[1].upper()
    t2 = list(df1.columns)[5].upper()
    q = 1
    df = None
    for index, row in df1.iterrows():
        d = {'QUARTER': float('nan'), 'TIME_REMAINING': float('nan'), f'{t1}_ACTION': float('nan'), f'{t2}_ACTION': float('nan'), f'{t1}_SCORE': float('nan'), f'{t2}_SCORE': float('nan')}
        if row['Time']=='2nd Q':
            q = 2
        elif row['Time']=='3rd Q':
            q = 3
        elif row['Time']=='4th Q':
            q = 4
        elif 'OT' in row['Time']:
            q = row['Time'][0]+'OT'
        try:
            d['QUARTER'] = [q]
            d['TIME_REMAINING'] = [row['Time']]
            scores = row['Score'].split('-')
            d[f'{t1}_SCORE'] = [int(scores[0])]
            d[f'{t2}_SCORE'] = [int(scores[1])]
            d[f'{t1}_ACTION'] = [row[list(df1.columns)[1]]]
            d[f'{t2}_ACTION'] = [row[list(df1.columns)[5]]]
            if df is None:
                df = pd.DataFrame(columns = list(d.keys()))
            df = pd.concat([df, pd.DataFrame.from_dict(d)], ignore_index=True)
        except:
            continue

    return df

def get_pbp(date, home):
    date_url = date_convert_for_pbp(date)
    date = pd.to_datetime(date)
    df = get_pbp_helper(date_url + home)
    #print(df)
    df = format_df(df)
    return df

#2017, 2018, , 2021


#years = [2017, 2018, 2019, 2020]
#years = [2015, 2016]

years = [2017]


for year in years:
    df = pd.read_csv(f'GameSchedules/NBA_Schedule_{year}.csv')
    for index, row in df.iterrows():
        try:
            #sleep(0.5)
            date = row['Date']
            home = row['Home Team']
            temp = get_pbp(date, home)
            filename = date_convert_for_pbp(date) + home
            print(f'{filename} Done')
            temp.to_csv(f'PlayByPlayData{year}/{filename}.csv')
        except:
            date = row['Date']
            home = row['Home Team']
            filename = date_convert_for_pbp(date) + home
            print(f'Failed On {filename}')








