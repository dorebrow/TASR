#File: plot_sc_results_cs.py
#Purpose: Plots single-commodity average efficiency ratios and standard deviations 
#for the Chicago Sketch network under low, medium, and high demand levels.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

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

def calculate_efficiency_ratios_with_std(cs_dict):
    ratios = [tstt / so_tstt for tstt, so_tstt in zip(cs_dict['TSTT'], cs_dict['SO_TSTT'])]
    std_devs = [std_tstt / so_tstt for std_tstt, so_tstt in zip(cs_dict['st_devs_t'], cs_dict['SO_TSTT'])]
    return ratios, std_devs

efficiency_cs_low, std_cs_low = calculate_efficiency_ratios_with_std(cs_low)
efficiency_cs_med, std_cs_med = calculate_efficiency_ratios_with_std(cs_med)
efficiency_cs_high, std_cs_high = calculate_efficiency_ratios_with_std(cs_high)

efficiency_cs_low = [value for i, value in enumerate(efficiency_cs_low) if i != 1]
efficiency_cs_med = [value for i, value in enumerate(efficiency_cs_med) if i != 1]
efficiency_cs_high = [value for i, value in enumerate(efficiency_cs_high) if i != 1]

std_cs_low = [value for i, value in enumerate(std_cs_low) if i != 1]
std_cs_med = [value for i, value in enumerate(std_cs_med) if i != 1]
std_cs_high = [value for i, value in enumerate(std_cs_high) if i != 1]

group_width = 5
group_spacing = 1
x_cs_low = np.arange(group_width)
x_cs_med = np.arange(group_width) + group_width + group_spacing
x_cs_high = np.arange(group_width) + 2 * (group_width + group_spacing)

colors = ['#6B9BD2', '#7DCD7D', '#E06D6D', '#B58BB6', '#F6A04A']
bar_labels = ['TASR','SCALE', 'ASCALE', 'ALOOF', 'LLF']

fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.bar(x_cs_low, efficiency_cs_low, width=0.8, color=colors, yerr=std_cs_low, capsize=5)
bars_med = ax.bar(x_cs_med, efficiency_cs_med, width=0.8, color=colors, yerr=std_cs_med, capsize=5)
bars_high = ax.bar(x_cs_high, efficiency_cs_high, width=0.8, color=colors, yerr=std_cs_high, capsize=5)

ax.set_xticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_xticklabels(['Low', 'Med', 'High'], fontsize=34)
ax.tick_params(axis='y', labelsize=34)
ax.set_ylim(0.9, 1.5)

for i in range (0, len(bars_low)):
    ax.text(bars_low[i].get_x() + bars_low[i].get_width() / 2, bars_low[i].get_height(), 
            f'{efficiency_cs_low[i]:.2f} ± {std_cs_low[i]:.2f}', rotation=90, fontsize=34, 
            ha='right', va='bottom')
    
for i in range (0, len(bars_med)):
    ax.text(bars_med[i].get_x() + bars_med[i].get_width() / 2, bars_med[i].get_height(), 
            f'{efficiency_cs_med[i]:.2f} ± {std_cs_med[i]:.2f}', rotation=90, fontsize=34, 
            ha='right', va='bottom')
    
for i in range(len(bars_high)):
    ax.text(bars_high[i].get_x() + bars_high[i].get_width() / 2, bars_low[i].get_height(), 
            f'{efficiency_cs_high[i]:.2f} ± {std_cs_high[i]:.2f}', 
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
