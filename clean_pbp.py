import pandas as pd

def string_time_convert(str_time):
    temp = str_time.split(':')
    #print(temp)
    return int(temp[0])*60 + int(temp[1].split('.')[0])

def get_action_dict(action_str):
    '''
    :param action_str:
    :return:
    'PrimaryAction': Score (2ptJS, 2ptLU,
    'SecondaryAction': Score (Assit),
    'ActionMetric': Distance to basket (ft)
    'ActionResult':
    'PrimaryPlayer':
    'SecondaryPlayer':
    '''
    primary_action_dict = {
        'layup': 'LU',
        'hook shot': 'HS',
        'jump shot': 'JS'
    }

    ret_dict = {}

    if 'Defensive rebound ' in action_str:
        ret_dict = {'ActionResult': 'DefReb', 'PrimaryAction': 'DefReb', 'PrimaryPlayer': action_str.split('by ')[-1]}
        return 'rebound', ret_dict

    if 'Offensive rebound ' in action_str:
        ret_dict = {'PrimaryAction': 'OffReb', 'PrimaryPlayer': action_str.split('by ')[-1]}
        return 'rebound', ret_dict

    if 'Turnover ' in action_str:
        ret_dict['ActionResult'] = 'turnover'
        temp = action_str.split(' by ')
        temp.pop(0)
        temp = temp[0]
        if ' (' in temp:
            temp = temp.split(' (')
        ret_dict['PrimaryPlayer'] = temp.pop(0)
        if 'lost ball' in temp[0]:
            temp = temp[0].split('lost ball')
            ret_dict['PrimaryAction'] = 'LostBall'
            if temp == ['', ')']:
                return 'turnover', ret_dict
        if 'offensive foul' in temp[0]:
            temp = temp[0].split('offensive foul')
            ret_dict['PrimaryAction'] = 'OffensiveFoul'
            if temp == ['', ')']:
                return 'turnover', ret_dict


        #'PrimaryPlayer': action_str.split('by ')[-1]}
        #return 'turnover', ret_dict

    if '-pt' in action_str:
        if 'makes' in action_str:
            if '2-pt' in action_str:
                temp = action_str.split(' makes 2-pt ')
                ret_dict['PrimaryPlayer'] = temp.pop(0)
                ret_dict['ActionResult'] = 'make2'
                ret_dict['ScoreResult'] = '2'

                if ' from ' in temp[0]:
                    temp = temp[0].split(' from ')
                    ret_dict['PrimaryAction'] = primary_action_dict[temp.pop(0)]
                    if ' ft' in temp[0]:
                        temp = temp[0].split(' ft')
                        #print(temp)
                        ret_dict['ActionMetric'] = temp.pop(0)

                        if temp != []:
                            if 'assist' in temp[0]:
                                ret_dict['SecondaryAction'] = 'assist'
                                ret_dict['SecondaryPlayer'] = temp[0].split(' by ')[1][:-1]
                                return 'scoring', ret_dict
                    return 'scoring', ret_dict

                if ' at rim ' in temp[0]:
                    temp = temp[0].split(' at rim ')
                    ret_dict['PrimaryAction'] = primary_action_dict[temp.pop(0)]
                    ret_dict['ActionMetric'] = 0
                    if temp != []:
                        if 'assist' in temp[0]:
                            ret_dict['SecondaryAction'] = 'assist'
                            ret_dict['SecondaryPlayer'] = temp[0].split(' by ')[1][:-1]
                            return 'scoring', ret_dict
                    return 'scoring', ret_dict

            if '3-pt' in action_str:
                temp = action_str.split(' makes 3-pt ')
                ret_dict['PrimaryPlayer'] = temp.pop(0)
                ret_dict['ActionResult'] = 'make3'
                ret_dict['ScoreResult'] = '3'

                if ' from ' in temp[0]:
                    temp = temp[0].split(' from ')
                    ret_dict['PrimaryAction'] = primary_action_dict[temp.pop(0)]
                    if ' ft' in temp[0]:
                        temp = temp[0].split(' ft')
                        #print(temp)
                        ret_dict['ActionMetric'] = temp.pop(0)

                        if temp != []:
                            if 'assist' in temp[0]:
                                ret_dict['SecondaryAction'] = 'assist'
                                ret_dict['SecondaryPlayer'] = temp[0].split(' by ')[1][:-1]
                                return 'scoring', ret_dict
                    return 'scoring', ret_dict

        if 'misses' in action_str:
            if '2-pt' in action_str:
                temp = action_str.split(' misses 2-pt ')
                ret_dict['PrimaryPlayer'] = temp.pop(0)
                ret_dict['ActionResult'] = 'miss2'
                ret_dict['ScoreResult'] = '0'
                if ' from ' in temp[0]:
                    temp = temp[0].split(' from ')
                    ret_dict['PrimaryAction'] = primary_action_dict[temp.pop(0)]
                    if ' ft' in temp[0]:
                        temp = temp[0].split(' ft')
                        #print(temp)
                        ret_dict['ActionMetric'] = temp.pop(0)
                        return 'scoring', ret_dict

            if '3-pt' in action_str:
                temp = action_str.split(' misses 3-pt ')
                ret_dict['PrimaryPlayer'] = temp.pop(0)
                ret_dict['ActionResult'] = 'miss3'
                ret_dict['ScoreResult'] = '0'
                if ' from ' in temp[0]:
                    temp = temp[0].split(' from ')
                    ret_dict['PrimaryAction'] = primary_action_dict[temp.pop(0)]
                    if ' ft' in temp[0]:
                        temp = temp[0].split(' ft')
                        #print(temp)
                        ret_dict['ActionMetric'] = temp.pop(0)
                        return 'scoring', ret_dict

    if 'Offensive foul ' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'OffensiveFoul'
            temp = action_str.split(' by ')

            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            print(temp)
            ret_dict['PrimaryAction'] = 'OffensiveFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'turnover', ret_dict







    return 'unknown', ret_dict

def convert_to_clean(year, filename, home, away):
    clean_df = pd.DataFrame(columns=['Quarter', 'TimeRemaining', 'ScoreHome', 'ScoreAway', 'HomeTeam', 'AwayTeam', 'Duration', 'ActionTeam', 'PrimaryAction', 'SecondaryAction', 'ActionMetric', 'ActionResult', 'ScoreResult', 'PrimaryPlayer', 'SecondaryPlayer'])

    df = pd.read_csv(f'PlayByPlayData{year}/{filename}.csv')
    old_cols = df.columns.tolist()
    #print(old_cols)
    for index, row in df.iterrows():
        prev_time = 720

        add_row = {
            'Quarter': row['QUARTER'],
            'TimeRemaining': row['TIME_REMAINING'],
            'ScoreHome': row[old_cols[6]],
            'ScoreAway': row[old_cols[5]],
            'HomeTeam': home,
            'AwayTeam': away,
            'Duration': prev_time - string_time_convert(row['TIME_REMAINING']),
            'ActionTeam': 'home' if str(row[old_cols[4]]) != 'nan' else 'away'
        }

        action_str = str(row[old_cols[4]]) if str(row[old_cols[4]]) != 'nan' else str(row[old_cols[3]])
        action, act_dict = get_action_dict(action_str)
        print(act_dict)
        if action == 'unknown':
            print(action_str)
            break

        #print(str(row['CLEVELAND_ACTION']))
    return True


#if row[old_cols[6]]

#for year in [2017, 2018, 2019, 2020]:
#    df = pd.read_csv(f'GameSchedules/NBA_Schedule_{year}.csv')

convert_to_clean('2017', '201610250CLE', 'CLE', 'NKY')

#print(string_time_convert('12:00.0'))