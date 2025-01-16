# File: plot_sc_results_cs_congestion_table.py
# Purpose: Plots single-commodity average total travel time (congestion) and standard deviations 
# for the Chicago Sketch network under low, medium, and high demand levels. Includes horizontal
# bar chart and vertical table.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'


cs_low = {
    "SO_TSTT": [5046.88, 5046.88, 5046.88, 5046.88, 5046.88, 5046.88],
    "flow_assigned": [500.00, 500.00, 500.00, 500.00, 500.00, 500.00],
    "selfish_flow": [500.00, 500.00, 500.00, 500.00, 500.00, 500.00],
    "TSTT": [5046.88, 5046.88, 5046.88, 5046.88, 5046.88, 5046.88],
    "st_devs_t": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    "runtime": [3.21324, 3.26377, 3.24141, 3.22720, 3.23883, 3.13765],
    "st_devs": [0.06163, 0.07470, 0.28971, 0.05768, 0.02688, 0.09414],
    "drivers": [500.00, 500.00, 500.00, 500.00, 500.00, 500.00]
}

cs_med = {
    "SO_TSTT": [21085.83, 21085.83, 21085.83, 21085.83, 21085.83, 21085.83],
    "flow_assigned": [1500.00, 1500.00, 1500.00, 1500.00, 1500.00, 1500.00],
    "selfish_flow": [1500.00, 1500.00, 1500.00, 1500.00, 1500.00, 1500.00],
    "TSTT": [21096.84, 21085.83, 22573.84, 21681.54, 25945.24, 25958.20],
    "st_devs_t": [16.05, 0.00, 1081.75, 334.96, 890.78, 552.35],
    "runtime": [3.60566, 3.59844, 3.69611, 3.57403, 3.43428, 3.61350],
    "st_devs": [0.08687, 0.03848, 0.44191, 0.03658, 0.40641, 0.23425],
    "drivers": [1500.00, 1500.00, 1500.00, 1500.00, 1500.00, 1500.00]
}

cs_high = {
    "SO_TSTT": [52220.26, 52220.26, 52220.26, 52220.26, 52220.26, 52220.26],
    "flow_assigned": [2500.00, 2500.00, 2500.00, 2500.00, 2500.00, 2500.00],
    "selfish_flow": [2500.00, 2500.00, 2500.00, 2500.00, 2500.00, 2500.00],
    "TSTT": [77934.78, 52220.26, 107803.94, 102753.53, 292588.76, 232749.83],
    "st_devs_t": [33000.95, 0.00, 51563.44, 54071.97, 131749.03, 132346.12],
    "runtime": [4.29291, 4.23867, 4.28391, 4.32917, 4.27108, 4.31209],
    "st_devs": [0.15863, 0.11928, 0.18374, 0.19842, 0.21467, 0.25684],
    "drivers": [3000.00, 3000.00, 3000.00, 3000.00, 3000.00, 3000.00]
}


def construct_congestion_lists(sf_dict):
    tstt_values = sf_dict['TSTT']
    std_tstt_values = sf_dict['st_devs_t']
    return tstt_values, std_tstt_values

congestion_cs_low, std_cs_low = construct_congestion_lists(cs_low)
congestion_cs_med, std_cs_med = construct_congestion_lists(cs_med)
congestion_cs_high, std_cs_high = construct_congestion_lists(cs_high)

#Uncomment for values
'''print(congestion_cs_low)
print(std_cs_low)
print(congestion_cs_med)
print(std_cs_med)
print(congestion_cs_high)
print(std_cs_high)'''

congestion_cs_low = [value for i, value in enumerate(congestion_cs_low)][::-1]
congestion_cs_med = [value for i, value in enumerate(congestion_cs_med)][::-1]
congestion_cs_high = [value for i, value in enumerate(congestion_cs_high)][::-1]

std_cs_low = [value for i, value in enumerate(std_cs_low)][::-1]
std_cs_med = [value for i, value in enumerate(std_cs_med)][::-1]
std_cs_high = [value for i, value in enumerate(std_cs_high)][::-1]


colors = ['#1F4E79','#333333', '#2B7A2F', '#D04A4A', '#8C4B8C', '#D67C29'][::-1]
bar_labels = ['TASR', 'CC', 'SCALE', 'ASCALE', 'ALOOF', 'LLF'][::-1]

group_width = 6
group_spacing = 0.5
y_cs_low = np.arange(group_width) + 2 * (group_width + group_spacing)
y_cs_med = np.arange(group_width) + group_width + group_spacing
y_cs_high = np.arange(group_width)


fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.barh(y_cs_low, congestion_cs_low, height=0.6, color=colors, xerr=std_cs_low, capsize=5)
bars_med = ax.barh(y_cs_med, congestion_cs_med, height=0.6, color=colors, xerr=std_cs_med, capsize=5)
bars_high = ax.barh(y_cs_high, congestion_cs_high, height=0.6, color=colors, xerr=std_cs_high, capsize=5)

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
    ['5046', '0'],
    ['5046', '0'],
    ['5046', '0'],
    ['5046', '0'],
    ['5046', '0'],
    ['5046', '0'],
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
    ['21096', '16'],
    ['21085', '0'],
    ['22573', '1080'],
    ['21681', '334'],
    ['25945', '890'],
    ['25958', '552'],
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
    ['77934', '33000'],
    ['52220', '0'],
    ['107803', '51563'],
    ['102753', '54071'],
    ['292588', '131749'],
    ['232749', '132346'],
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
