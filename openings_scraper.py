# -*- coding: utf-8 -*-

import requests
import pandas as pd
#Request paramaters for the post request
payload={'startIndex':'0','results':'2963','sort':'name','dir':'asc','pieceColour':'either',
         'numGames':'100'}
r=requests.post('https://old.chesstempo.com/requests/openingslist.php',data=payload)
openings = r.json()
#Converting the json from the response to a pandas Dataframe
df =pd.DataFrame(data = openings['result']['openings'])
#I'm onyly interested in the opening names and the moves
opening_df=df.loc[:,['name','moves_san']]
#Function to format the notation to standard pgn notation
def cleanMoves(df):
    new_moves=[]
    games = df.to_numpy()
    for game in games:
        if len(game)%2!=0:
            game.append('')
        n_moves = list(range(int(len(game)/2)))
        moves = [str(n+1)+'.'+i+' '+j for n,i,j in zip(n_moves,game[0::2],game[1::2])]
        sep=' '
        moves=sep.join(moves)
        new_moves.append(moves)
    return new_moves

opening_df.loc[:,'moves_san'] = cleanMoves(opening_df.loc[:,'moves_san'])
opening_df.to_csv('openings.csv')

          
          
        