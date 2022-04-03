import pandas as pd

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
        'jump shot': 'JS',
        'dunk': 'DK'
    }

    ret_dict = {
        'PrimaryAction': float('nan'),
        'SecondaryAction': float('nan'),
        'ActionMetric': float('nan'),
        'ActionResult': float('nan'),
        'ScoreResult': float('nan'),
        'PrimaryPlayer': float('nan'),
        'SecondaryPlayer': float('nan'),
    }

    if 'Defensive rebound ' in action_str:
        ret_dict['ActionResult'] = 'DefReb'
        ret_dict['PrimaryAction'] = 'DefReb'
        ret_dict['PrimaryPlayer'] = action_str.split('by ')[-1]
        return 'rebound', ret_dict

    if 'Offensive rebound ' in action_str:
        ret_dict['ActionResult'] = 'OffReb'
        ret_dict['PrimaryAction'] = 'OffReb'
        ret_dict['PrimaryPlayer'] = action_str.split('by ')[-1]

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
            if 'steal' in action_str:
                ret_dict['SecondaryPlayer'] = action_str.split('steal by ')[-1][:-1]
                ret_dict['SecondaryAction'] = 'steal'
                return 'turnover', ret_dict

        if 'offensive foul' in temp[0]:
            temp = temp[0].split('offensive foul')
            ret_dict['PrimaryAction'] = 'OffensiveFoul'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'step out of bounds' in temp[0]:
            temp = temp[0].split('step out of bounds')
            ret_dict['PrimaryAction'] = 'OutOfBounds'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'bad pass' in temp[0]:
            temp = temp[0].split('bad pass')
            ret_dict['PrimaryAction'] = 'BadPass'
            if 'steal' in action_str:
                ret_dict['SecondaryPlayer'] = action_str.split('steal by ')[-1][:-1]
                ret_dict['SecondaryAction'] = 'steal'
                return 'turnover', ret_dict
            else:
                return 'turnover', ret_dict

        if 'Turnover by Team (shot clock)' in action_str:
            ret_dict['PrimaryPlayer'] = 'Team'
            ret_dict['PrimaryAction'] = 'ShotClockViolation'
            ret_dict['ActionResult'] = 'turnover'
            return 'turnover', ret_dict

    if '-pt' in action_str:
        if 'makes' in action_str:
            if '2-pt' in action_str:
                temp = action_str.split(' makes 2-pt ')
                ret_dict['PrimaryPlayer'] = temp.pop(0)
                ret_dict['ActionResult'] = 'make2'
                ret_dict['ScoreResult'] = 2

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

                if ' at rim' in temp[0]:
                    temp = temp[0].split(' at rim')
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
                ret_dict['ScoreResult'] = 3

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
                ret_dict['ScoreResult'] = 0
                if ' from ' in temp[0]:
                    temp = temp[0].split(' from ')
                    ret_dict['PrimaryAction'] = primary_action_dict[temp.pop(0)]
                    if ' ft' in temp[0]:
                        temp = temp[0].split(' ft')
                        #print(temp)
                        ret_dict['ActionMetric'] = temp.pop(0)
                        return 'scoring', ret_dict

                if ' at rim' in temp[0]:
                    temp = temp[0].split(' at rim')
                    ret_dict['PrimaryAction'] = primary_action_dict[temp.pop(0)]
                    ret_dict['ActionMetric'] = 0
                    return 'scoring', ret_dict

            if '3-pt' in action_str:
                temp = action_str.split(' misses 3-pt ')
                ret_dict['PrimaryPlayer'] = temp.pop(0)
                ret_dict['ActionResult'] = 'miss3'
                ret_dict['ScoreResult'] = 0
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
            #print(temp)
            ret_dict['PrimaryAction'] = 'OffensiveFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'offensive foul', ret_dict

    if 'Shooting foul ' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'ShootingFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'ShootingFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'shooting foul', ret_dict

    if 'Personal foul ' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'PersonalFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'PersonalFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'shooting foul', ret_dict

    if 'Offensive charge foul' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'ChargeFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'ChargeFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'charge foul', ret_dict

    if 'Shooting block foul' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'ShootingBlockingFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'ShootingBlockingFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'blocking foul', ret_dict

    if 'Personal block foul' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'PersonalBlockingFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'PersonalBlockingFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'blocking foul', ret_dict

    if 'Loose ball foul ' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'LooseBallFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'LooseBallFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'loose ball foul', ret_dict

    if 'free throw' in action_str:
        if 'makes' in action_str:
            temp = action_str.split(' makes free throw ')
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'FreeThrow'
            ret_dict['ActionResult'] = 'make1'
            ret_dict['ScoreResult'] = 1
            return 'freethrow', ret_dict

        if 'misses' in action_str:
            temp = action_str.split(' misses free throw ')
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'FreeThrow'
            ret_dict['ActionResult'] = 'make1'
            ret_dict['ScoreResult'] = 0
            return 'freethrow', ret_dict

    if 'timeout' in action_str:
        ret_dict['PrimaryAction'] = 'Timeout'
        return 'timeout', ret_dict

    if ' enters the game for ' in action_str:
        ret_dict['PrimaryAction'] = 'Sub'
        ret_dict['PrimaryPlayer'] = action_str.split(' enters the game for ')[0]
        ret_dict['SecondaryPlayer'] = action_str.split(' enters the game for ')[1]
        return 'sub', ret_dict

    if 'Def 3 sec tech foul by ' in action_str:
        ret_dict['PrimaryAction'] = 'D3SecTech'
        ret_dict['PrimaryPlayer'] = action_str.split('Def 3 sec tech foul by ')[0]
        return 'def3SecTech', ret_dict

    return 'unknown', ret_dict