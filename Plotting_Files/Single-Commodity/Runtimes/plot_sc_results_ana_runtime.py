#File: plot_sc_results_ana_runtime.py
#Purpose: Plots single-commodity average runtime and standard deviations for 
#the Anaheim network under low, medium, and high demand levels.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import math

ana_low = {
    "SO_TSTT": [3104.07, 3104.07, 3104.07, 3104.07, 3104.07, 3104.07],
    "flow_assigned": [1350.00, 1350.00, 1350.00, 1350.00, 1350.00, 1350.00],
    "selfish_flow": [1350.00, 1350.00, 1350.00, 1350.00, 1350.00, 1350.00],
    "TSTT": [3104.07, 3104.07, 3104.07, 3104.07, 3104.07, 3104.07],
    "st_devs_t": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    "runtime": [0.49882, 0.58963, 0.52024, 0.53772, 0.51444, 0.51340],
    "st_devs": [0.03448, 0.14414, 0.03639, 0.05354, 0.03916, 0.02621]
}

ana_med = {
    "SO_TSTT": [9693.82, 9693.82, 9693.82, 9693.82, 9693.82, 9693.82],
    "flow_assigned": [4050.00, 4050.00, 4050.00, 4050.00, 4050.00, 4050.00],
    "selfish_flow": [4050.00, 4050.00, 4050.00, 4050.00, 4050.00, 4050.00],
    "TSTT": [9693.82, 9693.82, 9693.82, 10069.20, 9693.82, 9693.82],
    "st_devs_t": [0.0, 0.0, 0.0, 124.15, 0.0, 0.0],
    "runtime": [0.51303, 0.50823, 0.53056, 0.88218, 0.49687, 0.51121],
    "st_devs": [0.03874, 0.05147, 0.04313, 0.07175, 0.01982, 0.02263]
}

ana_high = {
    "SO_TSTT": [25577.72, 25577.72, 25577.72, 25577.72, 25577.72, 25577.72],
    "flow_assigned": [8100.00, 8100.00, 8100.00, 8100.00, 8100.00, 8100.00],
    "selfish_flow": [8100.00, 8100.00, 8100.00, 8100.00, 8100.00, 8100.00],
    "TSTT": [25559.33, 25577.72, 27082.24, 26028.03, 30426.63, 30533.22], 
    "st_devs_t": [23.65, 0.00, 1007.94, 475.97,  690.38, 649.31],
    "runtime": [0.88233, 0.97247, 0.91193, 0.92403, 0.65550, 0.98349],
    "st_devs": [0.07670, 0.18958, 0.08441, 0.09904, 0.17489, 0.17388]
}

def calculate_average_and_std(ana_dict):
    runtimes = ana_dict['runtime']
    std_devs = ana_dict['st_devs']
    
    if any(runtime == 0 for runtime in runtimes):
        raise ValueError("Runtime values cannot be zero.")
    
    std_devs_propagated = [
        std_dev / math.sqrt(len(runtimes)) if len(runtimes) > 0 else 0
        for std_dev in std_devs
    ]
    
    return runtimes, std_devs_propagated

runtime_ana_low, std_ana_low = calculate_average_and_std(ana_low)
runtime_ana_med, std_ana_med = calculate_average_and_std(ana_med)
runtime_ana_high, std_ana_high = calculate_average_and_std(ana_high)

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

bars_low = ax.bar(x_ana_low, runtime_ana_low, width=0.8, color=colors, yerr=std_ana_low, capsize=5)
bars_med = ax.bar(x_ana_med, runtime_ana_med, width=0.8, color=colors, yerr=std_ana_med, capsize=5)
bars_high = ax.bar(x_ana_high, runtime_ana_high, width=0.8, color=colors, yerr=std_ana_high, capsize=5)

ax.set_xticks([(group_width / 2), 
               (group_width + group_spacing + group_width / 2), 
               (2 * (group_width + group_spacing) + group_width / 2)])
ax.set_xticklabels(['Low', 'Med', 'High'], fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.set_ylim(0, 30)

legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=color) for color in colors]

combined_handles = legend_handles
combined_labels = bar_labels

fixed_offset = 0.5

for i in range(len(bars_low)):
    bar_height = bars_low[i].get_height()
    ax.text(
        bars_low[i].get_x() + bars_low[i].get_width() / 2, 
        bar_height + fixed_offset, 
        f'{runtime_ana_low[i]:.2f} ± {std_ana_low[i]:.2f}', 
        rotation=90, fontsize=20, ha='right', va='bottom', fontweight='bold'
    )

for i in range(len(bars_med)):
    bar_height = bars_med[i].get_height()
    ax.text(
        bars_med[i].get_x() + bars_med[i].get_width() / 2, 
        bar_height + fixed_offset, 
        f'{runtime_ana_med[i]:.2f} ± {std_ana_med[i]:.2f}', 
        rotation=90, fontsize=20, ha='right', va='bottom', fontweight='bold'
    )

for i in range(len(bars_high)):
    bar_height = bars_high[i].get_height()
    ax.text(
        bars_high[i].get_x() + bars_high[i].get_width() / 2, 
        bar_height + fixed_offset, 
        f'{runtime_ana_high[i]:.2f} ± {std_ana_high[i]:.2f}', 
        rotation=90, fontsize=20, ha='right', va='bottom', fontweight='bold'
    )

ax.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

ax.legend(
    combined_handles,
    combined_labels,
    loc='upper center',
    ncol=5,
    fontsize=24
)

plt.tight_layout()
plt.show()
