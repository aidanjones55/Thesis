import pickle
import pandas as pd
import operator
import numpy as np
from util import one_hot_translate


def string_time_convert(str_time):
    temp = str_time.split(':')
    #print(temp)
    return int(temp[0])*60 + int(temp[1].split('.')[0])

def convert_to_onehot(tup):
    return one_hot_translate[tup]

def normalize_time_left(num):
    return round(num/720, 4)

def normalize_duration(num):
    return round(min(1.0, num/24), 4)

def gen_one_hot_v1(year):
    concat_file = pd.read_csv(f'ConcatPlayByPlay/cleabPBP{year}.csv')

    concat_file[['PrimaryAction', 'SecondaryAction', 'ActionResult', 'ScoreResult']] = concat_file[['PrimaryAction', 'SecondaryAction', 'ActionResult', 'ScoreResult']].fillna(value=-1)
    concat_file['TimeRemaining'] = concat_file.apply(lambda row: string_time_convert(row['TimeRemaining']), axis=1)
    concat_file['TimeRemaining'] = concat_file.apply(lambda row: normalize_time_left(row['TimeRemaining']), axis=1)
    concat_file['Duration'] = concat_file.apply(lambda row: normalize_duration(row['Duration']), axis=1)
    concat_file['Action'] = concat_file.apply(lambda row: convert_to_onehot((str(row['PrimaryAction']), str(row['SecondaryAction']), str(row['ActionResult']), str(int(row['ScoreResult'])))), axis=1)

    team_one_hot = pd.get_dummies(concat_file.ActionTeam, prefix='Team')

    final = concat_file[['HomeTeam', 'AwayTeam', 'ScoreHome', 'ScoreAway', 'Quarter', 'TimeRemaining', 'Duration', 'Action']]
    final = pd.concat([final, team_one_hot], axis=1)

    final.to_csv(f'Embed_For_Training_V1/EMBED_{year}.csv')
    return True

gen_one_hot_v1(2015)