import pandas as pd
from util import get_action_dict

#Testing

def date_convert_for_pbp(date):
    final = date.split('-')
    return ''.join(final) + '0'

def string_time_convert(str_time):
    temp = str_time.split(':')
    #print(temp)
    return int(temp[0])*60 + int(temp[1].split('.')[0])


def convert_to_clean(year, filename, home, away):
    clean_df = pd.DataFrame(columns=['Quarter', 'TimeRemaining', 'ScoreHome', 'ScoreAway', 'HomeTeam', 'AwayTeam', 'Duration', 'ActionTeam', 'PrimaryAction', 'SecondaryAction', 'ActionMetric', 'ActionResult', 'ScoreResult', 'PrimaryPlayer', 'SecondaryPlayer'])

    df = pd.read_csv(f'PlayByPlayData{year}/{filename}.csv')
    old_cols = df.columns.tolist()
    #print(old_cols)
    prev_time = 720

    for index, row in df.iterrows():

        duration = prev_time - string_time_convert(row['TIME_REMAINING']) if prev_time - string_time_convert(row['TIME_REMAINING']) != 720 else 0
        if duration < 0:
            duration = 720 - string_time_convert(row['TIME_REMAINING'])


        add_row = {
            'Quarter': row['QUARTER'],
            'TimeRemaining': row['TIME_REMAINING'],
            'ScoreHome': row[old_cols[6]],
            'ScoreAway': row[old_cols[5]],
            'HomeTeam': home,
            'AwayTeam': away,
            'Duration': duration,
            'ActionTeam': 'home' if str(row[old_cols[4]]) != 'nan' else 'away'
        }

        prev_time = string_time_convert(row['TIME_REMAINING'])
        if prev_time == 0:
            prev_time = 720

        action_str = str(row[old_cols[4]]) if str(row[old_cols[4]]) != 'nan' else str(row[old_cols[3]])
        action, act_dict = get_action_dict(action_str)

        add_row.update(act_dict)
        #print(act_dict)
        if action == 'unknown':
            print(action_str)
            return False

        for key in add_row.keys():
            add_row[key] = [add_row[key]]

        clean_df = pd.concat([clean_df, pd.DataFrame.from_dict(add_row)], ignore_index=True)
    clean_df.to_csv(f'CleanPBP/{filename}.csv')

    return True


# Done: [2015, 2016, 2017, 2018, 2019, ]
for year in [2017]:
    df = pd.read_csv(f'GameSchedules/NBA_Schedule_{year}.csv')
    length = df.shape[0]
    pct = 0

    for index, row in df.iterrows():
        old_pct = pct
        pct = int(100*(index/length))
        if pct % 5 == 0 and pct != old_pct:
            print(f'{pct}% Done {year}')
        if pct < 0:
            continue
        filename = date_convert_for_pbp(row['Date']) + row['Home Team']
        home = row['Home Team']
        away = row['Away Team']
        if convert_to_clean(year, filename, home, away):
            continue
        else:
            break
    print(f'################ Done {year}! ################')

#convert_to_clean('2017', '201610250CLE', 'CLE', 'NKY')

#print(string_time_convert('12:00.0'))