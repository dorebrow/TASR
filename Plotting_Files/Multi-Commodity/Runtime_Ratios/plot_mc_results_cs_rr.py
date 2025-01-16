#File: plot_mc_results_cs_rr_alt.py
#Purpose: Plots multi-commodity average runtime ratio (algorithmic runtime over CC runtime) 
#and standard deviations for the Chicago Sketch network under low, medium, and high demand levels.
#Includes table.

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import math

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

def calculate_runtime_ratios_with_std(cs_dict):
    denom = cs_dict['runtime'][1]
    denom_std_dev = cs_dict['st_devs'][1]
    
    if denom == 0:
        raise ValueError("Denominator for runtime ratios cannot be zero.")
    
    ratios = [runtime / denom for runtime in cs_dict['runtime']]
    
    std_devs_propagated = [
        ratio * math.sqrt((std_dev / runtime) ** 2 + (denom_std_dev / denom) ** 2)
        if runtime != 0 else 0
        for runtime, std_dev, ratio in zip(cs_dict['runtime'], cs_dict['st_devs'], ratios)
    ]
    
    return ratios, std_devs_propagated

runtime_cs_low, std_cs_low = calculate_runtime_ratios_with_std(cs_low)
runtime_cs_med, std_cs_med = calculate_runtime_ratios_with_std(cs_med)
runtime_cs_high, std_cs_high = calculate_runtime_ratios_with_std(cs_high)

runtime_cs_low = [value for i, value in enumerate(runtime_cs_low) if i != 1]
runtime_cs_med = [value for i, value in enumerate(runtime_cs_med) if i != 1]
runtime_cs_high = [value for i, value in enumerate(runtime_cs_high) if i != 1]

std_cs_low = [value for i, value in enumerate(std_cs_low) if i != 1]
std_cs_med = [value for i, value in enumerate(std_cs_med) if i != 1]
std_cs_high = [value for i, value in enumerate(std_cs_high) if i != 1]

group_width = 5
group_spacing = 1
x_cs_low = np.arange(group_width)
x_cs_med = np.arange(group_width) + group_width + group_spacing
x_cs_high = np.arange(group_width) + 2 * (group_width + group_spacing)

colors = ['#1F4E79', '#2B7A2F', '#D04A4A', '#8C4B8C', '#D67C29']
bar_labels = ['TASR','SCALE', 'ASCALE', 'ALOOF', 'LLF']

fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.bar(
    x_cs_low, runtime_cs_low, width=0.8, facecolor="none", 
    edgecolor=colors, linewidth=4.5, yerr=std_cs_low, capsize=5
)
bars_med = ax.bar(
    x_cs_med, runtime_cs_med, width=0.8, facecolor="none", 
    edgecolor=colors, linewidth=4.5, yerr=std_cs_med, capsize=5
)
bars_high = ax.bar(
    x_cs_high, runtime_cs_high, width=0.8, facecolor="none", 
    edgecolor=colors, linewidth=4.5, yerr=std_cs_high, capsize=5
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
    ', '.join([f"{value:.2f}" for value in runtime_cs_low]),
    ', '.join([f"{value:.2f}" for value in runtime_cs_med]),
    ', '.join([f"{value:.2f}" for value in runtime_cs_high])
]

sd_row = [
    ', '.join([f"{value:.2f}" for value in std_cs_low]),
    ', '.join([f"{value:.2f}" for value in std_cs_med]),
    ', '.join([f"{value:.2f}" for value in std_cs_high])
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
