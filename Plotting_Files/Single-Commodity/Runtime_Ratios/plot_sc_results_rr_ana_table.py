#File: plot_sc_results_rr_ana_table.py
#Purpose: Plots single-commodity average runtime ratio (algorithmic runtime over CC runtime) 
#and standard deviations for the Anaheim network under low, medium, and high demand levels.
#Includes table.

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import math

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

runtime_ana_low, std_ana_low = calculate_runtime_ratios_with_std(ana_low)
runtime_ana_med, std_ana_med = calculate_runtime_ratios_with_std(ana_med)
runtime_ana_high, std_ana_high = calculate_runtime_ratios_with_std(ana_high)

runtime_ana_low = [value for i, value in enumerate(runtime_ana_low) if i != 1]
runtime_ana_med = [value for i, value in enumerate(runtime_ana_med) if i != 1]
runtime_ana_high = [value for i, value in enumerate(runtime_ana_high) if i != 1]

std_ana_low = [value for i, value in enumerate(std_ana_low) if i != 1]
std_ana_med = [value for i, value in enumerate(std_ana_med) if i != 1]
std_ana_high = [value for i, value in enumerate(std_ana_high) if i != 1]

group_width = 5
group_spacing = 1
x_ana_low = np.arange(group_width)
x_ana_med = np.arange(group_width) + group_width + group_spacing
x_ana_high = np.arange(group_width) + 2 * (group_width + group_spacing)

colors = ['#1F4E79', '#2B7A2F', '#D04A4A', '#8C4B8C', '#D67C29']
bar_labels = ['TASR','SCALE', 'ASCALE', 'ALOOF', 'LLF']

fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.bar(
    x_ana_low, runtime_ana_low, width=0.8, facecolor="none", 
    edgecolor=colors, linewidth=4.5, yerr=std_ana_low, capsize=5
)
bars_med = ax.bar(
    x_ana_med, runtime_ana_med, width=0.8, facecolor="none", 
    edgecolor=colors, linewidth=4.5, yerr=std_ana_med, capsize=5
)
bars_high = ax.bar(
    x_ana_high, runtime_ana_high, width=0.8, facecolor="none", 
    edgecolor=colors, linewidth=4.5, yerr=std_ana_high, capsize=5
)
ax.set_xticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_xticklabels(['Low', 'Med', 'High'], fontsize=34)
ax.set_xticklabels([])
ax.tick_params(axis='y', labelsize=34)
ax.set_ylim(0, 2)

legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color) for color in colors]

combined_handles = legend_handles
combined_labels = bar_labels

columns = ["Low", "Med", "High"]

mean_row = [
    ', '.join([f"{value:.2f}" for value in runtime_ana_low]),
    ', '.join([f"{value:.2f}" for value in runtime_ana_med]),
    ', '.join([f"{value:.2f}" for value in runtime_ana_high])
]

sd_row = [
    ', '.join([f"{value:.2f}" for value in std_ana_low]),
    ', '.join([f"{value:.2f}" for value in std_ana_med]),
    ', '.join([f"{value:.2f}" for value in std_ana_high])
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
