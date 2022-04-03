import bs4 as BS
import requests
import pandas as pd

projected = pd.DataFrame(columns = ['R#', 'ADP', 'PLAYER', 'POS', 'GP', 'GP', 'MPG', 'FG%', 'FGDiv', 'FT%', 'FTDiv', '3PM', 'PTS', 'TREB', 'AST', 'STL', 'BLK', 'TO', 'TOTAL'])

with open('projected.html', 'r') as f:

    contents = f.read()

    soup = BS.BeautifulSoup(contents, 'lxml')

    count = -1
    for tr in soup.find_all('tr'):
        count += 1
        if count != 0:
            row = []
            print(f'Player: {count}')
            for td in tr.find_all('td'):
                txt = td.text.strip()
                row.extend(txt.split('\n\n'))
            if len(row) == 19:
                df_length = len(projected)
                projected.loc[df_length] = row

projected.to_csv('projected_stats.csv')