#File: plot_sc_results_rr_pig_table.py
#Purpose: Plots single-commodity average runtime ratio (algorithmic runtime over CC runtime) 
#and standard deviations for the Pigou network under low, medium, and high demand levels.
#Includes table.

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import math


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

def calculate_runtime_ratios_with_std(sf_dict):
    denom = sf_dict['runtime'][1]
    denom_std_dev = sf_dict['st_devs'][1]
    
    if denom == 0:
        raise ValueError("Denominator for runtime ratios cannot be zero.")
    
    ratios = [runtime / denom for runtime in sf_dict['runtime']]
    
    std_devs_propagated = [
        ratio * math.sqrt((std_dev / runtime) ** 2 + (denom_std_dev / denom) ** 2)
        if runtime != 0 else 0
        for runtime, std_dev, ratio in zip(sf_dict['runtime'], sf_dict['st_devs'], ratios)
    ]
    
    return ratios, std_devs_propagated

runtime_pig_low, std_pig_low = calculate_runtime_ratios_with_std(pig_low)
runtime_pig_med, std_pig_med = calculate_runtime_ratios_with_std(pig_med)
runtime_pig_high, std_pig_high = calculate_runtime_ratios_with_std(pig_high)

runtime_pig_low = [value for i, value in enumerate(runtime_pig_low) if i != 1]
runtime_pig_med = [value for i, value in enumerate(runtime_pig_med) if i != 1]
runtime_pig_high = [value for i, value in enumerate(runtime_pig_high) if i != 1]

std_pig_low = [value for i, value in enumerate(std_pig_low) if i != 1]
std_pig_med = [value for i, value in enumerate(std_pig_med) if i != 1]
std_pig_high = [value for i, value in enumerate(std_pig_high) if i != 1]

group_width = 5
group_spacing = 1
x_pig_low = np.arange(group_width)
x_pig_med = np.arange(group_width) + group_width + group_spacing
x_pig_high = np.arange(group_width) + 2 * (group_width + group_spacing)

colors = ['#1F4E79', '#2B7A2F', '#D04A4A', '#8C4B8C', '#D67C29']
bar_labels = ['TASR','SCALE', 'ASCALE', 'ALOOF', 'LLF']

fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.bar(
    x_pig_low, runtime_pig_low, width=0.8, facecolor="none", 
    edgecolor=colors, linewidth=4.5, yerr=std_pig_low, capsize=5
)
bars_med = ax.bar(
    x_pig_med, runtime_pig_med, width=0.8, facecolor="none", 
    edgecolor=colors, linewidth=4.5, yerr=std_pig_med, capsize=5
)
bars_high = ax.bar(
    x_pig_high, runtime_pig_high, width=0.8, facecolor="none", 
    edgecolor=colors, linewidth=4.5, yerr=std_pig_high, capsize=5
)
ax.set_xticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_xticklabels(['Low', 'Med', 'High'], fontsize=34)
#ax.set_xticklabels(['Low', 'Med', 'High'], fontsize=34)
ax.set_xticklabels([])
ax.tick_params(axis='y', labelsize=34)
ax.set_ylim(0, 2)

legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color) for color in colors]

combined_handles = legend_handles
combined_labels = bar_labels

columns = ["Low", "Med", "High"]

mean_row = [
    ', '.join([f"{value:.2f}" for value in runtime_pig_low]),
    ', '.join([f"{value:.2f}" for value in runtime_pig_med]),
    ', '.join([f"{value:.2f}" for value in runtime_pig_high])
]

sd_row = [
    ', '.join([f"{value:.2f}" for value in std_pig_low]),
    ', '.join([f"{value:.2f}" for value in std_pig_med]),
    ', '.join([f"{value:.2f}" for value in std_pig_high])
]

rows = ["Mean", "SD"]
plt.subplots_adjust(bottom=0.3)

table_data = [mean_row, sd_row]

table = plt.table(cellText=table_data,
                  rowLabels=rows,
                  colLabels=columns,
                  loc='bottom',
                  cellLoc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1)

for (i, col) in enumerate(table.get_celld()):
    if i == 0 or i == 1 or i == 2:
        table[(0, i)].set_fontsize(34) 

column_widths = [group_width*0.8, group_width*0.8, group_width*0.8] 

cellDict = table.get_celld()
for x in range(1, len(rows)+1):
    cellDict[(x,-1)].set_height(0.1)
    cellDict[(x, -1)].set_fontsize(34) 

for i in range(len(columns)):
    table[(0, i)].set_height(0.1)

for i in range(len(columns)):
    table[(1, i)].set_height(0.1)

for i in range(len(columns)):
    table[(2, i)].set_height(0.1)


for row in range(1, len(rows)+1):
    for col in range(len(columns)):
        cellDict[(row, col)].set_fontsize(36)

ax.legend(
    combined_handles,
    combined_labels,
    loc='upper left',
    ncol=2,
    fontsize=34
)

plt.grid(axis='y', linestyle='--', alpha=0.5)

ax.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

ax.legend(
    combined_handles,
    combined_labels,
    loc='upper right',
    ncol=2,
    fontsize=34
)

plt.tight_layout()
plt.show()
