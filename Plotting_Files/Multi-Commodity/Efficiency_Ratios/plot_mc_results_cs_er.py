# File: plot_mc_results_cs_er.py
# Purpose: Plots multi-commodity average total travel time (congestion) and standard deviations 
# for the Chicago Sketch network under low, medium, and high demand levels. Includes horizontal
# bar chart and vertical table.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'

cs_low = {
    "SO_TSTT": [21265561.87, 21265561.87, 21265561.87, 21265561.87, 21265561.87, 21265561.87],
    "serviced_drivers": [3149097.81, 5996375.00, 3016275.62, 3014860.32, 3039924.92, 3086977.81],
    "serviced_drivers_st_devs": [17536.40, 0.00, 15580.63, 18786.83, 17853.74, 15116.73],
    "total_drivers": [5996375.00, 5996375.00, 5996375.00, 5996375.00, 5996375.00, 5996375.00],
    "TSTT": [335195944696.52, 21265561.87, 323233668821.47, 239663921197.57, 239614096942.19, 333872729689.05],
    "st_devs_t": [19116237843.97, 0.00, 20738068069.50, 13798227110.96, 14688853734.13, 20519369932.27],
    "runtime": [8.73655, 8.00838, 8.73940, 63.20748, 38.51555, 8.72854],
    "st_devs": [0.04925, 0.06677, 0.08117, 0.83794, 1.61989, 0.05208]
}

cs_med = {
    "SO_TSTT": [3768387034.92, 3768387034.92, 3768387034.92, 3768387034.92, 3768387034.92, 3768387034.92],
    "serviced_drivers": [9579463.12, 17989125.00, 9052965.00, 9053488.03, 9120952.26, 9257469.38],
    "serviced_drivers_st_devs": [49431.36, 0.00, 55767.95, 45337.86, 56319.32, 47954.98],
    "total_drivers": [17989125.00, 17989125.00, 17989125.00, 17989125.00, 17989125.00, 17989125.00],
    "TSTT": [73742243620582.69, 3768387034.92, 71511959858620.08, 95908304497250.80, 97083532790922.45, 72413452253724.78],
    "st_devs_t": [4424938041841.67, 0.00, 4138440941488.97, 8139250524057.70, 8029211804889.86, 4264374330448.81],
    "runtime": [8.74198, 8.00039, 8.92156, 77.21629, 75.36125, 8.74190],
    "st_devs": [0.05119, 0.04246, 1.77714, 1.26719, 1.07278, 0.04439]
}

cs_high = {
    "SO_TSTT": [120063705930.10, 120063705930.10, 120063705930.10, 120063705930.10, 120063705930.10, 120063705930.10],
    "serviced_drivers": [19211401.88, 35978250.00, 18108420.00, 18109217.62, 18252832.30, 18524152.50],
    "serviced_drivers_st_devs": [99861.12, 0.00, 101724.56, 102611.50, 81814.85, 121236.65],
    "total_drivers": [35978250.00, 35978250.00, 35978250.00, 35978250.00, 35978250.00, 35978250.00],
    "TSTT": [3315089723435326.00, 120063705930.10, 3281218392708630.00, 2151132335538244.25, 2207266394845636.50, 3383228770579677.00],
    "st_devs_t": [265401704931263.81, 0.00, 291441026234021.50, 127320005227606.92, 136955422692630.30, 339218195745509.69],
    "runtime": [8.75302, 8.00324, 8.76191, 78.84004, 77.52874, 8.75518],
    "st_devs": [0.10037, 0.08061, 0.14688, 1.18982, 0.70796, 0.05152]
}

def calculate_efficiency_ratios_with_std(cs_dict):
    ratios = [tstt / so_tstt for tstt, so_tstt in zip(cs_dict['TSTT'], cs_dict['SO_TSTT'])]
    std_devs = [std_tstt / so_tstt for std_tstt, so_tstt in zip(cs_dict['st_devs_t'], cs_dict['SO_TSTT'])]
    return ratios, std_devs

efficiency_cs_low, std_cs_low = calculate_efficiency_ratios_with_std(cs_low)
efficiency_cs_med, std_cs_med = calculate_efficiency_ratios_with_std(cs_med)
efficiency_cs_high, std_cs_high = calculate_efficiency_ratios_with_std(cs_high)

efficiency_cs_low = [value for i, value in enumerate(efficiency_cs_low) if i != 1][::-1]
efficiency_cs_med = [value for i, value in enumerate(efficiency_cs_med) if i != 1][::-1]
efficiency_cs_high = [value for i, value in enumerate(efficiency_cs_high) if i != 1][::-1]

std_cs_low = [value for i, value in enumerate(std_cs_low) if i != 1][::-1]
std_cs_med = [value for i, value in enumerate(std_cs_med) if i != 1][::-1]
std_cs_high = [value for i, value in enumerate(std_cs_high) if i != 1][::-1]

print(efficiency_cs_low)
print(efficiency_cs_med)
print(efficiency_cs_high)
print(std_cs_low)
print(std_cs_med)
print(std_cs_high)

colors = ['#6B9BD2', '#7DCD7D', '#E06D6D', '#B58BB6', '#F6A04A'][::-1]
bar_labels = ['TASR','SCALE', 'ASCALE', 'ALOOF', 'LLF'][::-1]

group_width = 5
group_spacing = 0.5
y_cs_low = np.arange(group_width) + 2 * (group_width + group_spacing)
y_cs_med = np.arange(group_width) + group_width + group_spacing
y_cs_high = np.arange(group_width)

fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.barh(y_cs_low, efficiency_cs_low, height=0.6, color=colors, xerr=std_cs_low, capsize=5)
bars_med = ax.barh(y_cs_med, efficiency_cs_med, height=0.6, color=colors, xerr=std_cs_med, capsize=5)
bars_high = ax.barh(y_cs_high, efficiency_cs_high, height=0.6, color=colors, xerr=std_cs_high, capsize=5)

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
    ['15700.160274629507', '964.9107819350554'],
    ['11267.705899660294', '690.7343348802849'],
    ['11270.048854701152', '648.8531643466987'],
    ['15199.864964652823', '975.1949276616973'],
    ['15762.383648531362', '898.9293563382344']
])

table2_data = format_table_data([
    ['19216.03369895419', '1131.6179285547669'],
    ['25762.62254680628', '2130.675997578448'],
    ['25450.757474885235', '2159.876479946145'],
    ['18976.80869718262', '1098.1995488095681'],
    ['19568.64911625198', '1174.226001957256'],
])

table3_data = format_table_data([
    ['28178.613548288788', '2825.3183850829946'],
    ['18384.12680790219', '1140.689616663711'],
    ['17916.591186937156', '1060.4370758114985'],
    ['27328.97812282194', '2427.386560962026'],
    ['27611.089444176752', '2210.507354202262'],
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
