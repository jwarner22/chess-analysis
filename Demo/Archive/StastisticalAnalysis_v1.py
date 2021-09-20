
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import mode

def get_rows_indexing(df, col, start, stop):
    min_ind = min(df.index[df[col]==start].tolist() or [0])
    max_ind = max(df.index[df[col]==stop].tolist() or [len(df)])
    return df[min_ind:max_ind+1]

#import meta data
Meta_data = pd.read_csv(r'/Users/josephwarner/PycharmProjects/StaffordChess/output/output.csv', low_memory=False)
df = pd.DataFrame(Meta_data)

#import player data
Player_data = pd.read_csv(r'/Users/josephwarner/PycharmProjects/StaffordChess/output/player_output.csv', low_memory=False)
pdf = pd.DataFrame(Player_data)

#extract elos
w_elo_in = df.loc[:, 'WhiteElo']
b_elo_in = df.loc[:,'BlackElo']

# calculate elo differential and normalize inversely from 0 to 1
eloDiff = abs(w_elo_in-b_elo_in)
eloDiff_invnorm = 1-((eloDiff - np.min(eloDiff))/(np.max(eloDiff)-np.min(eloDiff))) # inverse normalization of elo differential

#intialize lists/arrays
# w_elo = []
# b_elo = []

# remove nan data
# acpl_w_in = df.loc[:, 'acpl_w']
# acpl_w = []
# for index, acpl in enumerate(acpl_w_in):
  #  if pd.isna(acpl):
   #     continue

  #  elif acpl == 0:
  #      continue

  #  else:
   #     w_elo.append(w_elo_in[index])
    #    acpl_w.append(acpl)
     #   b_elo.append(b_elo_in[index])

# split data
player_name = mode(pdf.loc[:,'White']).mode[0] #gets player name
pd_w = pdf[pdf.loc[:,'White'] == player_name]   #extracts player data as white
pd_b = pdf[pdf.loc[:,'Black'] == player_name]   #extracts player data as black

#get player elo
pull_elos = pd_w.loc[:,'WhiteElo'] # gets player elo data
pull_elos = pd.to_numeric(pull_elos,errors='coerce') # converts to int

#calculate player stats
median_elo = np.nanmedian(pull_elos.iloc[0:100])  # gets median elo from last 100 games
median_acpl_w = np.nanmedian(pd_w.loc[:, 'acpl_w']) # median acpl gives centrl tendency (need to sort for player black and white
std_acpl_w = np.nanstd(pd_w.loc[:, 'acpl_w'])  # std assesses consistency of play
median_o_acpl_w = np.nanmedian(pd_w.loc[:, 'opening_mcpl_w']) # median acpl gives centrl tendency (need to sort for player black and white
std_o_acpl_w = np.nanstd(pd_w.loc[:, 'opening_mcpl_w'])
median_m_acpl_w = np.nanmedian(pd_w.loc[:, 'mid_mcpl_w']) # median acpl gives centrl tendency (need to sort for player black and white
std_m_acpl_w = np.nanstd(pd_w.loc[:, 'mid_mcpl_w'])
median_e_acpl_w = np.nanmedian(pd_w.loc[:, 'end_mcpl_w']) # median acpl gives centrl tendency (need to sort for player black and white
std_e_acpl_w = np.nanstd(pd_w.loc[:, 'end_mcpl_w'])

median_acpl_b = np.nanmedian(pd_b.loc[:, 'acpl_b'])
std_acpl_b = np.nanstd(pd_b.loc[:,'acpl_b'])
median_o_acpl_b = np.nanmedian(pd_b.loc[:, 'opening_mcpl_b'])
std_o_acpl_b = np.nanstd(pd_b.loc[:,'opening_mcpl_b'])
median_m_acpl_b = np.nanmedian(pd_b.loc[:, 'mid_mcpl_b'])
std_m_acpl_b = np.nanstd(pd_b.loc[:,'mid_mcpl_w'])
median_e_acpl_b = np.nanmedian(pd_b.loc[:, 'end_mcpl_w'])
std_e_acpl_b = np.nanstd(pd_b.loc[:,'end_mcpl_w'])

# Meta_data = Meta_data.sort_values('WhiteElo')
# pull_meta_elo = Meta_data.loc[:, 'WhiteElo']

# n_range = []
#next_bracket_range = []
#n = 0

#while n < len(pull_meta_elo):
    #elo = pull_meta_elo.iloc[n]
    #if elo > (median_elo - 50) and elo < (median_elo + 50):
     #   n_range.append(n)
    #elif elo > (median_elo +50) and elo < (median_elo + 150):
   #     next_bracket_range.append(n)
  #  n += 1

# get dataframe range
col = 'WhiteElo'
start: {int} = median_elo - 50
stop: {int} = median_elo + 50

# Meta (All)
Meta_range = Meta_data[Meta_data[col] > start]
Meta_range = Meta_range[Meta_range[col] < stop]

# median values (All)
median_elo_meta = np.nanmedian(Meta_range.loc[:, 'WhiteElo'])
median_cpl_w_meta = np.nanmedian(Meta_range.loc[:, 'acpl_w'])

#Meta (White)
median_ocpl_w_meta = np.nanmedian(Meta_range.loc[:, 'opening_mcpl_w'])
median_mcpl_w_meta = np.nanmedian(Meta_range.loc[:, 'mid_mcpl_w'])
median_ecpl_w_meta = np.nanmedian(Meta_range.loc[:, 'end_mcpl_w'])

std_cpl_w_meta = np.nanstd(Meta_range.loc[:, 'acpl_w'])
std_ocpl_w_meta = np.nanstd(Meta_range.loc[:, 'opening_mcpl_w'])
std_mcpl_w_meta = np.nanstd(Meta_range.loc[:, 'mid_mcpl_w'])
std_ecpl_w_meta = np.nanstd(Meta_range.loc[:,'opening_mcpl_w'])

# Meta (Black)
median_cpl_b_meta = np.nanmedian(Meta_range.loc[:,'acpl_b'])
std_cpl_b_meta = np.nanstd(Meta_range.loc[:, 'acpl_b'])

# Meta (Next Elo range)
start = median_elo + 50
stop = median_elo + 150
Meta_range_next = Meta_data[Meta_data[col] > start]
Meta_range_next = Meta_range_next[Meta_range_next[col] < stop]

median_elo_next = np.nanmedian(Meta_range_next.loc[:,'WhiteElo'])
median_cpl_next_w = np.nanmedian(Meta_range_next.loc[:,'acpl_w'])
std_cpl_next_w = np.nanstd(Meta_range_next.loc[:,'acpl_w'])

median_cpl_next_b = np.nanmedian(Meta_range_next.loc[:,'acpl_b'])
std_cpl_next_b = np.nanstd(Meta_range_next.loc[:,'acpl_b'])



print('Elos:')
print(median_elo)
print(median_elo_meta)
print(median_elo_next)
print('CPL White:')
print(median_cpl_w_meta)
print(median_acpl_w)
print(median_cpl_next_w)
print('CPL Black:')
print(median_cpl_b_meta)
print(median_acpl_b)
print(median_cpl_next_b)
print('STD White:')
print(std_acpl_w)
print(std_cpl_w_meta)
print(std_cpl_next_w)
print('STD Black:')
print(std_acpl_b)
print(std_cpl_b_meta)
print(std_cpl_next_b)
print('Opening:')
print(median_o_acpl_w)
print(median_ocpl_w_meta)
print(std_o_acpl_w)
print(std_ocpl_w_meta)
print('Midgame:')
print(median_acpl_w)
print(median_mcpl_w_meta)
print(std_m_acpl_w)
print(std_mcpl_w_meta)
print('Endgame:')
print(median_e_acpl_w)
print(median_ecpl_w_meta)
print(std_e_acpl_w)
print(std_ecpl_w_meta)

plot_data = [median_cpl_w_meta,median_acpl_w,median_cpl_next_w]
plot_data_names = ['Your Elo Range','You','Elo + 100']
x_pos = np.arange(len(plot_data_names))
std_a = [std_cpl_w_meta,std_acpl_w,std_cpl_next_w]
# Build the plot
fig, ax = plt.subplots()
ax.bar(x_pos,plot_data, yerr=std_a, align='center', alpha=0.5, ecolor='black', capsize=10, color=['silver','blue','gold'])
ax.set_ylabel('Avg Centipawn Loss')
ax.set_xticks(x_pos)
ax.set_xticklabels(plot_data_names)
ax.set_title('Avg Centipawn Loss')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
# plt.savefig('bar_plot_with_error_bars.png')
plt.show()

# Elo_range.append(Elo_range_i)


# How to plot data:


# acpl_filtered = list(filter(lambda a: a > 250, acpl_w)) # filter list
# plt.hist(w_elo_filtered,bins=100) # plot histogram of list
# acpl_log = np.log10(acpl_w) # take log of list (necessary for cpl as it is logarithmically distribute)
# w_elo_filtered = list(filter(lambda a: a != 1500, w_elo)) # remove default elo rating for beginners
# mode = mode(w_elo) # find default elo # from scipy.stats import mode
# z_scores = zscore(acpl_w) # calc z scores (can be used to filter outliers) # from scipy.stats import zscore

# Calculate log curve fit:
# w_elo = np.array(w_elo) #transform lists to arrays
# eloDiff = abs(w_elo-b_elo)
# eloDiff_invnorm = 1-((eloDiff - np.min(eloDiff))/(np.max(eloDiff)-np.min(eloDiff))) # inverse normalization of elo differential
# logfit = np.polyfit(w_elo, np.log(acpl_w), 1, w=eloDiff_invnorm) #gets weighted logfit curve
# general curve fit:
# scipy.optimize.curve_fit(lambda t,a,b: a+b*np.log(t),  w_elo, acpl_w) # log returns A,B for acpl_w = A + B*log(w_elo)

# plot hist
# acpl_hist = hist = plt.hist(acpl_w,bins=100,weights=eloDiff_invnorm)


