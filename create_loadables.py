import pandas as pd
from util import get_action_dict
import pickle



def date_convert_for_pbp(date):
    final = date.split('-')
    return ''.join(final) + '0'

def string_time_convert(str_time):
    temp = str_time.split(':')
    #print(temp)
    return int(temp[0])*60 + int(temp[1].split('.')[0])

years = [2015, 2016, 2017, 2018, 2019, 2020]

to_1_hot = {}
total_size = 0

for year in years:
    concat_file = pd.read_csv(f'ConcatPlayByPlay/cleabPBP{year}.csv')
    total_size += concat_file.shape[0]
    #print(concat_file.head(5))
    #print(concat_file.columns.tolist())
    concat_file.fillna(value=-1, method=None, axis=None, inplace=True, limit=None, downcast=None)
    temp = concat_file.groupby(['PrimaryAction', 'SecondaryAction', 'ActionResult', 'ScoreResult']).size().to_frame('size').reset_index(inplace=False)

    for index, row in temp.iterrows():
        ind = (row['PrimaryAction'], row['SecondaryAction'], row['ActionResult'], row['ScoreResult'])
        if not ind in to_1_hot.keys():
            to_1_hot[ind] = row['size']
        else:
            to_1_hot[ind] += row['size']

with open('to_1_hot.pickle', 'wb') as handle:
    pickle.dump(to_1_hot, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(len(to_1_hot))
print(total_size)

    #print(f'Done: {year}')

#print(to_1_hot)
#print(len(list(dict.fromkeys(to_1_hot))))
