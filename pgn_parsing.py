# -*- coding: utf-8 -*-

import chess.pgn
import pickle
import regex as re

all_games = []
match=re.compile('Rated.+') #criteria for selecting rated games only
#visitor to pass each game to string format
exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True) 
with open('lichess_db_standard_rated_2020-02.pgn') as games:
    while True:
        game = chess.pgn.read_game(games)
        if game is None:
            break
        event=game.headers['Event']        
        #exporting the game to string
        exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
        game = game.accept(exporter)
        #I only wanted rated games and games that have engine evaluation
        if bool(re.match(match,event)) and re.search('\[%eval',game):
            all_games.append(game)
        exporter = None #resetting exporter, otherwise it will accumulate games

file = all_games
pickle.dump(all_games,open('games.pickle','wb'))

# =============================================================================
# At the end I made a mistake, because I didn't set an ammount of colected games
# to stop the loop, I opened after the script ran for some time, so it's not as 
# reproducible if someone was to use my code to trey and obtain the same result.
# =============================================================================
