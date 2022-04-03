import pandas as pd
from util import get_action_dict

#Testing

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
            break

        for key in add_row.keys():
            add_row[key] = [add_row[key]]

        clean_df = pd.concat([clean_df, pd.DataFrame.from_dict(add_row)], ignore_index=True)
    clean_df.to_csv('testing.csv')

    return True


#if row[old_cols[6]]

#for year in [2017, 2018, 2019, 2020]:
#    df = pd.read_csv(f'GameSchedules/NBA_Schedule_{year}.csv')

convert_to_clean('2017', '201610250CLE', 'CLE', 'NKY')

#print(string_time_convert('12:00.0'))