from statistics import mode

import dash
# import plotly.express as px
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from url_pull import urlpull
from scipy.stats import mode
# import weightedstats as ws

colors = {
    'background': '#add8e6',
    'text': '#00008b',
    'muted text': '#808080'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


# df_analysis = pd.DataFrame({
# 'CPL': [100,50,35,75,200,50,55,70,65,104,33,20,98,45,50,60,105,35,85,125,150,40,10,200],
#  'CPL Comparison': ['CPL','CPL','CPL','CPL','CPL','CPL','CPL','CPL','CPL','CPL','CPL','CPL', 'Elo Bracket CPL', 'Elo Bracket CPL', 'Elo Bracket CPL', 'Elo Bracket CPL', 'Elo Bracket CPL', 'Elo Bracket CPL', 'Elo Bracket CPL', 'Elo Bracket CPL', 'Elo Bracket CPL','Elo Bracket CPL','Elo Bracket CPL','Elo Bracket CPL'],
#   'color': ['blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','green','green','green','green','green','green','green','green','green','green','green','green']
# })


# fig_analysis = px.box(df_analysis, x='CPL Comparison', y="CPL", notched=True, color='color')
# fig_analysis.update_traces(orientation='h') # horizontal box plots


# Plot Resulting Graph
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='ELO ELEVATION',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='ELO ELEVATION: Get more from your game.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Label('Enter Lichess Username:', style={
        'margin-left': 80,
        'color': colors['text']
    }),
    dcc.Input(value='', id='input-box', type='text', style={
        'margin-left': 80,
        'background': 'gray',
        'color': '#d3d3d3'
    }),

    html.Button('Analyze', id='btn-nclicks-1', n_clicks=0, style={
        'margin-left': 40,
    }),

    dcc.Graph(id='indicator-graphic-1')
])


@app.callback(
    dash.dependencies.Output('indicator-graphic-1', 'figure'),
    [dash.dependencies.Input('btn-nclicks-1', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_graph(n_clicks, value):

    # import meta data
    Meta_data = pd.read_csv(r'/Users/josephwarner/PycharmProjects/StaffordChess/output/output.csv', low_memory=False)
    # df = pd.DataFrame(Meta_data)
    # df = df[df['TimeControl'].map() != 'Rated Bullet Game']
    # df = df.drop(df[df.TimeControl == 'Rated Bullet Game'].index)
    # df = df[df["TimeControl"] != 'Rated Bullet Game']
    # Enter code to initialize analysis here
    username = value
    pdf = urlpull(username)

    # split data
    player_name = mode(pdf.loc[:, 'White'])  # gets player name
    pd_w = pdf[pdf.loc[:, 'White'] == player_name]  # extracts player data as white
    pd_b = pdf[pdf.loc[:, 'Black'] == player_name]  # extracts player data as black

    # get player elo
    pull_elos = pd_w.loc[:, 'WhiteElo']  # gets player elo data
    pull_elos = pd.to_numeric(pull_elos, errors='coerce')  # converts to int

    median_elo = np.nanmedian(pull_elos.iloc[0:100])  # gets median elo from last 100 games

    acpl_w = pd_w.loc[:, 'acpl_w']
    opening_mcpl_w = pd_w.loc[:, 'opening_mcpl_w']
    mid_mcpl_w = pd_w.loc[:, 'mid_mcpl_w']
    end_mcpl_w = pd_w.loc[:, 'end_mcpl_w']

    acpl_w = [acpl for acpl in acpl_w if acpl != 'nan']
    opening_mcpl_w = [acpl_o for acpl_o in opening_mcpl_w if acpl_o != 'nan']
    mid_mcpl_w = [acpl_m for acpl_m in mid_mcpl_w if acpl_m != 'nan']
    end_mcpl_w = [acpl_e for acpl_e in end_mcpl_w if acpl_e != 'nan']

    # get dataframe range
    col = 'WhiteElo'
    start: {int} = median_elo - 50
    stop: {int} = median_elo + 50

    # Meta (All)
    Meta_range = Meta_data[Meta_data[col] > start]
    Meta_range = Meta_range[Meta_range[col] < stop]

    acpl_w_m = Meta_range.loc[:, 'acpl_w']
    opening_mcpl_w_m = Meta_range.loc[:, 'opening_mcpl_w']
    mid_mcpl_w_m = Meta_range.loc[:, 'mid_mcpl_w']
    end_mcpl_w_m = Meta_range.loc[:, 'end_mcpl_w']

    acpl_w_m = [acpl for acpl in acpl_w_m if np.isnan(acpl) == False]
    opening_mcpl_w_m = [acpl for acpl in opening_mcpl_w_m if np.isnan(acpl) == False]
    mid_mcpl_w_m = [acpl for acpl in mid_mcpl_w_m if np.isnan(acpl) == False]
    end_mcpl_w_m = [acpl for acpl in end_mcpl_w_m if np.isnan(acpl) == False]

    # Meta (Next Elo range)
    start = median_elo + 150
    stop = median_elo + 250

    Meta_range_next = Meta_data[Meta_data[col] > start]
    Meta_range_next = Meta_range_next[Meta_range_next[col] < stop]

    acpl_w_n = Meta_range_next.loc[:, 'acpl_w']
    opening_mcpl_w_n = Meta_range_next.loc[:, 'opening_mcpl_w']
    mid_mcpl_w_n = Meta_range_next.loc[:, 'mid_mcpl_w']
    end_mcpl_w_n = Meta_range_next.loc[:, 'end_mcpl_w']

    acpl_w_n = [acpl for acpl in acpl_w_n if np.isnan(acpl) == False]
    opening_mcpl_w_n = [acpl for acpl in opening_mcpl_w_n if np.isnan(acpl) == False]
    mid_mcpl_w_n = [acpl for acpl in mid_mcpl_w_n if np.isnan(acpl) == False]
    end_mcpl_w_n = [acpl for acpl in end_mcpl_w_n if np.isnan(acpl) == False]


    # Player As Black:

    acpl_b = pd_b.loc[:, 'acpl_b']
    opening_mcpl_b = pd_b.loc[:, 'opening_mcpl_b']
    mid_mcpl_b = pd_b.loc[:, 'mid_mcpl_b']
    end_mcpl_b = pd_b.loc[:, 'end_mcpl_b']

    acpl_b = [acpl for acpl in acpl_b if acpl != 'nan']
    opening_mcpl_b = [acpl_o for acpl_o in opening_mcpl_b if acpl_o != 'nan']
    mid_mcpl_b = [acpl_m for acpl_m in mid_mcpl_b if acpl_m != 'nan']
    end_mcpl_b = [acpl_e for acpl_e in end_mcpl_b if acpl_e != 'nan']

    # Meta (All) As Black

    acpl_b_m = Meta_range.loc[:, 'acpl_b']
    opening_mcpl_b_m = Meta_range.loc[:, 'opening_mcpl_b']
    mid_mcpl_b_m = Meta_range.loc[:, 'mid_mcpl_b']
    end_mcpl_b_m = Meta_range.loc[:, 'end_mcpl_b']

    acpl_b_m = [acpl for acpl in acpl_b_m if np.isnan(acpl) == False]
    opening_mcpl_b_m = [acpl for acpl in opening_mcpl_b_m if np.isnan(acpl) == False]
    mid_mcpl_b_m = [acpl for acpl in mid_mcpl_b_m if np.isnan(acpl) == False]
    end_mcpl_b_m = [acpl for acpl in end_mcpl_b_m if np.isnan(acpl) == False]

    # Next Elo Range As Black

    acpl_b_n = Meta_range_next.loc[:, 'acpl_b']
    opening_mcpl_b_n = Meta_range_next.loc[:, 'opening_mcpl_b']
    mid_mcpl_b_n = Meta_range_next.loc[:, 'mid_mcpl_b']
    end_mcpl_b_n = Meta_range_next.loc[:, 'end_mcpl_b']

    acpl_b_n = [acpl for acpl in acpl_b_n if np.isnan(acpl) == False]
    opening_mcpl_b_n = [acpl for acpl in opening_mcpl_b_n if np.isnan(acpl) == False]
    mid_mcpl_b_n = [acpl for acpl in mid_mcpl_b_n if np.isnan(acpl) == False]
    end_mcpl_b_n = [acpl for acpl in end_mcpl_b_n if np.isnan(acpl) == False]


   # player_a = [end_mcpl_w, mid_mcpl_w, opening_mcpl_w, acpl_w]
   # meta_a = [end_mcpl_w_m, mid_mcpl_w_m, opening_mcpl_w_m, acpl_w_m]
   # next_a = [end_mcpl_w_n, mid_mcpl_w_n, opening_mcpl_w_n, acpl_w_n]

    # meta_tags_w = []
    # for i in acpl_w_m:
    #   meta_tags_w.append("ACPL")

   # player_tags = []
  #  meta_tags = []
  #  next_tags = []
  #  phases = ["Endgame", "Midgame", "Endgame", "ACPL"]
  #  for index, phase in enumerate(player_a):
      #  phase_tag = phases[index]
       # for n in range(0, len(phase) - 1):
         #   player_tags.append(phase_tag)

   # for index, phase in enumerate(meta_a):
       # phase_tag = phases[index]
      #  for n in range(0, len(phase) - 1):
     #       meta_tags.append(phase_tag)

    #for index, phase in enumerate(next_a):
        #phase_tag = phases[index]
        #for n in range(0, len(phase) - 1):
        #    next_tags.append(phase_tag)

    # player_a = np.array(player_a)
    # player_a = np.ndarray.flatten(player_a)
    # meta_a = np.array(player_a)
    # meta_a = np.ndarray.flatten(meta_a)

    # Player Elo stats:
    w_elo_in = pd_w.loc[:,'WhiteElo']
    w_elo_n = pd.to_numeric(w_elo_in, errors='coerce')
    w_elo = np.array(w_elo_n)  # transform lists to arrays

    b_elo_in = pd_w.loc[:, 'BlackElo']
    b_elo_n = pd.to_numeric(b_elo_in, errors='coerce')
    b_elo = np.array(b_elo_n)

    eloDiff = abs(w_elo-b_elo)
    # eloDiff_invnorm = 1-((eloDiff - np.min(eloDiff))/(np.max(eloDiff)-np.min(eloDiff)))  # inverse normalization of elo differential

    # As White
    # Player as White
    # acpl_w = acpl_w[~np.isnan(acpl_w)] removes nan
    median_acpl_w = np.median(acpl_w) # .weighted_median(acpl_w) # , weights=eloDiff_invnorm)
    median_opening_mcpl_w = np.median(opening_mcpl_w) # .weighted_median(opening_mcpl_w) #, weights=eloDiff_invnorm)
    median_mid_mcpl_w = np.median(mid_mcpl_w) # .weighted_median(mid_mcpl_w) #, weights=eloDiff_invnorm)
    median_end_mcpl_w = np.median(end_mcpl_w) # .weighted_median(end_mcpl_w) #, weights=eloDiff_invnorm)


    # Meta  Elo stats
    w_elo_in = Meta_range.loc[:,'WhiteElo']
    w_elo_n = pd.to_numeric(w_elo_in,errors='coerce')
    w_elo = np.array(w_elo_n) #transform lists to arrays

    b_elo_in = Meta_range.loc[:,'BlackElo']
    b_elo_n = pd.to_numeric(b_elo_in,errors='coerce')
    b_elo = np.array(b_elo_n)

    eloDiff = abs(w_elo-b_elo)
    # eloDiff_invnorm = 1-((eloDiff - np.min(eloDiff))/(np.max(eloDiff)-np.min(eloDiff))) # inverse normalization of elo differential

    # Meta Elo Bracket
    median_acpl_w_m = np.median(acpl_w_m) # .weighted_median(acpl_w_m) #, weights=eloDiff_invnorm)
    median_opening_mcpl_w_m = np.median(opening_mcpl_w_m) # .weighted_median(opening_mcpl_w_m) #, weights=eloDiff_invnorm)
    median_mid_mcpl_w_m = np.median(mid_mcpl_w_m) # ws.weighted_median(mid_mcpl_w_m) #, weights=eloDiff_invnorm)
    median_end_mcpl_w_m = np. median(end_mcpl_w_m) # .weighted_median(end_mcpl_w_m) #, weights=eloDiff_invnorm)


    # Next Elo stats
    w_elo_in = Meta_range_next.loc[:,'WhiteElo']
    w_elo_n = pd.to_numeric(w_elo_in,errors='coerce')
    #for index, elo_val in enumerate(w_elo):
     #   if isinstance(elo_val,str):
      #      w_elo.iloc[index] = 0
    w_elo = np.array(w_elo_n) #transform lists to arrays
    b_elo_in = Meta_range_next.loc[:,'BlackElo']
    b_elo_n = pd.to_numeric(b_elo_in,errors='coerce')
   # for index, elo_val in enumerate(b_elo):
    #    if isinstance(elo_val, str):
     #       b_elo.iloc[index] = 0
    b_elo = np.array(b_elo_n)

    eloDiff = abs(w_elo-b_elo)
    # eloDiff_invnorm = 1-((eloDiff - np.min(eloDiff))/(np.max(eloDiff)-np.min(eloDiff))) # inverse normalization of elo differential

    # Meta Next Elo Bracket
    median_acpl_w_n = np.median(acpl_w_n) # .weighted_median(acpl_w_n) #, weights=eloDiff_invnorm)
    median_opening_mcpl_w_n = np.median(opening_mcpl_w_n) # ws.weighted_median(opening_mcpl_w_n) #, weights=eloDiff_invnorm)
    median_mid_mcpl_w_n = np.median(mid_mcpl_w_n) # .weighted_median(mid_mcpl_w_n) #, weights=eloDiff_invnorm)
    median_end_mcpl_w_n = np.median(end_mcpl_w_n) # .weighted_median(end_mcpl_w_n) #, weights=eloDiff_invnorm)

    groups = ['You', 'Your Elo', 'Elevated Elo']
    acpl_all_w = [median_acpl_w, median_acpl_w_m, median_acpl_w_n]
    opening_all_w = [median_opening_mcpl_w, median_opening_mcpl_w_m, median_opening_mcpl_w_n]
    mid_all_w = [median_mid_mcpl_w, median_mid_mcpl_w_m, median_mid_mcpl_w_n]
    end_all_w = [median_end_mcpl_w, median_end_mcpl_w_m, median_end_mcpl_w_n]

    fig = go.Figure(data=[
        go.Bar(name='ACPL', x = groups, y = acpl_all_w),
        go.Bar(name='Opening', x = groups, y = opening_all_w),
        go.Bar(name='Midgame', x = groups, y = mid_all_w),
        go.Bar(name='Endgame', x = groups,y = end_all_w)
    ])

    fig.update_layout(barmode='group')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
