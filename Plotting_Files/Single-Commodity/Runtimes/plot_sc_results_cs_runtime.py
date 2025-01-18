#File: plot_sc_results_cs_runtime_table.py
#Purpose: Plots single-commodity average runtime and standard deviations for 
#the Chicago Sketch network under low, medium, and high demand levels.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import math

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
def calculate_average_and_std(cs_dict):
    runtimes = cs_dict['runtime']
    std_devs = cs_dict['st_devs']
    
    if any(runtime == 0 for runtime in runtimes):
        raise ValueError("Runtime values cannot be zero.")
    
    std_devs_propagated = [
        std_dev / math.sqrt(len(runtimes)) if len(runtimes) > 0 else 0
        for std_dev in std_devs
    ]
    
    return runtimes, std_devs_propagated

runtime_cs_low, std_cs_low = calculate_average_and_std(cs_low)
runtime_cs_med, std_cs_med = calculate_average_and_std(cs_med)
runtime_cs_high, std_cs_high = calculate_average_and_std(cs_high)

runtime_cs_low = [value for i, value in enumerate(runtime_cs_low)]
runtime_cs_med = [value for i, value in enumerate(runtime_cs_med)]
runtime_cs_high = [value for i, value in enumerate(runtime_cs_high)]

std_cs_low = [value for i, value in enumerate(std_cs_low)]
std_cs_med = [value for i, value in enumerate(std_cs_med)]
std_cs_high = [value for i, value in enumerate(std_cs_high)]

group_width = 6
group_spacing = 1
x_cs_low = np.arange(group_width)
x_cs_med = np.arange(group_width) + group_width + group_spacing
x_cs_high = np.arange(group_width) + 2 * (group_width + group_spacing)

colors = ['#1F4E79', '#707070', '#2B7A2F', '#D04A4A', '#8C4B8C', '#D67C29']
bar_labels = ['TASR', 'CC', 'SCALE', 'ASCALE', 'ALOOF', 'LLF']

fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.bar(x_cs_low, runtime_cs_low, width=0.8,  
                  color=colors, edgecolor=colors, alpha=0.7, 
                  yerr=std_cs_low, capsize=5)
bars_med = ax.bar(x_cs_med, runtime_cs_med, width=0.8,
                  color=colors, edgecolor=colors, alpha=0.7, 
                  yerr=std_cs_med, capsize=5)
bars_high = ax.bar(x_cs_high, runtime_cs_high, width=0.8,
                   color=colors, edgecolor=colors, alpha=0.7, 
                   yerr=std_cs_high, capsize=5)

ax.set_xticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
#ax.set_xticklabels(['Low', 'Med', 'High'], fontsize=30)
ax.set_xticklabels([])
ax.tick_params(axis='y', labelsize=34)
ax.set_ylim(0, 25)

legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color, alpha=0.7) for color in colors]

combined_handles = legend_handles
combined_labels = bar_labels

columns = ["Low", "Med", "High"]

mean_row = [
    ','.join([f"{value:.2f}" for value in runtime_cs_low]),
    ','.join([f"{value:.2f}" for value in runtime_cs_med]),
    ','.join([f"{value:.2f}" for value in runtime_cs_high])
]

sd_row = [
    ','.join([f"{value:.2f}" for value in std_cs_low]),
    ','.join([f"{value:.2f}" for value in std_cs_med]),
    ','.join([f"{value:.2f}" for value in std_cs_high])
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
