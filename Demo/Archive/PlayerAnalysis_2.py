from ChessParser import chessparser
# import centipawnloss
# import pgnToFen  # assumes you have pgntofen.py in the same directory, or you know how to handle python modules.
import pandas as pd
import numpy as np
from phase_check_wdrops import phase_check_wdrops

# pgnfile = open('/Users/josephwarner/PycharmProjects/StaffordChess/lichess_DDT3000.pgn')
# pgn = pgnfile.read()

players = []


def player_analysis_2(movelist, pgn_evals):
    tag_labels = ['Event', 'Site', 'Date', 'White', 'Black', 'Result', 'UTCDate', 'UTCTime', 'WhiteElo', 'BlackElo',
                  'WhiteRatingDiff', 'BlackRatingDiff', 'Variant', 'TimeControl', 'Opening', 'ECO', 'Termination']

    eval_headers = []
    mv_headers = []
    # in_row = []
    for n in range(0, 200):
        eval_header = 'Eval_ply_' + str(n + 1)
        mv_header = 'Move_ply_' + str(n + 1)
        eval_headers.append(eval_header)
        mv_headers.append(mv_header)

        # in_row.append('nan')

    Eval_df = pd.DataFrame([], columns=eval_headers)
    Move_df = pd.DataFrame([], columns=mv_headers)
    Tag_df = pd.DataFrame([], columns=tag_labels)

    def evalstring2int(es):  # Turns evalstring into an integer
        digits = ""
        for char in es:
            if char in "1234567890-":
                digits += char
        return (int(digits))

    def getevals(game):
        scores = []
        evalstring = ""
        recording = False
        for char in game:
            if recording:
                if char in "1234567890.-+\n":
                    evalstring += char
                elif char in "]":
                    recording = False
                    scores.append(evalstring2int(evalstring))
                else:
                    # recording = False
                    # scores.append(evalstring2int(evalstring))
                    evalstring = ""
            else:
                if char == "{":
                    recording = True
        return (scores)

    # Now we do the actual math.
    def calcacl(evals):
        whiteloss = []
        blackloss = []
        white = True
        lastscore = 0
        for score in evals:
            if white:
                loss = lastscore - score
                if loss > 0:
                    whiteloss.append(loss)
                else:
                    whiteloss.append(0)
            else:
                loss = (lastscore - score) * -1
                if loss > 0:
                    blackloss.append(loss)
                else:
                    blackloss.append(0)
            white = not white
            lastscore = score

        try:
            avgwl = round(sum(whiteloss) / len(whiteloss))
        except ZeroDivisionError:
            avgwl = 0

        try:
            avgbl = round(sum(blackloss) / len(blackloss))
        except ZeroDivisionError:
            avgbl = 0

        return ((avgwl, avgbl))

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

    def playeracl(player, acl):
        global players
        for entry in players:
            if entry[0] == player:
                entry[1].append(acl)
                return ()
        players.append([player, [acl]])
        return ()

    def processgame(game):
        gametags = parsepgntags(game)
        gameevals = getevals(game)
        gameacl = calcacl(gameevals)
        whiteacl = gameacl[0]
        blackacl = gameacl[1]
        playeracl(gettag(gametags, "White"), whiteacl)
        playeracl(gettag(gametags, "Black"), blackacl)
        return gameevals

    for game in gamespliter(pgn_evals):
        gameevals = processgame(game)
        acls = calcacl(getevals(game))
        whiteacl = acls[0]
        blackacl = acls[1]
        tags = parsepgntags(game)

        # extract evals
        while len(gameevals) < 200:
            gameevals.append('nan')

        Eval_df.loc[len(Eval_df)] = gameevals

        # extract game tags
        tag_list = []
        for tag in tag_labels:
            tag_list.append(gettag(tags, tag))

        Tag_df.loc[len(Tag_df)] = tag_list

    # movelist = chessparser("/Users/josephwarner/PycharmProjects/StaffordChess/lichess_DDT3000_2021-03-23.pgn")
    # movelist = chessparser(pgn)

    for full_game in movelist:
        # gm_moves_w = []
        # gm_moves_b = []
        gm_all_moves = []

        game = full_game['game']
        moves = game['moves']
        for move in moves:
            move_w = move[1]
            move_b = move[2]
            # gm_moves_w.append(move_w)
            # gm_moves_b.append(move_b)
            gm_all_moves.append(move_w)
            gm_all_moves.append(move_b)

        while len(gm_all_moves) < 200:
            gm_all_moves.append('nan')
        while len(gm_all_moves) > 200:
            gm_all_moves.pop()

        Move_df.loc[len(Move_df)] = gm_all_moves

    player_data = pd.concat([Tag_df, Move_df, Eval_df], axis=1)

    def cpl_calc_gm(evals_source):
        whiteloss = []
        blackloss = []
        evals = []
        track_drops = []

        white = True
        lastscore = 0
        for x in evals_source:

            if isinstance(x, str):
                evals.append(x)
            else:
                evals.append(x)

        for score in evals:
            if isinstance(score, str) | isinstance(lastscore, str):
                white = not white
                lastscore = score
                track_drops.append(1)
                continue
            elif white:
                loss = lastscore - score
                if loss > 900:
                    track_drops.append(1)
                    white = not white
                    lastscore = score
                    continue
                elif loss > 0:
                    whiteloss.append(loss)
                    track_drops.append(0)
                else:
                    # whiteloss.append(0)
                    track_drops.append(1)
            else:
                loss = (lastscore - score) * -1
                if loss > 900:
                    track_drops.append(1)
                    white = not white
                    lastscore = score
                    continue
                elif loss > 0:
                    blackloss.append(loss)
                    track_drops.append(0)
                else:
                    # blackloss.append(0)
                    track_drops.append(1)

            white = not white
            lastscore = score

        return whiteloss, blackloss, track_drops

    acpl_w = []
    acpl_b = []
    opening_mcpl_w = []
    opening_mcpl_b = []
    mid_mcpl_w = []
    mid_mcpl_b = []
    end_mcpl_w = []
    end_mcpl_b = []

    for n in range(0, len(Eval_df)):

        evals_cleaned = []

        working_evals = Eval_df.iloc[n, :]
        working_evals_flt = pd.to_numeric(working_evals[:], errors='coerce',
                                          downcast='float')  # convert strings to float
        for chk in range(0, len(working_evals)):
            index_val = working_evals_flt.iloc[chk]
            isnull = pd.isnull(index_val)
            if isnull:
                working_evals_flt.iloc[chk] = working_evals[chk]

        evals_cleaned = []
        for element in working_evals_flt:
            if pd.isna(element):
                continue
            elif isinstance(element, str):  # == 'nan':
                continue
            evals_cleaned.append(element)
        # end for loop

        wloss, bloss, trackdrops = cpl_calc_gm(evals_cleaned)

        working_moves = []
        while n > len(Move_df) - 1:
            n -= 1

        working_moves_in = Move_df.iloc[n, :]
        for move in working_moves_in:
            if pd.isna(move):
                continue
            elif move == 'nan':
                continue
            working_moves.append(move)

        try:
            move_phase = phase_check_wdrops(working_moves, trackdrops)
        except IndexError:
            pass
        # extract white moves (phase)

        index_phase_w = move_phase[::2]

        # extract black moves (phase)
        index_phase_b = []
        for n in range(1, len(move_phase), 2):
            move_phase_i = move_phase[n]
            index_phase_b.append(move_phase_i)
        # end for

        # need to reduce length of phase array in case of mate
        while len(wloss) < len(index_phase_w):
            index_phase_w.pop()
        while len(wloss) > len(index_phase_w):
            wloss.pop()
        while len(bloss) < len(index_phase_b):
            index_phase_b.pop()
        while len(bloss) > len(index_phase_b):
            bloss.pop()

        game_output_w = pd.DataFrame(
            {'wloss': wloss,
             'index_phase_w': index_phase_w
             })
        game_output_b = pd.DataFrame(
            {
                'bloss': bloss,
                'index_phase_b': index_phase_b
            }
        )

        grouped_w = game_output_w.groupby('index_phase_w')
        grouped_b = game_output_b.groupby('index_phase_b')

        try:
            gm_opening_w = grouped_w.get_group('o')
            gm_opening_b = grouped_b.get_group('o')
            gm_opening_cpl_w = gm_opening_w.iloc[:, 0]
            gm_opening_cpl_b = gm_opening_b.iloc[:, 0]
            o_m_w = np.mean(gm_opening_cpl_w)
            o_m_b = np.mean(gm_opening_cpl_b)
            gm_opening_mcpl = (o_m_w + o_m_b) / 2
            opening_mcpl_w.append(o_m_w)
            opening_mcpl_b.append(o_m_b)
        except KeyError:
            opening_mcpl_w.append('nan')
            opening_mcpl_b.append('nan')
        try:
            gm_mid_w = grouped_w.get_group('m')
            gm_mid_b = grouped_b.get_group('m')
            gm_mid_cpl_w = gm_mid_w.iloc[:, 0]
            gm_mid_cpl_b = gm_mid_b.iloc[:, 0]
            m_m_w = np.mean(gm_mid_cpl_w)
            m_m_b = np.mean(gm_mid_cpl_b)
            gm_mid_mcpl = (m_m_w + m_m_b) / 2
            mid_mcpl_w.append(m_m_w)
            mid_mcpl_b.append(m_m_b)
        except KeyError:
            mid_mcpl_w.append('nan')
            mid_mcpl_b.append('nan')
        try:
            gm_end_w = grouped_w.get_group('e')
            gm_end_b = grouped_b.get_group('e')
            gm_end_cpl_w = gm_end_w.iloc[:, 0]
            gm_end_cpl_b = gm_end_b.iloc[:, 0]
            e_m_w = np.mean(gm_end_cpl_w)
            e_m_b = np.mean(gm_end_cpl_b)
            gm_end_mcpl = (e_m_w + e_m_b) / 2
            end_mcpl_w.append(e_m_w)
            end_mcpl_b.append(e_m_b)
        except KeyError:
            end_mcpl_w.append('nan')
            end_mcpl_b.append('nan')

        awcpl = np.mean(wloss)
        abcpl = np.mean(bloss)
        acpl_w.append(awcpl)
        acpl_b.append(abcpl)

    acpl_w = pd.Series(acpl_w)
    acpl_b = pd.Series(acpl_b)
    opening_mcpl_w = pd.Series(opening_mcpl_w)
    opening_mcpl_b = pd.Series(opening_mcpl_b)
    mid_mcpl_w = pd.Series(mid_mcpl_w)
    mid_mcpl_b = pd.Series(mid_mcpl_b)
    end_mcpl_w = pd.Series(end_mcpl_w)
    end_mcpl_b = pd.Series(end_mcpl_b)

    calc_headers = ['acpl_w', 'acpl_b', 'opening_mcpl_w', 'opening_mcpl_b', 'mid_mcpl_w', 'mid_mcpl_b', 'end_mcpl_w',
                    'end_mcpl_b']
    Calc_vals = pd.DataFrame(
        {"acpl_w": acpl_w,
         "acpl_b": acpl_b,
         "opening_mcpl_w": opening_mcpl_w,
         "opening_mcpl_b": opening_mcpl_b,
         "mid_mcpl_w": mid_mcpl_w,
         "mid_mcpl_b": mid_mcpl_b,
         "end_mcpl_w": end_mcpl_w,
         "end_mcpl_b": end_mcpl_b
         })
    player_output = pd.concat([player_data, Calc_vals], axis=1)
    return player_output
# player_output.to_csv(r'/Users/josephwarner/PycharmProjects/StaffordChess/output/player_output.csv')
