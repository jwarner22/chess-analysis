import pandas as pd
import numpy as np

pgnfile = open('/Python Scripts/Other/ChessDemo/ChessCom_calebgibson21_202103.pgn')
pgn = pgnfile.read()


def parsemoves(game):
    gamemoves = []
    beginmoves = '1. '
    move_end = '{'
    move_start = '}'
    point = 0
    moves_started = False
    nextmove = False

    while point < len(game):
        if game[point:point + len(beginmoves)] == beginmoves:
            if not moves_started:
                last_end = point-2
            #startingpoint = point
            #initialmove = game[point+len(beginmoves)+1:point+len(beginmoves)+2]
            #gamemoves.append(initialmove)
            wmove = True
            moves_started = True
        if moves_started:
            if not wmove:
                if game[point] == move_start:
                    last_end = point
                    wmove = True
                    nextmove = True
                    continue
                if game[point] == move_end:
                    last_move = game[last_end+7:point-1]
                    gamemoves.append(last_move)
            if wmove:
                if game[point] == move_start and nextmove == False:
                    last_end = point
                    wmove = False
                if game[point] == move_end:
                    last_move = game[last_end+5:point-1]
                    gamemoves.append(last_move)
                    last_end = point
                    if nextmove == True:
                        nextmove = False

        point += 1

    return gamemoves


def gamespliter(pgndata):
    startingpoints = []
    point = 0
    beginstr = '[Event "'
    while point < len(pgndata):
        if pgndata[point:point + len(beginstr)] == beginstr:
            startingpoints.append(point)
        point += 1
    if len(startingpoints) == 1:
        return ([pgndata])
    else:
        games = []
        counter = 0
        while counter < len(startingpoints) - 1:
            games.append(pgndata[startingpoints[counter]:startingpoints[counter + 1]])
            counter += 1
        games.append(pgndata[startingpoints[-1]:])
        return (games)

def parsepgntags(game):
    rawtags = []
    rawtag = ""
    intag = False
    for char in game:
        if intag:
            if char == ']':
                rawtags.append(rawtag)
                rawtag = ""
                intag = False
            else:
                rawtag += char
        else:
            if char == '[':
                intag = True

    tags = []
    for entry in rawtags:
        stage = 0
        tag = ""
        data = ""
        for char in entry:
            if stage == 0:
                if char != " ":
                    tag += char
                else:
                    stage += 1
            elif stage == 1:
                if char == '"':
                    stage += 1
            elif stage == 2:
                if char != '"':
                    data += char
                else:
                    tags.append((tag, data))

    return (tags)

def gettag(taglist, tag):
    for entry in taglist:
        if entry[0] == tag:
            return (entry[1])
    return ("Tag not found")


def processgame(game):
    gametags = parsepgntags(game)
    gamemoves = parsemoves(game)
    return gametags, gamemoves


def chesscom_parser(pgn):
    global index
    gamerows = []
    for game in gamespliter(pgn):
        tags_raw, moves = processgame(game)

        # xtract tag data (remove headers)
        tags = []
        for index, tag in enumerate(tags_raw):
            tags.append(tag[1])

        # remove excess moves (max 100)
        while len(moves) > 200:
            moves.pop()
        while len(moves) < 200:
            moves.append('nan')
        game_row = tags + moves
        if len(tags) == 21:
            gamerows.append(game_row)
    chesscomanno = ['Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result', 'CurrentPosition', 'Timezone', 'ECO',
                    'ECOurl', 'UTCdate', 'UTCTime', 'WhiteElo', 'BlackElo', 'TimeControl', 'Termination', 'StartTime',
                    'EndDate', 'EndTime', 'Link']
    chesscommoves = []
    for i in range(1, 201):
        move_tag = 'Move_ply_' + str(i)
        chesscommoves.append(move_tag)
    chesscomtags = chesscomanno + chesscommoves
    pdf = pd.DataFrame(gamerows, columns=chesscomtags)

    return pdf


parsed_pgn = chesscom_parser(pgn)