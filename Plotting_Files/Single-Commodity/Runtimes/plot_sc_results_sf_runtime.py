#File: plot_sc_results_sf_runtime.py
#Purpose: Plots single-commodity average runtime and standard deviations for 
#the Sioux Falls network under low, medium, and high demand levels.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import math

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


def calculate_average_and_std(sf_dict):
    runtimes = sf_dict['runtime']
    std_devs = sf_dict['st_devs']
    
    if any(runtime == 0 for runtime in runtimes):
        raise ValueError("Runtime values cannot be zero.")
    
    std_devs_propagated = [
        std_dev / math.sqrt(len(runtimes)) if len(runtimes) > 0 else 0
        for std_dev in std_devs
    ]
    
    return runtimes, std_devs_propagated


runtime_sf_low, std_sf_low = calculate_average_and_std(sf_low)
runtime_sf_med, std_sf_med = calculate_average_and_std(sf_med)
runtime_sf_high, std_sf_high = calculate_average_and_std(sf_high)

runtime_sf_low = [value for i, value in enumerate(runtime_sf_low) if i != 1]
runtime_sf_med = [value for i, value in enumerate(runtime_sf_med) if i != 1]
runtime_sf_high = [value for i, value in enumerate(runtime_sf_high) if i != 1]

std_sf_low = [value for i, value in enumerate(std_sf_low) if i != 1]
std_sf_med = [value for i, value in enumerate(std_sf_med) if i != 1]
std_sf_high = [value for i, value in enumerate(std_sf_high) if i != 1]

group_width = 5
group_spacing = 1
x_sf_low = np.arange(group_width)
x_sf_med = np.arange(group_width) + group_width + group_spacing
x_sf_high = np.arange(group_width) + 2 * (group_width + group_spacing)

colors = ['#1F4E79', '#2B7A2F', '#D04A4A', '#8C4B8C', '#D67C29']
bar_labels = ['TASR','SCALE', 'ASCALE', 'ALOOF', 'LLF']


fig, ax = plt.subplots(figsize=(6, 6))


bars_low = ax.bar(x_sf_low, runtime_sf_low, width=0.8, color=colors, yerr=std_sf_low, capsize=5)
bars_med = ax.bar(x_sf_med, runtime_sf_med, width=0.8, color=colors, yerr=std_sf_med, capsize=5)
bars_high = ax.bar(x_sf_high, runtime_sf_high, width=0.8, color=colors, yerr=std_sf_high, capsize=5)

ax.set_xticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_xticklabels(['Low', 'Med', 'High'], fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.set_ylim(0,30)

fixed_offset = 0.5

for i in range(len(bars_low)):
    bar_height = bars_low[i].get_height()
    ax.text(
        bars_low[i].get_x() + bars_low[i].get_width() / 2, 
        bar_height + fixed_offset, 
        f'{runtime_sf_low[i]:.2f} ± {std_sf_low[i]:.2f}', 
        rotation=90, fontsize=20, ha='right', va='bottom', fontweight='bold'
    )

for i in range(len(bars_med)):
    bar_height = bars_med[i].get_height()
    ax.text(
        bars_med[i].get_x() + bars_med[i].get_width() / 2, 
        bar_height + fixed_offset, 
        f'{runtime_sf_med[i]:.2f} ± {std_sf_med[i]:.2f}', 
        rotation=90, fontsize=20, ha='right', va='bottom', fontweight='bold'
    )

for i in range(len(bars_high)):
    bar_height = bars_high[i].get_height()
    ax.text(
        bars_high[i].get_x() + bars_high[i].get_width() / 2, 
        bar_height + fixed_offset, 
        f'{runtime_sf_high[i]:.2f} ± {std_sf_high[i]:.2f}', 
        rotation=90, fontsize=20, ha='right', va='bottom', fontweight='bold'
    )


legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color) for color in colors]


combined_handles = legend_handles
combined_labels = bar_labels

ax.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)


ax.legend(
    combined_handles,
    combined_labels,
    loc='upper center',
    ncol=5,
    fontsize=24
)

plt.tight_layout()
plt.show()
