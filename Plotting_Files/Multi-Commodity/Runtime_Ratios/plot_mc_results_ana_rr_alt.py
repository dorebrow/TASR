#File: plot_mc_results_ana_rr_alt.py
#Purpose: Plots multi-commodity average runtime ratio (algorithmic runtime over CC runtime) 
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
    "SO_TSTT": [440492.48, 440492.48, 440492.48, 440492.48, 440492.48, 440492.48],
    "serviced_drivers": [108465.75, 114300.00, 93258.00, 98119.52, 84708.00, 110442.38],
    "serviced_drivers_st_devs": [1292.63 , 0.00, 1336.42, 1356.02, 1812.82, 1051.05],
    "total_drivers": [114300.00, 114300.00, 114300.00, 114300.00, 114300.00, 114300.00],
    "TSTT": [411525.63, 440492.48, 350721.14, 374093.97, 319966.49, 422152.15],
    "st_devs_t": [7675.34, 0.00, 7238.73, 5792.40, 7676.38, 6466.74],
    "runtime": [0.49000, 0.48280, 0.48861, 0.89224, 0.84512, 0.48874],
    "st_devs": [0.01319, 0.00770, 0.00879, 0.05580, 0.03241, 0.00721]
}

ana_med = {
    "SO_TSTT": [4550752.71, 4550752.71, 4550752.71, 4550752.71, 4550752.71, 4550752.71],
    "serviced_drivers": [320169.38, 342900.00, 277627.50, 290139.89, 255418.88, 327469.50],
    "serviced_drivers_st_devs": [5356.45, 0.00, 4470.82, 3905.73, 5270.22, 3942.57],
    "total_drivers": [342900.00, 342900.00, 342900.00, 342900.00, 342900.00, 342900.00],
    "TSTT": [2753806.89, 4550752.71, 1617120.68, 1864287.15, 1356716.27, 3366184.36],
    "st_devs_t": [500981.44, 0.00, 164303.21, 153712.27, 86923.74, 495594.42],
    "runtime": [0.48922, 0.48098, 0.48955, 2.62365, 1.60688, 0.48880],
    "st_devs": [0.00805, 0.00789, 0.00772, 0.21023, 0.17628, 0.00946]
}

ana_high = {
    "SO_TSTT": [107190741.65, 107190741.65, 107190741.65, 107190741.65, 107190741.65, 107190741.65],
    "serviced_drivers": [629862.75, 685800.00, 551292.75, 582666.81, 511336.93, 645873.75],
    "serviced_drivers_st_devs": [11849.53, 0.00, 11005.96, 8438.37, 10454.13, 8485.89],
    "total_drivers": [685800.00, 685800.00, 685800.00, 685800.00, 685800.00, 685800.00],
    "TSTT": [42078730.33, 107190741.65, 19339503.29, 25870585.71, 14700033.15, 53751356.70], 
    "st_devs_t": [16899574.15, 0.00, 5037522.91, 5484725.67, 2765228.96, 16058639.62],
    "runtime": [0.48490, 0.48310, 0.48818, 3.71333, 3.19644, 0.48709],
    "st_devs": [0.00841, 0.00823, 0.00782, 0.34562, 0.75633, 0.00853]
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

plt.grid(axis='y', linestyle='--', alpha=0.5)

ax.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

ax.legend(handles=combined_handles, 
          labels=combined_labels, 
          loc='lower center', 
          columnspacing=0.5, 
          bbox_to_anchor=(0.5, -0.55), 
          ncol=5, 
          frameon=True, 
          fontsize=38)


plt.tight_layout()
plt.show()
