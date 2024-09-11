import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import json
import sys
import pprint
from gns import SemiRadixSystem, Timer, SymmetricDigits

df = pd.read_csv('systems3.csv')
df = df[df['gns'] == 0]



prob_is_better = 0
prob_success_all = 0
klen_is_better = 0
klen_success_all = 0

for index, row in df.iterrows():
    print(row["digits"], row["base"])
    rs = SemiRadixSystem(json.loads(row['base']),json.loads(row['digits']))

    t = Timer()
    prob_result = rs.probability_gns_test(100000)
    prob_time = t.get_time()

    t.start_timer()
    n_length_search_count = 100000
    digit_num = len(rs.get_digits())
    find_period_round = math.floor(math.log((digit_num - 1) * n_length_search_count / digit_num + 1) / math.log(digit_num))
    klen_result = []
    for i in range(1, find_period_round):
        klen_result = rs.find_n_length_cycle(i)
        # print("nlength",res)
        if len(klen_result) > 0:
            break
    klen_time = t.get_time()
    baseline_time = row['optimize:vol:decide']

    if prob_result is not None:
        prob_success_all += 1
        if prob_time < baseline_time:
            prob_is_better += 1

    if len(klen_result) > 0:
        klen_success_all += 1
        if klen_time < baseline_time:
            klen_is_better += 1


print(f'prob_success_all={prob_success_all}')
print(f'prob_is_better={prob_is_better}')
print(f'klen_success_all={klen_success_all}')
print(f'klen_is_better={klen_is_better}')