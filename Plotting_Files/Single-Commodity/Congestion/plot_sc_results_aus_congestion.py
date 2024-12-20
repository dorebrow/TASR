#File: plot_sc_results_aus_congestion.py
#Purpose: Plots single-commodity average total travel time (congestion) and standard deviations 
#for the Austin network under low, medium, and high demand levels.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

aus_low = {
    #TASR, CC, SCALE, ASCALE, ALOOF, LLF
    "SO_TSTT": [38021.89, 38021.89, 38021.89, 38021.89, 38021.89, 38021.89],
    "flow_assigned": [24999.75, 24999.75, 24999.75, 24999.75, 24999.75, 24999.75],
    "selfish_flow": [24999.75, 24999.75, 24999.75, 24999.75, 24999.75, 24999.75],
    "TSTT": [38021.89, 38021.89, 38021.89, 38021.89, 38021.89, 119068.54],
    "st_devs_t": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    "runtime": [17.46001, 17.35566, 16.88342, 16.86667, 17.59253,  20.09164],
    "st_devs": [0.28568, 0.29585, 0.26978, 7.47353, 0.26525, 4.08561]
}

aus_med = {
    "SO_TSTT": [119409.35, 119409.35, 119409.35, 119409.35, 119409.35, 119409.35],
    "flow_assigned": [74999.25, 74999.25, 74999.25, 74999.25, 74999.25, 74999.25],
    "selfish_flow": [74999.25, 74999.25, 74999.25, 74999.25, 74999.25, 74999.25],
    "TSTT": [119409.35, 119409.35, 119409.35, 120788.30, 119409.35, 373939.82],
    "st_devs_t": [0.00, 0.00, 0.00, 420.10, 0.00, 0.00],
    "runtime": [17.65701, 17.19939, 17.01263, 17.24920, 16.86035, 16.87601],
    "st_devs": [0.39296, 0.25531, 0.28932, 0.32411, 0.26844, 0.27720]
}

aus_high = {
    "SO_TSTT": [365877.25, 365877.25, 365877.25, 365877.25, 365877.25, 365877.25],
    "flow_assigned": [149998.50, 149998.50, 149998.50, 149998.50, 149998.50, 149998.50],
    "selfish_flow": [149998.50, 149998.50, 149998.50, 149998.50, 149998.50, 149998.50],
    "TSTT": [365877.25, 365877.25, 371305.82, 369930.72, 393007.21, 1256181.19],
    "st_devs_t": [0.00, 0.00, 11136.52, 11629.40, 12715.16, 0.00],
    "runtime": [17.94908, 17.93724, 17.20328, 17.28063, 18.28812, 17.34867],
    "st_devs": [0.43738, 0.43165, 0.27002, 0.26509, 9.93242, 0.28261]
}

def construct_congestion_lists(aus_dict):
    tstt_values = aus_dict['TSTT']
    std_tstt_values = aus_dict['st_devs_t']
    return tstt_values, std_tstt_values

congestion_aus_low, std_aus_low = construct_congestion_lists(aus_low)
congestion_aus_med, std_aus_med = construct_congestion_lists(aus_med)
congestion_aus_high, std_aus_high = construct_congestion_lists(aus_high)

congestion_aus_low = [value for i, value in enumerate(congestion_aus_low) if i != 1]
congestion_aus_med = [value for i, value in enumerate(congestion_aus_med) if i != 1]
congestion_aus_high = [value for i, value in enumerate(congestion_aus_high) if i != 1]

std_aus_low = [value for i, value in enumerate(std_aus_low) if i != 1]
std_aus_med = [value for i, value in enumerate(std_aus_med) if i != 1]
std_aus_high = [value for i, value in enumerate(std_aus_high) if i != 1]

group_width = 5
group_spacing = 1
x_aus_low = np.arange(group_width)
x_aus_med = np.arange(group_width) + group_width + group_spacing
x_aus_high = np.arange(group_width) + 2 * (group_width + group_spacing)

colors = ['#6B9BD2', '#7DCD7D', '#E06D6D', '#B58BB6', '#F6A04A']
bar_labels = ['TASR','SCALE', 'ASCALE', 'ALOOF', 'LLF']

fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.bar(x_aus_low, congestion_aus_low, width=0.8, color=colors, yerr=std_aus_low, capsize=5)
bars_med = ax.bar(x_aus_med, congestion_aus_med, width=0.8, color=colors, yerr=std_aus_med, capsize=5)
bars_high = ax.bar(x_aus_high, congestion_aus_high, width=0.8, color=colors, yerr=std_aus_high, capsize=5)

ax.set_xticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_xticklabels(['Low', 'Med', 'High'], fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.set_ylim(0.0, 2400000)

fixed_offset = 30000

for i in range(len(bars_low)):
    bar_height = bars_low[i].get_height()
    ax.text(
        bars_low[i].get_x() + bars_low[i].get_width() / 2, 
        bar_height + fixed_offset, 
        f'{congestion_aus_low[i]:.2f} ± {std_aus_low[i]:.2f}', 
        rotation=90, fontsize=20, ha='right', va='bottom', fontweight='bold'
    )

for i in range(len(bars_med)):
    bar_height = bars_med[i].get_height()
    ax.text(
        bars_med[i].get_x() + bars_med[i].get_width() / 2, 
        bar_height + fixed_offset, 
        f'{congestion_aus_med[i]:.2f} ± {std_aus_med[i]:.2f}', 
        rotation=90, fontsize=20, ha='right', va='bottom', fontweight='bold'
    )

for i in range(len(bars_high)):
    bar_height = bars_high[i].get_height()
    ax.text(
        bars_high[i].get_x() + bars_high[i].get_width() / 2, 
        bar_height + fixed_offset, 
        f'{congestion_aus_high[i]:.2f} ± {std_aus_high[i]:.2f}', 
        rotation=90, fontsize=20, ha='right', va='bottom', fontweight='bold'
    )

legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color) for color in colors]

combined_handles = legend_handles
combined_labels = bar_labels

ax.legend(
    combined_handles,
    combined_labels,
    loc='upper center',
    ncol=5,
    fontsize=30
)

plt.tight_layout()
plt.show()
