import requests
from PlayerAnalysis import player_analysis
from ChessParser import chessparser

def urlpull(usrname):

    #url = "https://api.chess.com/pub/player/erik/games"
    #response = urllib.request.urlopen(url)
    #data = json.loads(response.read())

    #chess.com code:
    #url = "https://api.chess.com/pub/player/erik/games"
    #r = requests.get(url)
    # files = r.json()

    # lichess code

    # usrname = 'DDT3000'
    # get evals
    url_lichess_evals = 'https://lichess.org/api/games/user/' + usrname + '?evals=true&clocks=false&perfType=blitz,rapid,classical&analyzed=true&max=350'
    r = requests.get(url_lichess_evals)
    evals_raw = r.text


    # get moves (no evals)
    url_lichess_moves = 'https://lichess.org/api/games/user/' + usrname + '?evals=false&clocks=false&perfType=blitz,rapid,classical&analyzed=true&max=250'
    r_m = requests.get(url_lichess_moves)
    moves_raw = chessparser(r_m)
    player_data = player_analysis(moves_raw, evals_raw)





    # send player data to function to do statistics and return
    # return data to dash app

    return player_data

