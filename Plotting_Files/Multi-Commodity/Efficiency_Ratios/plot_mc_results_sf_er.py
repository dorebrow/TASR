# File: plot_mc_results_sf_er.py
# Purpose: Plots multi-commodity average total travel time (congestion) and standard deviations 
# for the Sioux Falls network under low, medium, and high demand levels. Includes horizontal
# bar chart and vertical table.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'

sf_low = {
    "SO_TSTT": [582973501.87, 582973501.87, 582973501.87, 582973501.87, 582973501.87, 582973501.87],
    "serviced_drivers": [964066.05, 114300.00, 787046.57, 841761.83, 674335.31, 954642.12],
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

def calculate_efficiency_ratios_with_std(sf_dict):
    ratios = [tstt / so_tstt for tstt, so_tstt in zip(sf_dict['TSTT'], sf_dict['SO_TSTT'])]
    std_devs = [std_tstt / so_tstt for std_tstt, so_tstt in zip(sf_dict['st_devs_t'], sf_dict['SO_TSTT'])]
    return ratios, std_devs

efficiency_sf_low, std_sf_low = calculate_efficiency_ratios_with_std(sf_low)
efficiency_sf_med, std_sf_med = calculate_efficiency_ratios_with_std(sf_med)
efficiency_sf_high, std_sf_high = calculate_efficiency_ratios_with_std(sf_high)

efficiency_sf_low = [value for i, value in enumerate(efficiency_sf_low) if i != 1][::-1]
efficiency_sf_med = [value for i, value in enumerate(efficiency_sf_med) if i != 1][::-1]
efficiency_sf_high = [value for i, value in enumerate(efficiency_sf_high) if i != 1][::-1]

std_sf_low = [value for i, value in enumerate(std_sf_low) if i != 1][::-1]
std_sf_med = [value for i, value in enumerate(std_sf_med) if i != 1][::-1]
std_sf_high = [value for i, value in enumerate(std_sf_high) if i != 1][::-1]

#print(efficiency_sf_low)
#print(efficiency_sf_med)
#print(efficiency_sf_high)
#print(std_sf_low)
#print(std_sf_med)
#print(std_sf_high)

colors = ['#6B9BD2', '#7DCD7D', '#E06D6D', '#B58BB6', '#F6A04A'][::-1]
bar_labels = ['TASR','SCALE', 'ASCALE', 'ALOOF', 'LLF'][::-1]

group_width = 5
group_spacing = 0.5
y_sf_low = np.arange(group_width) + 2 * (group_width + group_spacing)
y_sf_med = np.arange(group_width) + group_width + group_spacing
y_sf_high = np.arange(group_width)


fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.barh(y_sf_low, efficiency_sf_low, height=0.6, color=colors, xerr=std_sf_low, capsize=5)
bars_med = ax.barh(y_sf_med, efficiency_sf_med, height=0.6, color=colors, xerr=std_sf_med, capsize=5)
bars_high = ax.barh(y_sf_high, efficiency_sf_high, height=0.6, color=colors, xerr=std_sf_high, capsize=5)

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
    ['1.0493868982168941', '0.037330424093362916'],
    ['0.24682117632867429', '0.026012342707441967'],
    ['0.49677206336314816', '0.0191773014453289'],
    ['0.35503206760871636', '0.02043602663205897'],
    ['1.379410155145136', '0.07051040717656212']
])

table2_data = format_table_data([
    ['0.9711452933165181', '0.027126221541328096'],
    ['0.17369704263470886', '0.012339073041624257'],
    ['0.46682010083165293', '0.016365045028319296'],
    ['0.31191288227966235', '0.011513339443612712'],
    ['1.1403009355987381', '0.046287735357941895'],
])

table3_data = format_table_data([
    ['0.9203564522330201', '0.028369258291296523'],
    ['0.15356666839971903', '0.00891259395808005'],
    ['0.4443709252067137', '0.014589384678346693'],
    ['0.29213917121716115', '0.009804758319517696'],
    ['1.038655691124578', '0.040731891896676385'],
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
