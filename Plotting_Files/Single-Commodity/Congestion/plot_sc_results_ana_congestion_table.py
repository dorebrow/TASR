# File: plot_sc_results_ana_congestion_alt.py
# Purpose: Plots single-commodity average total travel time (congestion) and standard deviations 
# for the Anaheim network under low, medium, and high demand levels. Includes horizontal
# bar chart and vertical table.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'


ana_low = {
    "SO_TSTT": [3104.07, 3104.07, 3104.07, 3104.07, 3104.07, 3104.07],
    "flow_assigned": [1350.00, 1350.00, 1350.00, 1350.00, 1350.00, 1350.00],
    "selfish_flow": [1350.00, 1350.00, 1350.00, 1350.00, 1350.00, 1350.00],
    "TSTT": [3104.07, 3104.07, 3104.07, 3104.07, 3104.07, 3104.07],
    "st_devs_t": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    "runtime": [0.49882, 0.58963, 0.52024, 0.53772, 0.51444, 0.51340],
    "st_devs": [0.03448, 0.14414, 0.03639, 0.05354, 0.03916, 0.02621]
}

ana_med = {
    "SO_TSTT": [9693.82, 9693.82, 9693.82, 9693.82, 9693.82, 9693.82],
    "flow_assigned": [4050.00, 4050.00, 4050.00, 4050.00, 4050.00, 4050.00],
    "selfish_flow": [4050.00, 4050.00, 4050.00, 4050.00, 4050.00, 4050.00],
    "TSTT": [9693.82, 9693.82, 9693.82, 10069.20, 9693.82, 9693.82],
    "st_devs_t": [0.0, 0.0, 0.0, 124.15, 0.0, 0.0],
    "runtime": [0.51303, 0.50823, 0.53056, 0.88218, 0.49687, 0.51121],
    "st_devs": [0.03874, 0.05147, 0.04313, 0.07175, 0.01982, 0.02263]
}

ana_high = {
    "SO_TSTT": [25577.72, 25577.72, 25577.72, 25577.72, 25577.72, 25577.72],
    "flow_assigned": [8100.00, 8100.00, 8100.00, 8100.00, 8100.00, 8100.00],
    "selfish_flow": [8100.00, 8100.00, 8100.00, 8100.00, 8100.00, 8100.00],
    "TSTT": [25559.33, 25577.72, 27082.24, 26028.03, 30426.63, 30533.22], 
    "st_devs_t": [23.65, 0.00, 1007.94, 475.97,  690.38, 649.31],
    "runtime": [0.88233, 0.97247, 0.91193, 0.92403, 0.65550, 0.98349],
    "st_devs": [0.07670, 0.18958, 0.08441, 0.09904, 0.17489, 0.17388]
}


def construct_congestion_lists(sf_dict):
    tstt_values = sf_dict['TSTT']
    std_tstt_values = sf_dict['st_devs_t']
    return tstt_values, std_tstt_values

congestion_ana_low, std_ana_low = construct_congestion_lists(ana_low)
congestion_ana_med, std_ana_med = construct_congestion_lists(ana_med)
congestion_ana_high, std_ana_high = construct_congestion_lists(ana_high)

congestion_ana_low = [value for i, value in enumerate(congestion_ana_low)][::-1]
congestion_ana_med = [value for i, value in enumerate(congestion_ana_med)][::-1]
congestion_ana_high = [value for i, value in enumerate(congestion_ana_high)][::-1]

std_ana_low = [value for i, value in enumerate(std_ana_low)][::-1]
std_ana_med = [value for i, value in enumerate(std_ana_med)][::-1]
std_ana_high = [value for i, value in enumerate(std_ana_high)][::-1]


colors = ['#1F4E79','#333333', '#2B7A2F', '#D04A4A', '#8C4B8C', '#D67C29'][::-1]
bar_labels = ['TASR', 'CC', 'SCALE', 'ASCALE', 'ALOOF', 'LLF'][::-1]

group_width = 6
group_spacing = 0.5
y_ana_low = np.arange(group_width) + 2 * (group_width + group_spacing)
y_ana_med = np.arange(group_width) + group_width + group_spacing
y_ana_high = np.arange(group_width)


fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.barh(y_ana_low, congestion_ana_low, height=0.6, color=colors, xerr=std_ana_low, capsize=5)
bars_med = ax.barh(y_ana_med, congestion_ana_med, height=0.6, color=colors, xerr=std_ana_med, capsize=5)
bars_high = ax.barh(y_ana_high, congestion_ana_high, height=0.6, color=colors, xerr=std_ana_high, capsize=5)

ax.set_yticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_yticklabels(['High', 'Med', 'Low'], fontsize=34, rotation=90, fontweight='bold')
ax.tick_params(axis='x', labelsize=34, bottom=True, top=True)
ax.tick_params(axis='y', which='both', pad=240)
ax.set_xlim(0.0, 1200000)

def format_func(value, tick_number):
    return f'{value * 1e-5:.1f}e5'

ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color) for color in colors]

combined_handles = legend_handles 
combined_labels = bar_labels

fig.legend(handles=combined_handles, labels=combined_labels, loc='upper right', bbox_to_anchor=(0.85, 0.98), ncol=2, frameon=True, fontsize=38)

plt.grid(axis='x', linestyle='--', alpha=0.5)

table0_data = [
    ['Mean', 'SD'],
]

table0 = ax.table(cellText=table0_data,
         loc='top',
         cellLoc='center',
         colLabels=None, 
         bbox=[-0.3, 0.97, 0.3, 0.05]) 

for key, cell in table0.get_celld().items():
    cell.set_edgecolor('white')

table0.auto_set_font_size(False)
table0.set_fontsize(34)
fig.subplots_adjust(left=0.3, top=0.7) 

table_data = [
    ['3104', '0'],
    ['3104', '0'],
    ['3104', '0'],
    ['3104', '0'],
    ['3104', '0'],
    ['3104', '0']
]

table = ax.table(cellText=table_data,
         loc='center',
         cellLoc='center',
         colLabels=None, 
         bbox=[-0.3, 0.67, 0.3, 0.3]) 

table.auto_set_font_size(False)
table.set_fontsize(34)
fig.subplots_adjust(left=0.3, top=0.7) 

table2_data = [
    ['9693', '0'],
    ['9693', '0'],
    ['9693', '0'],
    ['10069', '124'],
    ['9693', '0'],
    ['9693', '0'],
]
table2 = ax.table(cellText=table2_data,
         loc='center',
         cellLoc='center',
         colLabels=None, 
         bbox=[-0.3, 0.35, 0.3, 0.3]) 

table2.auto_set_font_size(False)
table2.set_fontsize(34)
fig.subplots_adjust(left=0.3) 

table3_data = [
    ['25559', '23'],
    ['25577', '0'],
    ['27082', '1007'],
    ['26028', '475'],
    ['30426', '690'],
    ['30533', '649'],
]

table3 = ax.table(cellText=table3_data,
         loc='center',
         cellLoc='center',
         colLabels=None, 
         bbox=[-0.3, 0.03, 0.3, 0.3]) 

table3.auto_set_font_size(False)
table3.set_fontsize(34)
fig.subplots_adjust(left=0.3) 

for (i, j), cell in table0.get_celld().items():
    text = cell.get_text()
    if i == 0:
        text.set_fontweight('bold')

ax.axhline(y=5.7, color='gray', linestyle='--', linewidth=1.5)
ax.axhline(y=12.2, color='gray', linestyle='--', linewidth=1.5)

fig.tight_layout()
plt.draw()
plt.tight_layout()
plt.show()
