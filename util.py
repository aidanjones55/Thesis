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
        'dunk': 'DK',
        'tip-in': 'TI'
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
        try:
            ret_dict['PrimaryPlayer'] = temp.pop(0)
        except:
            ret_dict['PrimaryPlayer'] = 'Team'
            ret_dict['PrimaryAction'] = action_str.split('(')[-1][:-1]
            #print(ret_dict)
            return 'turnover', ret_dict



        if '; ' in action_str:
            #print(temp)
            temp = temp[0].split('; ')
            ret_dict['PrimaryAction'] = temp[0]
            ret_dict['SecondaryAction'] = temp[1]
            ret_dict['SecondaryPlayer'] = action_str.split(' by ')[-1][:-1]
            return 'turnover', ret_dict


        if 'out of bounds lost ball' in temp[0]:
            temp = temp[0].split('out of bounds lost ball')
            ret_dict['PrimaryAction'] = 'OutOfBoundsLB'
            return 'turnover', ret_dict

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

        if 'turnover' in temp[0]:
            temp = temp[0].split('turnover')
            ret_dict['PrimaryAction'] = 'Turnover'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'kicked ball' in temp[0]:
            temp = temp[0].split('kicked ball')
            ret_dict['PrimaryAction'] = 'KickedBallTurnover'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'back court' in temp[0]:
            temp = temp[0].split('back court')
            ret_dict['PrimaryAction'] = 'BackCourtTurnover'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'discontinued dribble' in temp[0]:
            temp = temp[0].split('discontinued dribble')
            ret_dict['PrimaryAction'] = 'DiscontinueDribbleTurnover'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'illegal assist' in temp[0]:
            temp = temp[0].split('illegal assist')
            ret_dict['PrimaryAction'] = 'IllegalAssist'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'jump ball violation.' in temp[0]:
            temp = temp[0].split('jump ball violation.')
            ret_dict['PrimaryAction'] = 'JumpBallViolation'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'jump ball' in temp[0]:
            temp = temp[0].split('jump ball')
            ret_dict['PrimaryAction'] = 'JumpBallViolation'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'step out of bounds' in temp[0]:
            temp = temp[0].split('step out of bounds')
            ret_dict['PrimaryAction'] = 'OutOfBounds'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'offensive goaltending' in temp[0]:
            temp = temp[0].split('offensive goaltending')
            ret_dict['PrimaryAction'] = 'OffGoaltending'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'off goaltending' in temp[0]:
            temp = temp[0].split('off goaltending')
            ret_dict['PrimaryAction'] = 'OffGoaltending'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'traveling' in temp[0]:
            temp = temp[0].split('traveling')
            ret_dict['PrimaryAction'] = 'Traveling'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'inbound' in temp[0]:
            temp = temp[0].split('inbound')
            ret_dict['PrimaryAction'] = 'inboundTurnover'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if '3 sec' in temp[0]:
            temp = temp[0].split('3 sec')
            ret_dict['PrimaryAction'] = '3sec'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if '5 sec' in temp[0]:
            temp = temp[0].split('5 sec')
            ret_dict['PrimaryAction'] = '5sec'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'punched ball' in temp[0]:
            temp = temp[0].split('punched ball')
            ret_dict['PrimaryAction'] = 'PunchedBall'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'swinging elbows' in temp[0]:
            temp = temp[0].split('swinging elbows')
            ret_dict['PrimaryAction'] = 'SwingingElbows'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'double personal' in temp[0]:
            temp = temp[0].split('double personal')
            ret_dict['PrimaryAction'] = 'DoublePersonal'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'palming' in temp[0]:
            temp = temp[0].split('palming')
            ret_dict['PrimaryAction'] = 'Palming'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'dbl dribble' in temp[0]:
            temp = temp[0].split('dbl dribble')
            ret_dict['PrimaryAction'] = 'DblDribble'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'lane violation.' in temp[0]:
            temp = temp[0].split('lane violation.')
            ret_dict['PrimaryAction'] = 'LaneViolation'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'lane violation' in temp[0]:
            temp = temp[0].split('lane violation')
            ret_dict['PrimaryAction'] = 'LaneViolation'
            if temp == ['', ')']:
                return 'turnover', ret_dict

        if 'illegal screen' in temp[0]:
            temp = temp[0].split('illegal screen')
            ret_dict['PrimaryAction'] = 'IllegalScreen'
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

                if 'layup ' in temp[0]:
                    temp = temp[0].split('layup ')
                    ret_dict['PrimaryAction'] = primary_action_dict['layup']
                    ret_dict['ActionMetric'] = 0
                    if temp != []:
                        if 'assist' in temp[0]:
                            ret_dict['SecondaryAction'] = 'assist'
                            ret_dict['SecondaryPlayer'] = temp[0].split(' by ')[1][:-1]
                            return 'scoring', ret_dict
                    return 'scoring', ret_dict

                if 'layup' in temp[0]:
                    temp = temp[0].split('layup')
                    ret_dict['PrimaryAction'] = primary_action_dict['layup']
                    ret_dict['ActionMetric'] = 0
                    if temp != []:
                        if 'assist' in temp[0]:
                            ret_dict['SecondaryAction'] = 'assist'
                            ret_dict['SecondaryPlayer'] = temp[0].split(' by ')[1][:-1]
                            return 'scoring', ret_dict
                    return 'scoring', ret_dict

                if 'jump shot' in temp[0]:
                    temp = temp[0].split('jump shot')
                    ret_dict['PrimaryAction'] = primary_action_dict['jump shot']
                    ret_dict['ActionMetric'] = 8
                    if temp != []:
                        if 'assist' in temp[0]:
                            ret_dict['SecondaryAction'] = 'assist'
                            ret_dict['SecondaryPlayer'] = temp[0].split(' by ')[1][:-1]
                            return 'scoring', ret_dict
                    return 'scoring', ret_dict

                if 'dunk' in temp[0]:
                    temp = temp[0].split('dunk')
                    ret_dict['PrimaryAction'] = primary_action_dict['dunk']
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

                if 'jump shot ' in temp[0]:
                    temp = temp[0].split('jump shot ')
                    ret_dict['PrimaryAction'] = primary_action_dict['jump shot']
                    ret_dict['ActionMetric'] = 23
                    if temp != []:
                        if 'assist' in temp[0]:
                            ret_dict['SecondaryAction'] = 'assist'
                            ret_dict['SecondaryPlayer'] = temp[0].split(' by ')[1][:-1]
                            return 'scoring', ret_dict
                    return 'scoring', ret_dict

                if 'jump shot' in temp[0]:
                    temp = temp[0].split('jump shot')
                    ret_dict['PrimaryAction'] = primary_action_dict['jump shot']
                    ret_dict['ActionMetric'] = 23
                    if temp != []:
                        if 'assist' in temp[0]:
                            ret_dict['SecondaryAction'] = 'assist'
                            ret_dict['SecondaryPlayer'] = temp[0].split(' by ')[1][:-1]
                            return 'scoring', ret_dict
                    return 'scoring', ret_dict

        if 'misses' in action_str:
            if '2-pt' in action_str:
                #if 'block' in action_str:
                    #print(f'BLOCK!!!!: {action_str}')
                temp = action_str.split(' misses 2-pt ')
                ret_dict['PrimaryPlayer'] = temp.pop(0)
                ret_dict['ActionResult'] = 'miss2'
                ret_dict['ScoreResult'] = 0
                if ' from ' in temp[0]:
                    temp = temp[0].split(' from ')
                    ret_dict['PrimaryAction'] = primary_action_dict[temp.pop(0)]
                    if ' ft' in temp[0]:
                        temp = temp[0].split(' ft')
                        ret_dict['ActionMetric'] = temp.pop(0)
                        if 'block' in temp[0]:
                            ret_dict['SecondaryPlayer'] = temp[0].split('block by ')[-1][:-1]
                            ret_dict['SecondaryAction'] = 'block'
                            #print(ret_dict)
                            return 'scoring', ret_dict
                        else:
                            return 'scoring', ret_dict

                if ' at rim' in temp[0]:
                    temp = temp[0].split(' at rim')
                    ret_dict['PrimaryAction'] = primary_action_dict[temp.pop(0)]
                    ret_dict['ActionMetric'] = 0
                    if 'block' in temp[0]:
                        ret_dict['SecondaryPlayer'] = temp[0].split('block by ')[-1][:-1]
                        ret_dict['SecondaryAction'] = 'block'
                       #print(ret_dict)
                        return 'scoring', ret_dict
                    else:
                        return 'scoring', ret_dict

                if 'layup' in temp[0]:
                    temp = temp[0].split('layup ')
                    ret_dict['PrimaryAction'] = primary_action_dict['layup']
                    ret_dict['ActionMetric'] = 0
                    if 'block' in temp[0]:
                        ret_dict['SecondaryPlayer'] = temp[0].split('block by ')[-1][:-1]
                        ret_dict['SecondaryAction'] = 'block'
                       #print(ret_dict)
                        return 'scoring', ret_dict
                    else:
                        return 'scoring', ret_dict

                if 'jump shot' in temp[0]:
                    temp = temp[0].split('jump shot')
                    ret_dict['PrimaryAction'] = primary_action_dict['jump shot']
                    ret_dict['ActionMetric'] = 0
                    if 'block' in temp[0]:
                        ret_dict['SecondaryPlayer'] = temp[0].split('block by ')[-1][:-1]
                        ret_dict['SecondaryAction'] = 'block'
                       #print(ret_dict)
                        return 'scoring', ret_dict
                    else:
                        return 'scoring', ret_dict

                if 'dunk' in temp[0]:
                    temp = temp[0].split('dunk')
                    ret_dict['PrimaryAction'] = primary_action_dict['dunk']
                    ret_dict['ActionMetric'] = 0
                    if 'block' in temp[0]:
                        ret_dict['SecondaryPlayer'] = temp[0].split('block by ')[-1][:-1]
                        ret_dict['SecondaryAction'] = 'block'
                       #print(ret_dict)
                        return 'scoring', ret_dict
                    else:
                        return 'scoring', ret_dict

                if 'hook shot' in temp[0]:
                    temp = temp[0].split('hook shot')
                    ret_dict['PrimaryAction'] = primary_action_dict['hook shot']
                    ret_dict['ActionMetric'] = 3
                    if 'block' in temp[0]:
                        ret_dict['SecondaryPlayer'] = temp[0].split('block by ')[-1][:-1]
                        ret_dict['SecondaryAction'] = 'block'
                       #print(ret_dict)
                        return 'scoring', ret_dict
                    else:
                        return 'scoring', ret_dict


            if '3-pt' in action_str:
                #if 'block' in action_str:
                    #print(f'BLOCK!!!!: {action_str}')
                temp = action_str.split(' misses 3-pt ')
                ret_dict['PrimaryPlayer'] = temp.pop(0)
                ret_dict['ActionResult'] = 'miss3'
                ret_dict['ScoreResult'] = 0
                if ' from ' in temp[0]:
                    temp = temp[0].split(' from ')
                    ret_dict['PrimaryAction'] = primary_action_dict[temp.pop(0)]
                    if ' ft' in temp[0]:
                        temp = temp[0].split(' ft')
                        ret_dict['ActionMetric'] = temp.pop(0)
                        if 'block' in temp[0]:
                            ret_dict['SecondaryPlayer'] = temp[0].split('block by ')[-1][:-1]
                            ret_dict['SecondaryAction'] = 'block'
                            #print(ret_dict)
                            return 'scoring', ret_dict
                        else:
                            return 'scoring', ret_dict

                if 'jump shot' in temp[0]:
                    ret_dict['PrimaryAction'] = primary_action_dict['jump shot']
                    ret_dict['ActionMetric'] = '23'
                    temp = temp[0].split('jump shot')
                    if temp == ['', '']:
                        return 'scoring', ret_dict
                    if 'block' in temp[0]:
                        ret_dict['SecondaryPlayer'] = temp[0].split('block by ')[-1][:-1]
                        ret_dict['SecondaryAction'] = 'block'
                        print(ret_dict)
                        return 'scoring', ret_dict
                    else:
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
        else:
            temp = action_str.split(' by ')
            temp.pop(0)
            try:
                ret_dict['PrimaryPlayer'] = temp[0]
                ret_dict['PrimaryAction'] = 'OffensiveFoul'
                return 'offensive foul', ret_dict
            except:
                ret_dict['PrimaryPlayer'] = 'Team'
                ret_dict['PrimaryAction'] = 'OffensiveFoul'
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
        else:
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'ShootingFoul'
            return 'shooting foul', ret_dict

    if 'Flagrant foul type 1 ' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'FlagrantFoul1'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'FlagrantFoul1'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'flagrant1 foul', ret_dict
        else:
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'FlagrantFoul1'
            return 'flagrant1 foul', ret_dict

    if 'Flagrant foul type 2 ' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'FlagrantFoul2'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'FlagrantFoul2'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'flagrant2 foul', ret_dict
        else:
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'FlagrantFoul2'
            return 'flagrant2 foul', ret_dict

    if 'Personal foul ' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'PersonalFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'PersonalFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'personal foul', ret_dict
        else:
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'PersonalFoul'
            return 'personal foul', ret_dict

    if 'Clear path foul ' in action_str:
        ret_dict['ActionResult'] = 'ClearPathFoul'
        temp = action_str.split(' by ')
        temp.pop(0)
        ret_dict['PrimaryPlayer'] = temp[0]
        ret_dict['PrimaryAction'] = 'ClearPathFoul'
        return 'clear path foul', ret_dict

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
        else:
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'ChargeFoul'
            return 'charge foul', ret_dict

    if 'Shooting block foul' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'ShootingBlockingFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'ShootingBlockFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'blocking foul', ret_dict
        else:
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'ShootingBlockFoul'
            return 'blocking foul', ret_dict

    if 'Personal block foul' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'PersonalBlockingFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'PersonalBlockFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'blocking foul', ret_dict
        else:
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'PersonalBlockFoul'
            return 'blocking foul', ret_dict

    if 'Personal take foul' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'PersonalTakeFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'PersonalTakeFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'take foul', ret_dict
        else:
            ret_dict['ActionResult'] = 'PersonalTakeFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'PersonalTakeFoul'
            return 'take foul', ret_dict

    if 'Inbound foul ' in action_str:
        ret_dict['ActionResult'] = 'InboundFoul'
        temp = action_str.split(' by ')
        temp.pop(0)
        ret_dict['PrimaryPlayer'] = temp[0]
        ret_dict['PrimaryAction'] = 'InboundFoul'
        return 'inbound foul', ret_dict

    if 'ejected from game' in action_str:
        ret_dict['ActionResult'] = 'Ejection'
        temp = action_str.split(' ejected from game')
        ret_dict['PrimaryPlayer'] = temp[0]
        ret_dict['PrimaryAction'] = 'Ejection'
        return 'ejection', ret_dict

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
        else:
            ret_dict['ActionResult'] = 'LooseBallFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'LooseBallFoul'
            return 'loose ball foul', ret_dict

    if 'Technical foul by ' in action_str:
        ret_dict['ActionResult'] = 'TechnicalFoul'
        temp = action_str.split(' by ')
        temp.pop(0)
        if len(temp[0].split(' ')[0]) == 2:
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'TechnicalFoul'
            return 'technical foul', ret_dict
        if temp[0] == 'Team':
            ret_dict['PrimaryPlayer'] = 'Team'
            ret_dict['PrimaryAction'] = 'TechnicalFoul'
            return 'technical foul', ret_dict

    if 'Away from play foul' in action_str:
        if 'drawn by' in action_str:
            ret_dict['ActionResult'] = 'AFPFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (drawn')[0]
            ret_dict['PrimaryAction'] = 'AFPFoul'
            ret_dict['SecondaryAction'] = 'DrawnBy'
            ret_dict['SecondaryPlayer'] = temp[1][:-1]
            return 'AFPFoul', ret_dict
        else:
            ret_dict['ActionResult'] = 'AFPFoul'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0]
            ret_dict['PrimaryAction'] = 'AFPFoul'
            return 'AFPFoul', ret_dict


    if 'Violation ' in action_str:
        if 'kicked ball' in action_str:
            ret_dict['ActionResult'] = 'KickBallViolation'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (kicked')[0]
            ret_dict['PrimaryAction'] = 'KickBallViolation'
            return 'KickBallViolation', ret_dict

        if 'def goaltending' in action_str:
            ret_dict['ActionResult'] = 'DefGoaltending'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (def goaltending')[0]
            ret_dict['PrimaryAction'] = 'DefGoaltending'
            return 'DefGoaltending', ret_dict

        if 'delay of game' in action_str:
            ret_dict['ActionResult'] = 'DelayOfGame'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (delay of game')[0]
            ret_dict['PrimaryAction'] = 'DelayOfGame'
            return 'DelayOfGame', ret_dict

        if 'lane' in action_str:
            ret_dict['ActionResult'] = 'LaneViolation'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (lane')[0]
            ret_dict['PrimaryAction'] = 'LaneViolation'
            return 'LaneViolation', ret_dict

        if 'jump ball' in action_str:
            ret_dict['ActionResult'] = 'JumpBallViolation'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (jump')[0]
            ret_dict['PrimaryAction'] = 'JumpBallViolation'
            return 'JumpBallViolation', ret_dict

        if 'violation' in action_str:
            ret_dict['ActionResult'] = 'Violation'
            temp = action_str.split(' by ')
            temp.pop(0)
            ret_dict['PrimaryPlayer'] = temp[0].split(' (violation')[0]
            ret_dict['PrimaryAction'] = 'Violation'
            return 'Violation', ret_dict


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

    if ' enters the game for' in action_str:
        ret_dict['PrimaryAction'] = 'Sub'
        ret_dict['PrimaryPlayer'] = action_str.split(' enters the game for')[0]
        return 'sub', ret_dict

    if 'Def 3 sec tech foul by ' in action_str:
        ret_dict['PrimaryAction'] = 'D3SecTech'
        ret_dict['PrimaryPlayer'] = action_str.split('Def 3 sec tech foul by ')[0]
        return 'def3SecTech', ret_dict

    if 'Instant Replay' in action_str:
        ret_dict['PrimaryAction'] = 'InstantReplay'
        ret_dict['PrimaryPlayer'] = 'Team'
        if 'Ruling Stands' in action_str:
            ret_dict['ActionResult'] = 'RulingStands'
            return 'replay', ret_dict
        if 'Challenge: Stands' in action_str:
            ret_dict['ActionResult'] = 'RulingStands'
            return 'replay', ret_dict
        if 'Request: Stands' in action_str:
            ret_dict['ActionResult'] = 'RulingStands'
            return 'replay', ret_dict
        else:
            ret_dict['ActionResult'] = 'Unknown'
            return 'replay', ret_dict

    if 'Turnover by Team (5 sec inbounds)' in action_str:
        ret_dict['PrimaryAction'] = 'Turnover5Second'
        ret_dict['PrimaryPlayer'] = 'Team'
        return 'Turnover5Second', ret_dict

    if 'Technical foul by' == action_str:
        ret_dict['PrimaryPlayer'] = 'Team'
        ret_dict['PrimaryAction'] = 'TechnicalFoul'
        return 'Turnover5Second', ret_dict

    return 'unknown', ret_dict