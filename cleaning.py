# -*- coding: utf-8 -*-

import pandas as pd
import pickle
import re
#%%
#Future dataframe columns name list
columns=['White_Elo','Black_Elo','Result', 'Opening','Variation',
         'Time_Control','Increment','Evaluation','Players_Clock','Termination',
         'Moves']
#dictionary to store the data
data={c:[] for c in columns}
#Time to revome data of interest in the dataframe
games = pickle.load(open('games.pickle','rb'))
for game in games:
    #Player's Elo
    data['White_Elo'].append(re.search(r'WhiteElo\s"(\d+)',game).group(1))
    data['Black_Elo'].append(re.search(r'BlackElo\s"(\d+)',game).group(1))
    #Match Result(draw, win)
    data['Result'].append(re.search(r'\d-\d', game).group(0))
    #Opening and variation
    opn_m = re.search(r'(Opening\s")(.+")',game).group(2)[:-1].split(':')
    data['Opening'].append(opn_m[0])
    data['Variation'].append(opn_m[1] if len(opn_m)>1 else None)
    
    #Time control and increment
    time_m = re.search(r'(TimeControl\s")(\d+\+)(\d+")',game)
    data['Time_Control'].append(time_m.group(2)[:-1] if time_m is not None 
                                else None)
    data['Increment'].append(time_m.group(3)[:-1] if time_m is not None 
                             else None)
    #Engine evaluation
    data['Evaluation'].append(re.findall(
        r'%eval\s(#-?\d{1,2}|-?\d{1,2}\.?\d{1,2})', game))
    #Player clock
    data['Players_Clock'].append(re.findall(r'%clk\s(\d:\d\d:\d\d)', game))
    #Type of termination (Resign, mate or timeout)
    data['Termination'].append(
        re.search(r'(Termination\s")(.+")',game).group(2)[:-1])
    #moves played
    moves = [x+y for x, y in re.findall(r'(\d{1,2}\.{1,3}\s.{1,6})(\d|#|\+|\w)'
                                        ,game)]
    sep=' '
    moves = sep.join(moves)
    moves= re.sub(r'(\n|\d{1,3}\.{3}\s?|\$\d\s)','',moves)
    moves=re.sub(r'\s\$\d','',moves) #Read comment bellow
    data['Moves'].append(re.sub(r'(\d\.)(\s)(\w)',r'\1\3',moves))

games_df=pd.DataFrame(data=data, columns=columns)

# =============================================================================
# During the EDA I noticed that the resub hat not removed the "$\d" in end of
# the game. When I noticed this I've had soem problems in my computer and lost 
# the games.pickle, so I'm adding this here as not that I've loaded the csv file
# and rerunning, removed "$/d" at the end and ran the GetTermination function.
# I also adde the re.sub above as if I had ran it at first.
# 
# =============================================================================

def GetTermination(df):
#Function to diferentiate win by checkmate and resignation
    games = df['Moves'].to_numpy()
    termination = df['Termination'].to_numpy()
    for i, game in enumerate(games):
        last_move = re.search(r'(\d{1,2}\.| ).{1,7}$',game).group(0)
        if last_move.endswith('#'):
            termination[i]='Checkmate'
        else:
            if termination[i] == 'Normal':
                termination[i]='Resignation'
    return termination
                
games_df['Termination'] =GetTermination(games_df)
 
games_df.to_csv('games.zip',sep =';',compression='zip')   

