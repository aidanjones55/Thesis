import bs4 as BS
import requests
import pandas as pd

#years = [2017, 2018, 2019, 2020, 2021]
#years = [2015, 2016]


month_dict = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

team_dict = {'Brooklyn Nets': 'BRK',
             'Milwaukee Bucks': 'MIL',
             'Boston Celtics': 'BOS',
             'New York Knicks': 'NYK',
             'Philadelphia 76ers': 'PHI',
             'Toronto Raptors': 'TOR',
             'Chicago Bulls': 'CHI',
             'Cleveland Cavaliers': 'CLE',
             'Detroit Pistons': 'DET',
             'Indiana Pacers': 'IND',
             'Atlanta Hawks': 'ATL',
             'Charlotte Hornets': 'CHO',
             'Miami Heat': 'MIA',
             'Orlando Magic': 'ORL',
             'Washington Wizards': 'WAS',
             'Denver Nuggets': 'DEN',
             'Minnesota Timberwolves': 'MIN',
             'Oklahoma City Thunder': 'OKC',
             'Portland Trail Blazers': 'POR',
             'Utah Jazz': 'UTA',
             'Golden State Warriors': 'GSW',
             'Los Angeles Clippers': 'LAC',
             'Los Angeles Lakers': 'LAL',
             'Phoenix Suns': 'PHO',
             'Sacramento Kings': 'SAC',
             'Dallas Mavericks': 'DAL',
             'Houston Rockets': 'HOU',
             'Memphis Grizzlies': 'MEM',
             'New Orleans Pelicans': 'NOP',
             'San Antonio Spurs': 'SAS'
             }

def date_formatter(date:str):
    date_split = date.split(', ')[1:]
    year = date_split[1]
    month = month_dict[date_split[0].split(' ')[0]]
    day = date_split[0].split(' ')[1]
    if len(day)==1:
        day = '0{}'.format(day)
    #print(date_split)
    return '{}-{}-{}'.format(year,month,day)

years = [2017]
#months = ['october', 'november', 'december', 'january', 'february', 'march', 'april']
months = ['april']

for year in years:
    schedule = pd.DataFrame(columns=['Date', 'Away Team', 'Home Team'])
    for month in months:
        print(f'Scraping {month}, {year}...')

        result = requests.get("https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html".format(year, month))
        src = result.content
        soup = BS.BeautifulSoup(src, 'lxml')

        for tables in soup.find_all('tbody'):
            for rows in tables.find_all('tr'):
                row = []
                for head in rows.find_all('th'):
                    if 'data-stat' in head.attrs.keys():
                        if head['data-stat'] == 'date_game':
                            row.append(date_formatter(head.text))
                for td in rows.find_all('td'):
                    if 'data-stat' in td.attrs.keys():
                        if td['data-stat'] == 'home_team_name':
                            row.append(team_dict[td.text])
                        if td['data-stat'] == 'visitor_team_name':
                            row.append(team_dict[td.text])

                if len(row) == 3:
                    df_length = len(schedule)
                    schedule.loc[df_length] = row

    schedule.to_csv(f'GameSchedules/NBA_Schedule_{year}.csv')
