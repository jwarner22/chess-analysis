
# from stockfish import Stockfish
import pgnToFen  # assumes you have pgntofen.py in the same directory, or you know how to handle python modules.
import numpy as np
import pandas as pd

# stockfish = Stockfish('/Users/josephwarner/PycharmProjects/StaffordChess/stockfish') # , parameters={"Threads": 2, "Minimum Thinking Time": 1, "Use NNUE": 'true', "EvalFile": '/Users/josephwarner/PycharmProjects/StaffordChess/13/nn-c157e0a5755b.nnue'})



# FUNCTIONS
def  phase_check_wdrops(movelist_source ,track_drops):

    pieces_index = ['p', 'n', 'b', 'r', 'q', 'P', 'N', 'B', 'R', 'Q']
    midgameLimit = 15258
    endgameLimit = 3915
    piece_val_o = [124, 781, 825, 1276, 2538]  # PNBRQ opening and mid

    phase_array = []
    movelist_phase = []
    for element in movelist_source:  # removes nan values
        if pd.isna(element):
            continue
        movelist_phase.append(element)
    # end for loop

    # movelist_source = ["e4","c5","c3","d5","exd5","Qxd5","d4", "Nc6","Nf3","Bg4","Be2","cxd4","cxd4","e6","Nc3","Bb4","O-O","Qa5","a3","Bxc3","bxc3","Nf6","Rb1","O-O","Rb5","Qc7","h3","Bf5","Nh4","Bg6","Nxg6","hxg6","Bf3","a6","Rc5","Nd7","Rg5","Ne7","Qb3","Rab8"] # , "g3 Rbc8 22.Qxb7 Qxb7 23.Bxb7 Rxc3 24.Bd2 Rxa3 25.Bb4 Rb3 26.Bxe7
    # movelist = []

    pgnConverter = pgnToFen.PgnToFen()
    pgnConverter.clearAllFens()
    pgnConverter.resetBoard()
    PGNMoves = movelist_phase
    fen = pgnConverter.pgnToFen(PGNMoves)
    #fen = pgnConverter.getFullFen()
    fens_all = fen.fens  # getAllFens()



    for index, fen_i in enumerate(fens_all):
        # stockfish.set_fen_position(fen)
        # bv = stockfish.get_board_visual()

        # get material count

        material = []
        element = ''
        c = 0
        for letter in fen_i:
            if letter != ' ':
                c += 1
            else:
                break
        splitat = c
        fen_split = fen_i[:splitat]

        for piece in pieces_index:

            piece_i = fen_split.count(piece)
            material.append(piece_i)

                    # need to count each element before space in fen to speed up phse check by bypassing stockfish
                    # piece_i = fen.count(piece)
                    # material.append(piece_i)

        # piece_val_e = [206, 854, 915, 1380, 2682]  # PNBRQ endgame

        # i = 0
        # material_value_a = []
        material_w = material[:5]
        material_b = material[5:]
        piece_val_w = np.multiply(material_w, piece_val_o)
        piece_val_b = np.multiply(material_b, piece_val_o)
        # piece_val_w = np.dot(material_w, piece_val_o)
        # piece_val_b = np.dot(material_b, piece_val_o)
        material_value: {int} = sum(piece_val_w) + sum(piece_val_b)

        # for materials in material:
          #  piece_val_t = materials * piece_val_o[i]
           # material_value_a.append(piece_val_t)
           # i = i + 1
           # if i > 4:
                # i = 0

        # material_value = np.sum(material_value_a)
        # material_value = int(np.rint(material_value))
        min_mat = min(material_value, midgameLimit)
        mat = max(endgameLimit, min_mat)
        chk_phase = (mat - endgameLimit) / (midgameLimit - endgameLimit)

        if chk_phase == 0:
            phase = "e"
        elif chk_phase < 1:
            phase = "m"
        else:
            phase = "o"

        try:
            if track_drops[index] == 0:
                phase_array.append(phase)
        except IndexError:
            continue

    return phase_array
