#File: plot_mc_results_aus_sr.py
#Purpose: Plots multi-commodity average ratio of serviced demand and standard deviations for 
#the Austin network under low, medium, and high demand levels. Includes table.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import math

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'

aus_low = {
    "SO_TSTT": [1476963546863.02, 1476963546863.02, 1476963546863.02, 1476963546863.02, 1476963546863.02, 1476963546863.02],
    "serviced_drivers": [20779125.27, 22907104.00, 18047738.35, 19748171.07, 17400659.39, 20995142.35],
    "serviced_drivers_st_devs": [106133.01, 0.00, 106895.74, 68443.28, 81522.63, 106977.44],
    "total_drivers": [22907104.00, 22907104.00, 22907104.00, 22907104.00, 22907104.00, 22907104.00],
    "TSTT": [60254505786.38, 1476963546863.02, 11505928759.35, 3088426018.15, 2861426674.06, 26158993380.55],
    "st_devs_t": [24234277461.47, 0.00, 3456818163.27, 1240915008.08, 1171466286.86, 8983500528.15],
    "runtime": [129.47174, 113.15083, 129.19513, 191.47883, 189.88957, 120.76576],
    "st_devs": [7.03187, 2.21966, 7.22586, 2.42736, 1.37445, 1.16726]
}

aus_med = {
    "SO_TSTT": [358881423098443.44, 358881423098443.44, 358881423098443.44, 358881423098443.44, 358881423098443.44, 358881423098443.44],
    "serviced_drivers": [62766565.37, 68721312.00, 54580210.41, 59591111.59, 52409986.65, 62946204.41],
    "serviced_drivers_st_devs": [351528.24, 0.00, 307322.04, 491004.99, 288910.58, 346284.50],
    "total_drivers": [68721312.00, 68721312.00, 68721312.00, 68721312.00, 68721312.00, 68721312.00],
    "TSTT": [20014125095017.79, 358881423098443.44, 9794465262850.35, 353912789143.60, 168853944481.59, 13224851526417.18],
    "st_devs_t": [6150019521522.28, 0.00, 2085565240734.02, 248660494974.22, 83287792193.81, 3678122331276.74],
    "runtime": [128.24407, 113.38804, 122.19929, 192.00570, 185.76705, 121.36129],
    "st_devs": [3.88499, 1.17564, 1.53082, 5.34350, 4.09993, 1.10989]
}

aus_high = {
    "SO_TSTT": [11484197769604214.00, 11484197769604214.00, 11484197769604214.00, 11484197769604214.00, 11484197769604214.00, 11484197769604214.00],
    "serviced_drivers": [126211063.78, 137442624.00, 109641775.00, 118772033.03, 105912110.75, 125809044.89],
    "serviced_drivers_st_devs": [539273.28, 0.00, 621849.86, 1284327.84, 472622.99, 597058.28],
    "total_drivers": [137442624.00, 137442624.00, 137442624.00, 137442624.00, 137442624.00, 137442624.00],
    "TSTT": [2095849182147911.25, 11484197769604214.00, 1519182363965060.50, 9930149518569.62, 5040426415306.59, 1637221131780826.50],
    "st_devs_t": [545213604220665.00, 0.00, 364410153049544.56, 8974467346936.88, 1758937303409.21, 422320982011527.25],
    "runtime": [128.59871, 114.40518, 122.40884, 191.99697, 187.62428, 130.68534],
    "st_devs": [5.78801, 1.60968, 2.19722, 14.15250, 2.15832, 4.26038]
}

def calculate_serviced_ratios_with_std(sf_dict):
    denom = sf_dict['serviced_drivers'][1]
    denom_std_dev = sf_dict['serviced_drivers_st_devs'][1]
    
    if denom == 0:
        raise ValueError("Denominator for runtime ratios cannot be zero.")
    
    ratios = [runtime / denom for runtime in sf_dict['serviced_drivers']]
    
    std_devs_propagated = [
        ratio * math.sqrt((std_dev / runtime) ** 2 + (denom_std_dev / denom) ** 2)
        if runtime != 0 else 0
        for runtime, std_dev, ratio in zip(sf_dict['serviced_drivers'], sf_dict['serviced_drivers_st_devs'], ratios)
    ]
    
    return ratios, std_devs_propagated

runtime_aus_low, std_aus_low = calculate_serviced_ratios_with_std(aus_low)
runtime_aus_med, std_aus_med = calculate_serviced_ratios_with_std(aus_med)
runtime_aus_high, std_aus_high = calculate_serviced_ratios_with_std(aus_high)

runtime_aus_low = [value for i, value in enumerate(runtime_aus_low) if i != 1]
runtime_aus_med = [value for i, value in enumerate(runtime_aus_med) if i != 1]
runtime_aus_high = [value for i, value in enumerate(runtime_aus_high) if i != 1]

std_aus_low = [value for i, value in enumerate(std_aus_low) if i != 1]
std_aus_med = [value for i, value in enumerate(std_aus_med) if i != 1]
std_aus_high = [value for i, value in enumerate(std_aus_high) if i != 1]

group_width = 5
group_spacing = 1
x_aus_low = np.arange(group_width)
x_aus_med = np.arange(group_width) + group_width + group_spacing
x_aus_high = np.arange(group_width) + 2 * (group_width + group_spacing)

colors = ['#1F4E79', '#2B7A2F', '#D04A4A', '#8C4B8C', '#D67C29']
bar_labels = ['TASR', 'SCALE', 'ASCALE', 'ALOOF', 'LLF']

fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.bar(x_aus_low, runtime_aus_low, width=0.8,  
                  color=colors, edgecolor=colors, hatch='/', alpha=0.7, 
                  yerr=std_aus_low, capsize=5)
bars_med = ax.bar(x_aus_med, runtime_aus_med, width=0.8,
                  color=colors, edgecolor=colors,  hatch='/', alpha=0.7, 
                  yerr=std_aus_med, capsize=5)
bars_high = ax.bar(x_aus_high, runtime_aus_high, width=0.8,
                   color=colors, edgecolor=colors, hatch='/', alpha=0.7, 
                   yerr=std_aus_high, capsize=5)

ax.set_xticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_xticklabels([])
ax.tick_params(axis='y', labelsize=34)
ax.set_ylim(0, 1)

legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color, alpha=0.7) for color in colors]

combined_handles = legend_handles
combined_labels = bar_labels

columns = ["Low", "Med", "High"]

mean_row = [
    ', '.join([f"{value:.2f}" for value in runtime_aus_low]),
    ', '.join([f"{value:.2f}" for value in runtime_aus_med]),
    ', '.join([f"{value:.2f}" for value in runtime_aus_high])
]

sd_row = [
    ', '.join([f"{value:.2f}" for value in std_aus_low]),
    ', '.join([f"{value:.2f}" for value in std_aus_med]),
    ', '.join([f"{value:.2f}" for value in std_aus_high])
]

rows = ["RT", "SD"]
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

plt.grid(axis='y', linestyle='--', alpha=0.5)
ax.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

ax.legend(
    combined_handles,
    combined_labels,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.2),
    columnspacing=0.5,
    ncol=6,
    fontsize=34
)

plt.tight_layout()
plt.show()
