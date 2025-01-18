#File: plot_sc_results_aus_runtime_table.py
#Purpose: Plots single-commodity average runtime and standard deviations for 
#the Austin network under low, medium, and high demand levels.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import math

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'

aus_low = {
    #TASR, CC, SCALE, ASCALE, ALOOF, LLF
    "SO_TSTT": [38021.89, 38021.89, 38021.89, 38021.89, 38021.89, 38021.89],
    "flow_assigned": [24999.75, 24999.75, 24999.75, 24999.75, 24999.75, 24999.75],
    "selfish_flow": [24999.75, 24999.75, 24999.75, 24999.75, 24999.75, 24999.75],
    "TSTT": [38021.89, 38021.89, 38021.89, 38021.89, 38021.89, 119068.54],
    "st_devs_t": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    "runtime": [17.46001, 17.35566, 16.88342, 16.86667, 17.59253,  20.09164],
    "st_devs": [0.28568, 0.29585, 0.26978, 7.47353, 0.26525, 4.08561]
}

aus_med = {
    "SO_TSTT": [119409.35, 119409.35, 119409.35, 119409.35, 119409.35, 119409.35],
    "flow_assigned": [74999.25, 74999.25, 74999.25, 74999.25, 74999.25, 74999.25],
    "selfish_flow": [74999.25, 74999.25, 74999.25, 74999.25, 74999.25, 74999.25],
    "TSTT": [119409.35, 119409.35, 119409.35, 120788.30, 119409.35, 373939.82],
    "st_devs_t": [0.00, 0.00, 0.00, 420.10, 0.00, 0.00],
    "runtime": [17.65701, 17.19939, 17.01263, 17.24920, 16.86035, 16.87601],
    "st_devs": [0.39296, 0.25531, 0.28932, 0.32411, 0.26844, 0.27720]
}

aus_high = {
    "SO_TSTT": [365877.25, 365877.25, 365877.25, 365877.25, 365877.25, 365877.25],
    "flow_assigned": [149998.50, 149998.50, 149998.50, 149998.50, 149998.50, 149998.50],
    "selfish_flow": [149998.50, 149998.50, 149998.50, 149998.50, 149998.50, 149998.50],
    "TSTT": [365877.25, 365877.25, 371305.82, 369930.72, 393007.21, 1256181.19],
    "st_devs_t": [0.00, 0.00, 11136.52, 11629.40, 12715.16, 0.00],
    "runtime": [17.94908, 17.93724, 17.20328, 17.28063, 18.28812, 17.34867],
    "st_devs": [0.43738, 0.43165, 0.27002, 0.26509, 9.93242, 0.28261]
}


def calculate_average_and_std(aus_dict):
    runtimes = aus_dict['runtime']
    std_devs = aus_dict['st_devs']
    
    if any(runtime == 0 for runtime in runtimes):
        raise ValueError("Runtime values cannot be zero.")
    
    std_devs_propagated = [
        std_dev / math.sqrt(len(runtimes)) if len(runtimes) > 0 else 0
        for std_dev in std_devs
    ]
    
    return runtimes, std_devs_propagated

runtime_aus_low, std_aus_low = calculate_average_and_std(aus_low)
runtime_aus_med, std_aus_med = calculate_average_and_std(aus_med)
runtime_aus_high, std_aus_high = calculate_average_and_std(aus_high)

runtime_aus_low = [value for i, value in enumerate(runtime_aus_low)]
runtime_aus_med = [value for i, value in enumerate(runtime_aus_med)]
runtime_aus_high = [value for i, value in enumerate(runtime_aus_high)]

std_aus_low = [value for i, value in enumerate(std_aus_low)]
std_aus_med = [value for i, value in enumerate(std_aus_med)]
std_aus_high = [value for i, value in enumerate(std_aus_high)]

group_width = 6
group_spacing = 1
x_aus_low = np.arange(group_width)
x_aus_med = np.arange(group_width) + group_width + group_spacing
x_aus_high = np.arange(group_width) + 2 * (group_width + group_spacing)

colors = ['#1F4E79', '#707070', '#2B7A2F', '#D04A4A', '#8C4B8C', '#D67C29']
bar_labels = ['TASR', 'CC', 'SCALE', 'ASCALE', 'ALOOF', 'LLF']

fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.bar(x_aus_low, runtime_aus_low, width=0.8,  
                  color=colors, edgecolor=colors, alpha=0.7, 
                  yerr=std_aus_low, capsize=5)
bars_med = ax.bar(x_aus_med, runtime_aus_med, width=0.8,
                  color=colors, edgecolor=colors, alpha=0.7, 
                  yerr=std_aus_med, capsize=5)
bars_high = ax.bar(x_aus_high, runtime_aus_high, width=0.8,
                   color=colors, edgecolor=colors, alpha=0.7, 
                   yerr=std_aus_high, capsize=5)

ax.set_xticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_xticklabels([])
ax.tick_params(axis='y', labelsize=34)
ax.set_ylim(0, 25)

legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color, alpha=0.7) for color in colors]

combined_handles = legend_handles
combined_labels = bar_labels

columns = ["Low", "Med", "High"]

mean_row = [
    ','.join([f"{value:.1f}" for value in runtime_aus_low]),
    ','.join([f"{value:.1f}" for value in runtime_aus_med]),
    ',' .join([f"{value:.1f}" for value in runtime_aus_high])
]

sd_row = [
    ','.join([f"{value:.2f}" for value in std_aus_low]),
    ','.join([f"{value:.2f}" for value in std_aus_med]),
    ','.join([f"{value:.2f}" for value in std_aus_high])
]

plt.grid(axis='y', linestyle='--', alpha=0.5)
ax.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

ax.legend(
    combined_handles,
    combined_labels,
    loc='upper center',
    columnspacing=0.5,
    ncol=6,
    fontsize=34
)

plt.tight_layout()
plt.show()
