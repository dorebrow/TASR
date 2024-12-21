# File: plot_mc_results_aus_er.py
# Purpose: Plots multi-commodity average total travel time (congestion) and standard deviations 
# for the Austin network under low, medium, and high demand levels. Includes horizontal
# bar chart and vertical table.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

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

def calculate_efficiency_ratios_with_std(aus_dict):
    ratios = [tstt / so_tstt for tstt, so_tstt in zip(aus_dict['TSTT'], aus_dict['SO_TSTT'])]
    std_devs = [std_tstt / so_tstt for std_tstt, so_tstt in zip(aus_dict['st_devs_t'], aus_dict['SO_TSTT'])]
    return ratios, std_devs

efficiency_aus_low, std_aus_low = calculate_efficiency_ratios_with_std(aus_low)
efficiency_aus_med, std_aus_med = calculate_efficiency_ratios_with_std(aus_med)
efficiency_aus_high, std_aus_high = calculate_efficiency_ratios_with_std(aus_high)

efficiency_aus_low = [value for i, value in enumerate(efficiency_aus_low) if i != 1][::-1]
efficiency_aus_med = [value for i, value in enumerate(efficiency_aus_med) if i != 1][::-1]
efficiency_aus_high = [value for i, value in enumerate(efficiency_aus_high) if i != 1][::-1]

std_aus_low = [value for i, value in enumerate(std_aus_low) if i != 1][::-1]
std_aus_med = [value for i, value in enumerate(std_aus_med) if i != 1][::-1]
std_aus_high = [value for i, value in enumerate(std_aus_high) if i != 1][::-1]

#print(efficiency_aus_low)
#print(efficiency_aus_med)
#print(efficiency_aus_high)
#print(std_aus_low)
#print(std_aus_med)
#print(std_aus_high)

colors = ['#6B9BD2', '#7DCD7D', '#E06D6D', '#B58BB6', '#F6A04A'][::-1]
bar_labels = ['TASR','SCALE', 'ASCALE', 'ALOOF', 'LLF'][::-1]

group_width = 5
group_spacing = 0.5
y_aus_low = np.arange(group_width) + 2 * (group_width + group_spacing)
y_aus_med = np.arange(group_width) + group_width + group_spacing
y_aus_high = np.arange(group_width)


fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.barh(y_aus_low, efficiency_aus_low, height=0.6, color=colors, xerr=std_aus_low, capsize=5)
bars_med = ax.barh(y_aus_med, efficiency_aus_med, height=0.6, color=colors, xerr=std_aus_med, capsize=5)
bars_high = ax.barh(y_aus_high, efficiency_aus_high, height=0.6, color=colors, xerr=std_aus_high, capsize=5)

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
    ['0.01771133311726623', '0.006082411815261388'],
    ['0.0019373712236415684', '0.0007931585646430627'],
    ['0.002091064484773255', '0.0008401798478477193'],
    ['0.007790259132520831', '0.0023404898317308303'],
    ['0.04079620374812694', '0.016408175755550716']
])

table2_data = format_table_data([
    ['0.03685019807444734', '0.01024885127661737'],
    ['0.0004705006545721156', '0.00023207607536421195'],
    ['0.000986155221097971', '0.0006928764738708998'],
    ['0.027291647414593723', '0.005811293386902159'],
    ['0.055768072145455656', '0.017136633789582613'],
])

table3_data = format_table_data([
    ['0.14256295168602368', '0.03677409519446842'],
    ['0.0004389010461529435', '0.0001531615301910487'],
    ['0.0008646794245264767', '0.0007814622777300162'],
    ['0.13228458743421803', '0.03173144179161096'],
    ['0.1824985274718185', '0.04747511451463405'],
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
