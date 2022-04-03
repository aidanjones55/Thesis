import bs4 as BS
import requests
import pandas as pd
import os

positions_away_dict = {
    0:'A0',
    1:'A1',
    2:'A2',
    3:'A3',
    4:'A4'
}

positions_home_dict = {
    0:'H0',
    1:'H1',
    2:'H2',
    3:'H3',
    4:'H4'
}

def name_to_short(name):

    short = name.split(',')
    shorthand = '{}. {}'.format(short[1][0], short[0])

    return shorthand


def get_starters(away_team, home_team, date):

    game_excel = '{}_{}_at_{}.xlsx'.format(date, away_team, home_team)
    path = "C:/Users/aidan/PycharmProjects/BBallBetting/venv/2020_games/"
    game_file = os.path.join(path, game_excel)
    game = pd.read_excel(game_file)

    game_start = requests.get("https://www.basketball-reference.com/boxscores/{}0{}.html".format(date, home_team))
    src = game_start.content
    soup = BS.BeautifulSoup(src, 'lxml')

    away_starters = []
    home_starters = []

    for rows in soup.find_all('table'):
        if rows.attrs['id'] == 'box-{}-game-basic'.format(away_team):
            for body in rows.find_all('tbody'):
                accum = 0
                for row in body.find_all('th'):
                    if 'csk' in list(row.attrs.keys()) and accum < 5:
                        away_starters.append(name_to_short(row['csk']))
                        accum += 1

    for rows in soup.find_all('table'):
        if rows.attrs['id'] == 'box-{}-game-basic'.format(home_team):
            for body in rows.find_all('tbody'):
                accum = 0
                for row in body.find_all('th'):
                    #print(list(row.attrs.keys()))
                    if 'csk' in list(row.attrs.keys()) and accum < 5:
                        home_starters.append(name_to_short(row['csk']))
                        accum += 1

    away_starters.sort(key=lambda x: x[3])
    home_starters.sort(key=lambda x: x[3])

    game.loc[0, 'A0'] = away_starters[0]
    game.loc[0, 'A1'] = away_starters[1]
    game.loc[0, 'A2'] = away_starters[2]
    game.loc[0, 'A3'] = away_starters[3]
    game.loc[0, 'A4'] = away_starters[4]

    game.loc[0, 'H0'] = home_starters[0]
    game.loc[0, 'H1'] = home_starters[1]
    game.loc[0, 'H2'] = home_starters[2]
    game.loc[0, 'H3'] = home_starters[3]
    game.loc[0, 'H4'] = home_starters[4]

    if 'Away Starters' in game.columns.tolist():
        game.drop(columns=['Away Starters', 'Home Starters'], inplace=True)

    populate_players(game)
    populate_players(game)

    game.to_excel(game_file, index=False)

    return(True)


def play_scrape(away_team, home_team, date):

    columns = ['Time','Away','Away Score', 'Score', 'Home Score', 'Home']

    df = pd.DataFrame(columns= columns)

    result = requests.get("https://www.basketball-reference.com/boxscores/pbp/{}0{}.html".format(date, home_team))
    src = result.content
    soup = BS.BeautifulSoup(src, 'lxml')
    table = soup.find_all('tbody')

    accum = 0

    for rows in soup.find_all('tr'):

        if list(rows.attrs.keys()) == []:
            count = 0
            play = []

            for cells in rows.find_all('td'):
                action = str(cells.text) if str(cells.text) != '\xa0' else ''
                play.append(action)

            if len(play) == 6:
                df.loc[accum] = play

        accum += 1

    print('{}_{}_at_{}.xlsx'.format(date, away_team, home_team))

    df.to_excel('{}_{}_at_{}.xlsx'.format(date, away_team, home_team), index=False)

    return True

def scrape_by_date(start, end, year):

    schedule = pd.read_excel('Schedule_{}.xlsx'.format(year))

    for i in range(0, schedule.shape[0]):
        if int(schedule.loc[i][0]) < end and int(schedule.loc[i][0]) > start:
            play_scrape(schedule.loc[i][1], schedule.loc[i][2], schedule.loc[i][0])

    return True

def populate_players(data_frame):

    for i in range(1, data_frame.shape[0]):

        if type(data_frame.iloc[i, 1]) is str:
            play = data_frame.iloc[i, 1]
            play = play.split(' ')

            if 'enters' in play:
                sub_in = '{} {}'.format(play[0],play[1])
                sub_out = '{} {}'.format(play[-2],play[-1])

                for j in range(0,5):
                    if data_frame.loc[i, positions_away_dict[j]] == sub_out:
                        data_frame.loc[i, positions_away_dict[j]] = sub_in

                    else:
                        data_frame.loc[i, positions_away_dict[j]] = data_frame.loc[i-1, positions_away_dict[j]]
            else:
                for j in range(0,5):
                    data_frame.loc[i, positions_away_dict[j]] = data_frame.loc[i - 1, positions_away_dict[j]]

        else:
            for j in range(0, 5):
                data_frame.loc[i, positions_away_dict[j]] = data_frame.loc[i - 1, positions_away_dict[j]]

        if type(data_frame.iloc[i, 5]) is str:
            play = data_frame.iloc[i, 5]
            play = play.split(' ')

            if 'enters' in play:
                sub_in = '{} {}'.format(play[0], play[1])
                sub_out = '{} {}'.format(play[-2], play[-1])

                for j in range(0, 5):
                    if data_frame.loc[i, positions_home_dict[j]] == sub_out:
                        data_frame.loc[i, positions_home_dict[j]] = sub_in

                    else:
                        data_frame.loc[i, positions_home_dict[j]] = data_frame.loc[i - 1, positions_home_dict[j]]
            else:
                for j in range(0, 5):
                    data_frame.loc[i, positions_home_dict[j]] = data_frame.loc[i - 1, positions_home_dict[j]]

        else:
            for j in range(0, 5):
                data_frame.loc[i, positions_home_dict[j]] = data_frame.loc[i - 1, positions_home_dict[j]]

def add_starters(year):

    path = "C:/Users/aidan/PycharmProjects/BBallBetting/venv/{}_games/".format(year)

    for games in os.listdir(path):
        game = games.split('_')
        game.pop(2)
        game[2] = game[2][:3]

        get_starters(game[1], game[2], game[0])
        print('Updated Game {} at {}, {}'.format(game[1], game[2], game[0]))

    return True

add_starters(2020)
