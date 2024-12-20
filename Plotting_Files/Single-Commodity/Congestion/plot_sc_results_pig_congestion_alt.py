# File: plot_sc_results_pig_congestion_alt.py
# Purpose: Plots single-commodity average total travel time (congestion) and standard deviations 
# for the Pigou network under low, medium, and high demand levels. Includes horizontal
# bar chart and vertical table.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'

pig_low = {
    "SO_TSTT": [500.02, 500.02, 500.02, 500.02, 500.02, 500.02],
    "flow_assigned": [25.00, 25.00, 25.00, 25.00, 25.00, 25.00],
    "selfish_flow": [25.00, 25.00, 25.00, 25.00, 25.00, 25.00],
    "TSTT": [500.03, 500.02, 500.08, 500.29, 500.29, 500.22],
    "st_devs_t": [0.02, 0.00, 0.05, 0.05, 0.12, 0.11],
    "runtime": [0.80378, 0.82581, 0.87960, 0.87646, 0.87642, 0.94837],
    "st_devs": [0.04226, 0.17641, 0.10181, 0.10645, 0.07027, 0.45453],
    "drivers": [25.00, 25.00, 25.00, 25.00, 25.00, 25.00],
}

pig_med = {
    "SO_TSTT": [1504.45, 1504.45, 1504.45, 1504.45, 1504.45, 1504.45],
    "flow_assigned": [75.0, 75.0, 75.0, 75.0, 75.0, 75.0],
    "selfish_flow": [75.0, 75.0, 75.0, 75.0, 75.0, 75.0],
    "TSTT": [1507.95, 1504.45, 1521.69, 1520.62, 1519.26, 1552.21],
    "st_devs_t": [5.62, 0.00, 12.21, 12.06, 11.99, 25.87],
    "runtime": [0.89452, 0.83683, 0.86312, 0.86490, 0.85911, 0.86281],
    "st_devs": [0.11822, 0.08921, 0.09300, 0.09478, 0.07674, 0.11934],
    "drivers": [75.00, 75.00, 75.00, 75.00, 75.00, 75.00]
}

pig_high = {
    "SO_TSTT": [3142.38, 3142.38, 3142.38, 3142.38, 3142.38, 3142.38],
    "flow_assigned": [150.00, 150.00, 150.00, 150.00, 150.00, 150.00],
    "selfish_flow": [150.00, 150.00, 150.00, 150.00, 150.00, 150.00],
    "TSTT": [3246.50, 3142.38, 3697.34, 3600.82, 3694.26, 4722.83], 
    "st_devs_t": [175.65, 0.00, 395.53, 385.08, 397.93, 809.47],
    "runtime": [0.82675, 0.87352, 0.89170, 0.88769, 0.83551, 0.87451],
    "st_devs": [0.11993, 0.19307, 0.14217, 0.10694, 0.06369, 0.06410],
    "drivers": [150.00, 150.00, 150.00, 150.00, 150.00, 150.00]
}

def construct_congestion_lists(sf_dict):
    tstt_values = sf_dict['TSTT']
    std_tstt_values = sf_dict['st_devs_t']
    return tstt_values, std_tstt_values

congestion_pig_low, std_pig_low = construct_congestion_lists(pig_low)
congestion_pig_med, std_pig_med = construct_congestion_lists(pig_med)
congestion_pig_high, std_pig_high = construct_congestion_lists(pig_high)

congestion_pig_low = [value for i, value in enumerate(congestion_pig_low)][::-1]
congestion_pig_med = [value for i, value in enumerate(congestion_pig_med)][::-1]
congestion_pig_high = [value for i, value in enumerate(congestion_pig_high)][::-1]

std_pig_low = [value for i, value in enumerate(std_pig_low)][::-1]
std_pig_med = [value for i, value in enumerate(std_pig_med)][::-1]
std_pig_high = [value for i, value in enumerate(std_pig_high)][::-1]


colors = ['#1F4E79','#333333', '#2B7A2F', '#D04A4A', '#8C4B8C', '#D67C29'][::-1]
bar_labels = ['TASR', 'CC', 'SCALE', 'ASCALE', 'ALOOF', 'LLF'][::-1]

group_width = 6
group_spacing = 0.5
y_pig_low = np.arange(group_width) + 2 * (group_width + group_spacing)
y_pig_med = np.arange(group_width) + group_width + group_spacing
y_pig_high = np.arange(group_width)


fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.barh(y_pig_low, congestion_pig_low, height=0.6, color=colors, xerr=std_pig_low, capsize=5)
bars_med = ax.barh(y_pig_med, congestion_pig_med, height=0.6, color=colors, xerr=std_pig_med, capsize=5)
bars_high = ax.barh(y_pig_high, congestion_pig_high, height=0.6, color=colors, xerr=std_pig_high, capsize=5)

ax.set_yticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_yticklabels(['High', 'Med', 'Low'], fontsize=34, rotation=90, fontweight='bold')
ax.tick_params(axis='x', labelsize=34, bottom=True, top=True)
ax.tick_params(axis='y', which='both', pad=240)
ax.set_xlim(0.0, 6000)

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
    ['500.03', '0.02'],
    ['500.02', '0.00'],
    ['500.08', '0.05'],
    ['500.29', '0.05'],
    ['500.29', '0.12'],
    ['500.22', '0.11']
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
    ['1507.95', '5.62'],
    ['1504.45', '0.00'],
    ['1521.69', '12.21'],
    ['1520.62', '12.06'],
    ['1519.26', '11.99'],
    ['1552.21', '25.87'],
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
    ['3246.50', '175.65'],
    ['3142.38', '0.00'],
    ['3697.34', '395.53'],
    ['3600.82', '385.08'],
    ['3694.26', '397.93'],
    ['4722.83', '809.47'],
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
