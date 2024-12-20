#File: plot_trust_sc.py
#Purpose: Plots data on updated trust for each single-commodity setting as lollipop graphs.

import matplotlib.pyplot as plt
import numpy as np

categories = ['0.25', '0.5', '0.75']
subcategories = ['CC','TASR', 'SCALE', 'ASCALE', 'ALOOF', 'LLF']
colors = ['#35495E', '#6B9BD2', '#7DCD7D', '#E06D6D', '#B58BB6', '#F6A04A']
symbols = ['H','*', 'o', 's', '^', 'D'] 

#CC, TASR, SCALE, ASCALE, ALOOF, LLF
values_pig_low = [
    [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    [0.55, 0.55, 0.55, 0.55, 0.55, 0.55],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
]

values_pig_med = [
    [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    [0.55, 0.55, 0.55, 0.55, 0.55, 0.55],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
]

values_pig_high = [
    [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    [0.55, 0.55, 0.55, 0.55, 0.55, 0.55],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
]

values_cs_low = [
    [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    [0.55, 0.55, 0.55, 0.55, 0.55, 0.55],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
]

values_cs_med = [
    [0.27, 0.27, 0.29, 0.28, 0.3, 0.3],
    [0.52, 0.52, 0.54, 0.52, 0.55, 0.55],
    [0.77, 0.77, 0.78, 0.76, 0.79, 0.8]
]

values_cs_high = [
    [0.24, 0.3, 0.3, 0.3, 0.3, 0.3],
    [0.49, 0.5, 0.55, 0.55, 0.55, 0.55],
    [0.74, 0.74, 0.76, 0.75, 0.8, 0.8]
]

values_ana_low = [
    [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    [0.55, 0.55, 0.55, 0.55, 0.55, 0.55],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
]

values_ana_med = [
    [0.3, 0.3, 0.3, 0.29, 0.3, 0.3],
    [0.55, 0.55, 0.55, 0.54, 0.55, 0.55],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
]

values_ana_high = [
    [0.27, 0.27, 0.29, 0.29, 0.3, 0.3],
    [0.52, 0.52, 0.54, 0.52, 0.55, 0.55],
    [0.77, 0.77, 0.78, 0.76, 0.8, 0.8]
]

values_sf_low = [
    [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    [0.55, 0.55, 0.55, 0.55, 0.55, 0.55],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
]

values_sf_med = [
    [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    [0.55, 0.55, 0.55, 0.55, 0.55, 0.55],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
]

values_sf_high = [
    [0.3, 0.3, 0.3, 0.29, 0.3, 0.3],
    [0.55, 0.55, 0.55, 0.53, 0.55, 0.55],
    [0.8, 0.8, 0.8, 0.78, 0.8, 0.8]
]

values_aus_low = [
    [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    [0.55, 0.55, 0.55, 0.55, 0.55, 0.55],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
]

values_aus_med = [
    [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    [0.55, 0.55, 0.55, 0.55, 0.55, 0.55],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
]

values_aus_high = [
    [0.3, 0.29, 0.3, 0.29, 0.3, 0.3],
    [0.56, 0.54, 0.55, 0.54, 0.55, 0.55],
    [0.82, 0.79, 0.79, 0.78, 0.79, 0.8]
]


values = values_aus_high

category_positions = np.arange(len(categories))

subcategory_width = 0.1

plt.figure(figsize=(10, 6))
plt.ylim(0, 1)

for i, (subcategory, color, symbol) in enumerate(zip(subcategories, colors, symbols)):
    subcategory_positions = category_positions + (i - 2) * subcategory_width
    subcategory_values = [value[i] for value in values]
    markerline, stemlines, baseline = plt.stem(
        subcategory_positions, subcategory_values, basefmt=" ", linefmt="grey", markerfmt=symbol
    )
    markerline.set_color(color)
    stemlines.set_color(color)  
    stemlines.set_linewidth(4)  
    markerline.set_markerfacecolor(color)
    markerline.set_markeredgecolor(color)
    markerline.set_markersize(10)

plt.xticks(category_positions, categories)
plt.legend(subcategories, ncol=2, loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()