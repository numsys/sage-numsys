import json

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

df = pd.read_csv('systems.csv')
df = df[df['gns'] == 0]
c = 0
scatter_points_x = []
scatter_points_y = []

def find_index_of_first_non_zero(in_list):
    for i, item in enumerate(in_list):
        if item != 0:
            return i

    return None

for index, row in df.iterrows():
    c += 1
    if c > 100000:
        break

    distances = []
    for p in range(1,100):
        field_name = f'period{p}sourceDistances'
        if type(row[field_name]) == str:
            source_distances = json.loads(row[field_name])
            closest_basin_point = find_index_of_first_non_zero(source_distances)
            distances.append(closest_basin_point)

    if len(distances) > 0:
        closest_witness = min(distances)
        digitnum = len(json.loads(row['digits']))
        scatter_points_x.append(digitnum)
        scatter_points_y.append(closest_witness)

        if digitnum < closest_witness:
            print(digitnum, closest_witness)
            for item in row.iteritems():
                print(item)

print(len(scatter_points_x))
plt.scatter(scatter_points_x, scatter_points_y)
plt.savefig('scatter.png')