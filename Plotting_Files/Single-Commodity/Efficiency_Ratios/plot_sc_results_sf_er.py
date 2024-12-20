#File: plot_sc_results_sf.py
#Purpose: Plots single-commodity average efficiency ratios and standard deviations 
#for the Sioux Falls network under low, medium, and high demand levels.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

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
    "TSTT": [26805.00, 26805.00, 26805.00, 26805.00, 26805.00, 26805.00],
    "st_devs_t": [0.00, 0.00, 9.14, 1566.78, 0.00, 0.00],
    "runtime": [0.82194, 0.87103, 0.84028, 0.89421, 0.53976, 0.85893],
    "st_devs": [0.04383, 0.01213, 0.05914, 0.03376, 0.01324, 0.02453]
}

def calculate_efficiency_ratios_with_std(sf_dict):
    ratios = [tstt / so_tstt for tstt, so_tstt in zip(sf_dict['TSTT'], sf_dict['SO_TSTT'])]
    std_devs = [std_tstt / so_tstt for std_tstt, so_tstt in zip(sf_dict['st_devs_t'], sf_dict['SO_TSTT'])]
    return ratios, std_devs

efficiency_sf_low, std_sf_low = calculate_efficiency_ratios_with_std(sf_low)
efficiency_sf_med, std_sf_med = calculate_efficiency_ratios_with_std(sf_med)
efficiency_sf_high, std_sf_high = calculate_efficiency_ratios_with_std(sf_high)

efficiency_sf_low = [value for i, value in enumerate(efficiency_sf_low) if i != 1]
efficiency_sf_med = [value for i, value in enumerate(efficiency_sf_med) if i != 1]
efficiency_sf_high = [value for i, value in enumerate(efficiency_sf_high) if i != 1]

std_sf_low = [value for i, value in enumerate(std_sf_low) if i != 1]
std_sf_med = [value for i, value in enumerate(std_sf_med) if i != 1]
std_sf_high = [value for i, value in enumerate(std_sf_high) if i != 1]

group_width = 5
group_spacing = 1
x_sf_low = np.arange(group_width)
x_sf_med = np.arange(group_width) + group_width + group_spacing
x_sf_high = np.arange(group_width) + 2 * (group_width + group_spacing)

colors = ['#6B9BD2', '#7DCD7D', '#E06D6D', '#B58BB6', '#F6A04A']
bar_labels = ['TASR','SCALE', 'ASCALE', 'ALOOF', 'LLF']

fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.bar(x_sf_low, efficiency_sf_low, width=0.8, color=colors, yerr=std_sf_low, capsize=5)
bars_med = ax.bar(x_sf_med, efficiency_sf_med, width=0.8, color=colors, yerr=std_sf_med, capsize=5)
bars_high = ax.bar(x_sf_high, efficiency_sf_high, width=0.8, color=colors, yerr=std_sf_high, capsize=5)

ax.set_xticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_xticklabels(['Low', 'Med', 'High'], fontsize=34)
ax.tick_params(axis='y', labelsize=34)
ax.set_ylim(0.9, 1.5)

for i in range (0, len(bars_low)):
    ax.text(bars_low[i].get_x() + bars_low[i].get_width() / 2, bars_low[i].get_height(),  
            f'{efficiency_sf_low[i]:.2f} ± {std_sf_low[i]:.2f}', rotation=90, fontsize=34, 
            ha='right', va='bottom')
    
for i in range (0, len(bars_med)):
    ax.text(bars_med[i].get_x() + bars_med[i].get_width() / 2, bars_med[i].get_height(), 
            f'{efficiency_sf_med[i]:.2f} ± {std_sf_med[i]:.2f}', rotation=90, fontsize=34, 
            ha='right', va='bottom')
    
for i in range(len(bars_high)):
    ax.text(bars_high[i].get_x() + bars_high[i].get_width() / 2, bars_high[i].get_height(), 
            f'{efficiency_sf_high[i]:.2f} ± {std_sf_high[i]:.2f}', 
            rotation=90, fontsize=34, ha='right', va='bottom')


legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color) for color in colors]

combined_handles = legend_handles
combined_labels = bar_labels

ax.legend(
    combined_handles,
    combined_labels,
    loc='upper left',
    ncol=2,
    fontsize=30
)

plt.tight_layout()
plt.show()
