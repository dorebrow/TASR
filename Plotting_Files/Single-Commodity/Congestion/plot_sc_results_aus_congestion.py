# File: plot_sc_results_aus_congestion_alt.py
# Purpose: Plots single-commodity average total travel time (congestion) and standard deviations 
# for the Austin network under low, medium, and high demand levels. 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.stretch'] = 'condensed'

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

congestion_aus_low = [value for i, value in enumerate(congestion_aus_low)][::-1]
congestion_aus_med = [value for i, value in enumerate(congestion_aus_med)][::-1]
congestion_aus_high = [value for i, value in enumerate(congestion_aus_high)][::-1]

std_aus_low = [value for i, value in enumerate(std_aus_low)][::-1]
std_aus_med = [value for i, value in enumerate(std_aus_med)][::-1]
std_aus_high = [value for i, value in enumerate(std_aus_high)][::-1]


colors = ['#1F4E79','#333333', '#2B7A2F', '#D04A4A', '#8C4B8C', '#D67C29'][::-1]
bar_labels = ['TASR', 'CC', 'SCALE', 'ASCALE', 'ALOOF', 'LLF'][::-1]

group_width = 6
group_spacing = 0.5
y_aus_low = np.arange(group_width) + 2 * (group_width + group_spacing)
y_aus_med = np.arange(group_width) + group_width + group_spacing
y_aus_high = np.arange(group_width)


fig, ax = plt.subplots(figsize=(6, 6))

bars_low = ax.barh(y_aus_low, congestion_aus_low, height=0.6, color=colors, xerr=std_aus_low, capsize=5)
bars_med = ax.barh(y_aus_med, congestion_aus_med, height=0.6, color=colors, xerr=std_aus_med, capsize=5)
bars_high = ax.barh(y_aus_high, congestion_aus_high, height=0.6, color=colors, xerr=std_aus_high, capsize=5)

ax.set_yticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_yticklabels(['High', 'Med', 'Low'], fontsize=34, rotation=90, fontweight='bold')
ax.tick_params(axis='x', labelsize=34, bottom=True, top=True)
ax.tick_params(axis='y', which='both', pad=10)
ax.set_xlim(0.0, 1300000)

def format_func(value, tick_number):
    return f'{value * 1e-5:.1f}e5'

ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color) for color in colors]

combined_handles = legend_handles 
combined_labels = bar_labels

fig.legend(handles=combined_handles, labels=combined_labels, loc='upper right', bbox_to_anchor=(0.85, 0.98), ncol=2, frameon=True, fontsize=38)

plt.grid(axis='x', linestyle='--', alpha=0.5)

ax.axhline(y=5.7, color='gray', linestyle='--', linewidth=1.5)
ax.axhline(y=12.2, color='gray', linestyle='--', linewidth=1.5)

fig.tight_layout()
plt.draw()
plt.tight_layout()
plt.show()
