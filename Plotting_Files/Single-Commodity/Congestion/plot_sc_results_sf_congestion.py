# File: plot_sc_results_sf_congestion_alt.py
# Purpose: Plots single-commodity average total travel time (congestion) and standard deviations 
# for the Sioux Falls network under low, medium, and high demand levels. 

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'

sf_low = {
    "SO_TSTT": [2540.74, 2540.74, 2540.74, 2540.74, 2540.74, 2540.74],
    "flow_assigned": [1269.63, 1269.63, 1269.63, 1269.63, 1269.63, 1269.63],
    "selfish_flow": [1269.63, 1269.63, 1269.63, 1269.63, 1269.63, 1269.63],
    "TSTT": [2540.74, 2540.74, 2540.74, 2540.74, 2540.74, 2540.74],
    "st_devs_t": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    "runtime": [0.52547, 0.56275, 0.53128, 0.54578, 0.57910, 0.54087],
    "st_devs": [0.03704, 0.02667, 0.03372, 0.01422, 0.01968, 0.01396]
}

sf_med = {
    "SO_TSTT": [7979.31, 7979.31, 7979.31, 7979.31, 7979.31, 7979.31],
    "flow_assigned": [3808.88, 3808.88, 3808.88, 3808.88, 3808.88, 3808.88],
    "selfish_flow": [3808.88, 3808.88, 3808.88, 3808.88, 3808.88, 3808.88],
    "TSTT": [7979.31, 7979.31, 7979.31, 7979.31, 7979.31, 7979.31],
    "st_devs_t": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    "runtime": [0.54320, 0.54017, 0.54447, 0.54236, 0.54296, 0.54279],
    "st_devs": [0.01817, 0.00992, 0.04048, 0.01007, 0.01176, 0.04080]
}

sf_high = {
    "SO_TSTT": [26759.90, 26759.90, 26759.90, 26759.90, 26759.90, 26759.90],
    "flow_assigned": [7617.76, 7617.76, 7617.76, 7617.76, 7617.76, 7617.76],
    "selfish_flow": [7617.76, 7617.76, 7617.76, 7617.76, 7617.76, 7617.76],
    "TSTT": [26759.90, 26759.90, 26774.23, 28491.72, 26805.00, 26805.00],
    "st_devs_t": [0.00, 0.00, 9.14, 1566.78, 0.00, 0.00],
    "runtime": [0.82194, 0.87103, 0.84028, 0.89421, 0.53976, 0.85893],
    "st_devs": [0.04383, 0.01213, 0.05914, 0.03376, 0.01324, 0.02453]
}


def construct_congestion_lists(sf_dict):
    tstt_values = sf_dict['TSTT']
    std_tstt_values = sf_dict['st_devs_t']
    return tstt_values, std_tstt_values

congestion_sf_low, std_sf_low = construct_congestion_lists(sf_low)
congestion_sf_med, std_sf_med = construct_congestion_lists(sf_med)
congestion_sf_high, std_sf_high = construct_congestion_lists(sf_high)

congestion_sf_low = [value for i, value in enumerate(congestion_sf_low)][::-1]
congestion_sf_med = [value for i, value in enumerate(congestion_sf_med)][::-1]
congestion_sf_high = [value for i, value in enumerate(congestion_sf_high)][::-1]

std_sf_low = [value for i, value in enumerate(std_sf_low)][::-1]
std_sf_med = [value for i, value in enumerate(std_sf_med)][::-1]
std_sf_high = [value for i, value in enumerate(std_sf_high)][::-1]


colors = ['#1F4E79','#333333', '#2B7A2F', '#D04A4A', '#8C4B8C', '#D67C29'][::-1]
bar_labels = ['TASR', 'CC', 'SCALE', 'ASCALE', 'ALOOF', 'LLF'][::-1]

group_width = 6
group_spacing = 0.5
y_sf_low = np.arange(group_width) + 2 * (group_width + group_spacing)
y_sf_med = np.arange(group_width) + group_width + group_spacing
y_sf_high = np.arange(group_width)


fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.barh(y_sf_low, congestion_sf_low, height=0.6, color=colors, xerr=std_sf_low, capsize=5)
bars_med = ax.barh(y_sf_med, congestion_sf_med, height=0.6, color=colors, xerr=std_sf_med, capsize=5)
bars_high = ax.barh(y_sf_high, congestion_sf_high, height=0.6, color=colors, xerr=std_sf_high, capsize=5)

ax.set_yticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_yticklabels(['High', 'Med', 'Low'], fontsize=34, rotation=90, fontweight='bold')
ax.tick_params(axis='x', labelsize=34, bottom=True, top=True)
ax.tick_params(axis='y', which='both', pad=10)
ax.set_xlim(0.0, 1200000)

def format_func(value, tick_number):
    return f'{value * 1e-5:.1f}e5'

ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color) for color in colors]

combined_handles = legend_handles 
combined_labels = bar_labels

fig.legend(handles=combined_handles, labels=combined_labels, loc='upper right', bbox_to_anchor=(0.85, 0.98), ncol=2, frameon=True, fontsize=38)

plt.grid(axis='x', linestyle='--', alpha=0.5)

ax.axhline(y=5.7, color='gray', linestyle='--', linewidth=1.5)
ax.axhline(y=12.2, color='gray', linestyle='--', linewidth=1.5)

fig.tight_layout()
plt.draw()
plt.tight_layout()
plt.show()
