#File: plot_mc_results_sf_sr.py
#Purpose: Plots multi-commodity average ratio of serviced demand and standard deviations for 
#the Sioux Falls network under low, medium, and high demand levels. Includes table.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import math

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'

sf_low = {
    "SO_TSTT": [582973501.87, 582973501.87, 582973501.87, 582973501.87, 582973501.87, 582973501.87],
    "serviced_drivers": [964066.05, 993682.67, 787046.57, 841761.83, 674335.31, 954642.12],
    "serviced_drivers_st_devs": [4410.44, 0.00, 6325.40, 5639.30, 7672.26, 3992.85],
    "total_drivers": [993682.67, 993682.67, 993682.67, 993682.67, 993682.67, 993682.67],
    "TSTT": [804159568.66, 582973501.87, 206974287.73, 289604949.41, 143890205.50, 611764754.87],
    "st_devs_t": [41105698.99, 0.00, 11913662.01, 11179858.58, 15164506.52, 21762648.06],
    "runtime": [3.84519, 3.69513, 3.73775, 3.74515, 3.73974, 3.72840],
    "st_devs": [0.31390, 0.06050, 0.09550, 0.16789, 0.09935, 0.06216]
}

sf_high = {
    "SO_TSTT": [4448462379269.08, 4448462379269.08, 4448462379269.08, 4448462379269.08, 4448462379269.08, 4448462379269.08],
    "serviced_drivers": [5748316.43, 5962095.99, 4674886.99, 5020494.05, 4014115.35, 5690532.70],
    "serviced_drivers_st_devs": [28881.05, 0.00, 37073.76, 36711.77, 49964.35, 26719.36],
    "total_drivers": [5962095.99, 5962095.99, 5962095.99, 5962095.99, 5962095.99, 5962095.99],
    "TSTT": [4620420766981.41, 4448462379269.08, 1299570112670.39, 1976767343223.06, 683135547085.84, 4094171053276.15],
    "st_devs_t": [181194288738.82, 0.00, 43616098522.20, 64900328878.31, 39647338924.22, 126199578236.60],
    "runtime": [3.74191, 3.70840, 3.74690, 3.74332, 3.76833, 3.72830],
    "st_devs": [0.08128, 0.07374, 0.07115, 0.14797, 0.24951, 0.06519]
}

sf_med = {
    "SO_TSTT": [139045382901.32, 139045382901.32, 139045382901.32, 139045382901.32, 139045382901.32, 139045382901.32],
    "serviced_drivers": [2894739.78, 2981048.00, 2354680.13, 2518310.55, 2011744.60, 2864907.69],
    "serviced_drivers_st_devs": [12937.87, 0.00, 18392.58, 17896.50, 26661.37, 11404.48],
    "total_drivers": [2981048.00, 2981048.00, 2981048.00, 2981048.00, 2981048.00, 2981048.00],
    "TSTT": [158553580213.06, 139045382901.32, 43370046148.43, 64909179666.17, 24151771801.97, 135033269162.01], 
    "st_devs_t": [6436095886.48, 0.00, 1600876691.41, 2275483952.16, 1715691135.72, 3771775860.88],
    "runtime": [3.79983, 3.70684, 3.73757, 3.72682, 3.73759, 3.75182],
    "st_devs": [0.25186, 0.09174, 0.06320, 0.05987, 0.06829, 0.16431]
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

runtime_sf_low, std_sf_low = calculate_serviced_ratios_with_std(sf_low)
runtime_sf_med, std_sf_med = calculate_serviced_ratios_with_std(sf_med)
runtime_sf_high, std_sf_high = calculate_serviced_ratios_with_std(sf_high)

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
bar_labels = ['TASR', 'SCALE', 'ASCALE', 'ALOOF', 'LLF']

fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.bar(x_sf_low, runtime_sf_low, width=0.8,  
                  color=colors, edgecolor=colors, hatch='/', alpha=0.7, 
                  yerr=std_sf_low, capsize=5)
bars_med = ax.bar(x_sf_med, runtime_sf_med, width=0.8,
                  color=colors, edgecolor=colors,  hatch='/', alpha=0.7, 
                  yerr=std_sf_med, capsize=5)
bars_high = ax.bar(x_sf_high, runtime_sf_high, width=0.8,
                   color=colors, edgecolor=colors, hatch='/', alpha=0.7, 
                   yerr=std_sf_high, capsize=5)

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
    ', '.join([f"{value:.2f}" for value in runtime_sf_low]),
    ', '.join([f"{value:.2f}" for value in runtime_sf_med]),
    ', '.join([f"{value:.2f}" for value in runtime_sf_high])
]

sd_row = [
    ', '.join([f"{value:.2f}" for value in std_sf_low]),
    ', '.join([f"{value:.2f}" for value in std_sf_med]),
    ', '.join([f"{value:.2f}" for value in std_sf_high])
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
