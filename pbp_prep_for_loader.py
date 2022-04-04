import pandas as pd
from util import get_action_dict


def date_convert_for_pbp(date):
    final = date.split('-')
    return ''.join(final) + '0'

def string_time_convert(str_time):
    temp = str_time.split(':')
    #print(temp)
    return int(temp[0])*60 + int(temp[1].split('.')[0])

# Done: [2015, 2016, 2017, 2018, 2019, 2020]

years = [2017]

for year in years:
    schedule = pd.read_csv(f'GameSchedules/NBA_Schedule_{year}.csv')
    clean_df = pd.DataFrame(
        columns=['Quarter', 'TimeRemaining', 'ScoreHome', 'ScoreAway', 'HomeTeam', 'AwayTeam', 'Duration',
                 'ActionTeam', 'PrimaryAction', 'SecondaryAction', 'ActionMetric', 'ActionResult', 'ScoreResult',
                 'PrimaryPlayer', 'SecondaryPlayer'])
    length = schedule.shape[0]
    pct = 0

    for index, row in schedule.iterrows():
        filename = date_convert_for_pbp(row['Date']) + row['Home Team']

        old_pct = pct
        pct = int(100 * (index / length))
        if pct % 5 == 0 and pct != old_pct:
            print(f'{pct}% done concat {year}')

        #Open CleanPBP Data
        try:
            pdb_clean = pd.read_csv(f'CleanPBP/{filename}.csv')
            clean_df = pd.concat([clean_df, pdb_clean], ignore_index=True)
        except:
            print(f'Skipping {filename}')

    clean_df.to_csv(f'ConcatPlayByPlay/cleabPBP{year}.csv')
