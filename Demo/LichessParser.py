import pandas as pd


def lichess_parser(pgn_list):
    # %% extract annotation headers for lichess games (chesscom is parsed through ChesscomParser.py)
    ann_tags = []  # annotation tags
    move_tags = []  # move tags
    # loop through first game and extract annotations
    for entry in pgn_list[0]['annotations']:
        ann_tags.append(entry)

    for i in range(1, 201):
        move_tag = 'Move_ply_' + str(i)
        move_tags.append(move_tag)

    tags = ann_tags + move_tags

    # %% loop through games and create dataframe
    rows = []
    for game in pgn_list:
        annotations = game['annotations']
        moves = game['game']['moves']

        # extract annotations to list
        annlist = []
        for key in annotations.keys():
            annlist.append(annotations[key])

        # extract moves
        movelist = []
        move_tags = []
        for move in moves:
            movelist.append(move[1])

            movelist.append(move[2])

        if not moves:
            continue

        # check if last move is null and remove
        if movelist[len(movelist) - 1] == 'None':
            movelist.pop()
        while len(movelist) < 200:  # add nans
            movelist.append('nan')

        # combine annotations and moves
        row_vals = annlist + movelist

        if not len(row_vals) > 217:
            rows.append(row_vals)

    # create dataframe from matrix
    pdf = pd.DataFrame(rows, columns=tags)
    return pdf

