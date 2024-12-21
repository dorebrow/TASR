# File: plot_mc_results_ana_er.py
# Purpose: Plots multi-commodity average total travel time (congestion) and standard deviations 
# for the Anaheim network under low, medium, and high demand levels. Includes horizontal
# bar chart and vertical table.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'

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

def calculate_efficiency_ratios_with_std(ana_dict):
    ratios = [tstt / so_tstt for tstt, so_tstt in zip(ana_dict['TSTT'], ana_dict['SO_TSTT'])]
    std_devs = [std_tstt / so_tstt for std_tstt, so_tstt in zip(ana_dict['st_devs_t'], ana_dict['SO_TSTT'])]
    return ratios, std_devs

efficiency_ana_low, std_ana_low = calculate_efficiency_ratios_with_std(ana_low)
efficiency_ana_med, std_ana_med = calculate_efficiency_ratios_with_std(ana_med)
efficiency_ana_high, std_ana_high = calculate_efficiency_ratios_with_std(ana_high)

efficiency_ana_low = [value for i, value in enumerate(efficiency_ana_low) if i != 1][::-1]
efficiency_ana_med = [value for i, value in enumerate(efficiency_ana_med) if i != 1][::-1]
efficiency_ana_high = [value for i, value in enumerate(efficiency_ana_high) if i != 1][::-1]

std_ana_low = [value for i, value in enumerate(std_ana_low) if i != 1][::-1]
std_ana_med = [value for i, value in enumerate(std_ana_med) if i != 1][::-1]
std_ana_high = [value for i, value in enumerate(std_ana_high) if i != 1][::-1]

#print(efficiency_ana_low)
#print(efficiency_ana_med)
#print(efficiency_ana_high)
#print(std_ana_low)
#print(std_ana_med)
#print(std_ana_high)

colors = ['#6B9BD2', '#7DCD7D', '#E06D6D', '#B58BB6', '#F6A04A'][::-1]
bar_labels = ['TASR','SCALE', 'ASCALE', 'ALOOF', 'LLF'][::-1]

group_width = 5
group_spacing = 0.5
y_ana_low = np.arange(group_width) + 2 * (group_width + group_spacing)
y_ana_med = np.arange(group_width) + group_width + group_spacing
y_ana_high = np.arange(group_width)


fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.barh(y_ana_low, efficiency_ana_low, height=0.6, color=colors, xerr=std_ana_low, capsize=5)
bars_med = ax.barh(y_ana_med, efficiency_ana_med, height=0.6, color=colors, xerr=std_ana_med, capsize=5)
bars_high = ax.barh(y_ana_high, efficiency_ana_high, height=0.6, color=colors, xerr=std_ana_high, capsize=5)

ax.set_yticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_yticklabels(['High', 'Med', 'Low'], fontsize=34, rotation=90, fontweight='bold')
ax.tick_params(axis='x', labelsize=34, bottom=True, top=True)
ax.tick_params(axis='y', which='both', pad=240)
ax.set_xlim(0.0, 1.5)

legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color) for color in colors]

combined_handles = legend_handles 
combined_labels = bar_labels

fig.legend(handles=combined_handles, labels=combined_labels, loc='lower center', columnspacing=0.5, bbox_to_anchor=(0.455, 0.00), ncol=5, frameon=True, fontsize=38)

plt.grid(axis='x', linestyle='--', alpha=0.5)

table0_data = [
    ['Mean', 'SD'],
]

table0 = ax.table(cellText=table0_data,
         loc='top',
         cellLoc='center',
         colLabels=None, 
         bbox=[-0.3, 0.97, 0.3, 0.05]) 

for key, cell in table0.get_celld().items():
    cell.set_edgecolor('white')

table0.auto_set_font_size(False)
table0.set_fontsize(34)
fig.subplots_adjust(left=0.3, top=0.7) 

def format_table_data(data):
    return [[f"{float(item):.2f}" for item in row] for row in data]

# Format the data
table_data = format_table_data([
    ['0.9342398535384759', '0.014680704651303014'],
    ['0.7962023324439047', '0.017426812825499315'],
    ['0.8492630112550389', '0.013149827211579184'],
    ['0.7263835468882466', '0.016433265784696255'],
    ['0.9583640338196013', '0.01742445183173161']
])

table2_data = format_table_data([
    ['0.6051321760351158', '0.10890383450433631'],
    ['0.355352352248558', '0.01910095879501218'],
    ['0.4096656682538129', '0.03377732867405137'],
    ['0.2981300801115163', '0.03610462278887485'],
    ['0.7396983695912582', '0.110087599112807'],
])

table3_data = format_table_data([
    ['0.3925593729670775', '0.14981368141322118'],
    ['0.1804213964033152', '0.02579727425554201'],
    ['0.24135093490138193', '0.051167904854215546'],
    ['0.1371390189462319', '0.04699587699886019'],
    ['0.5014552177977211', '0.15765889749303733'],
])

table = ax.table(cellText=table_data,
         loc='center',
         cellLoc='center',
         colLabels=None, 
         bbox=[-0.3, 0.67, 0.3, 0.3]) 

table.auto_set_font_size(False)
table.set_fontsize(34)
fig.subplots_adjust(left=0.3, top=0.7) 

table2 = ax.table(cellText=table2_data,
         loc='center',
         cellLoc='center',
         colLabels=None, 
         bbox=[-0.3, 0.35, 0.3, 0.3]) 

table2.auto_set_font_size(False)
table2.set_fontsize(34)
fig.subplots_adjust(left=0.3) 

table3 = ax.table(cellText=table3_data,
         loc='center',
         cellLoc='center',
         colLabels=None, 
         bbox=[-0.3, 0.03, 0.3, 0.3]) 

table3.auto_set_font_size(False)
table3.set_fontsize(34)
fig.subplots_adjust(left=0.3) 

for (i, j), cell in table0.get_celld().items():
    text = cell.get_text()
    if i == 0:
        text.set_fontweight('bold')

ax.axhline(y=4.7, color='gray', linestyle='--', linewidth=1.5)
ax.axhline(y=10.2, color='gray', linestyle='--', linewidth=1.5)

fig.tight_layout()
plt.draw()
plt.tight_layout()
plt.show()
