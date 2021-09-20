from parsita import *
from parsita.util import constant
import json

def formatannotations(annotations):
    return {ant[0]: ant[1] for ant in annotations}

def formatgame(game):
    return {
        'moves': game[0],
        'outcome': game[1]
    }

def formatclocks(clock):
    return {clk[0]: clk[1] for clk in clock}

def formatentry(entry):
    return {'annotations': entry[0], 'game': entry[1]}

def handleoptional(optionalmove):
    if len(optionalmove) > 0:
        return optionalmove[0]
    else:
        return None

# Define Grammar by building up from smallest components

def chessparser(r):

    # tokens
    quote = lit(r'"')
    whitespace = lit(' ') | lit('\n')
    tag = reg(r'[\u0021-\u0021\u0023-\u005A\u005E-\u007E]+')
    string = reg(r'[\u0020-\u0021\u0023-\u005A\u005E-\U0010FFFF]+')

    # Annotations: [Foo "Super Awesome Information"]
    annotation = '[' >> (tag) << ' ' & (quote >> string << quote) << ']'
    annotations = repsep(annotation, '\n') > formatannotations


    #clock = '{' << '[' << '%' >> whitespace >> ('clk' >> whitespace) & (tag << ']') << '}'
    #clocks = repsep(clock, '\n') > formatclocks

    # Moves are more complicated
    regularmove = reg(r'[a-h1-8NBRQKx\+#=]+') # Matches more than just chess moves
    longcastle = reg(r'O-O-O[+#]?') # match first to avoid castle matching spuriously
    castle = reg(r'O-O[+#]?')
    nullmove = lit('--') # Illegal move rarely used in annotations

    move = regularmove | longcastle | castle | nullmove

    # Build up the game
    # movenumber = (reg(r'[0-9]+') << '.' << whitespace) > int # | (reg(r'[0-9]+') << '...' << whitespace) > int #  & (clocks << whitespace)
    movenumber = (reg(r'[0-9]+') << '.' << whitespace) | (reg(r'[0-9]+') << '...' << whitespace) > int
    turn = movenumber & (move << whitespace) & (opt(move << whitespace) > handleoptional)

    draw = lit('1/2-1/2')
    white = lit('1-0')
    black = lit('0-1')
    outcome = draw | white | black

    game = (rep(turn) & outcome) > formatgame

# A PGN entry is annotations and the game
    entry = ((annotations << rep(whitespace)) & (game << rep(whitespace))) > formatentry

# A file is repeated entries
    file = rep(entry)

    #with open(pgn, 'r') as f:
     #   parsedoutput = file.parse(f.read()).or_die()
    parsedoutput = file.parse(r.text)

    return parsedoutput.value
