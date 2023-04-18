import pandas as pd

from distributed.helpers.download import download_raw_by_filters

records = []
for r in download_raw_by_filters('',10000000):
    row = {'id':r['id'],'base':r['base'],'digits':r['digits'], **(r['properties'])}

    records.append(row)

    if len(records) % 1000 == 0:
        df = pd.DataFrame(records)
        df.to_csv('systems.csv')

df = pd.DataFrame(records)
df.to_csv('systems.csv')