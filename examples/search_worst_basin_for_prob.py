import json

from distributed.helpers.download import download_raw_by_filters
from gns import SemiRadixSystem
from sage.all import *


targets = []
for r in download_raw_by_filters('.dimension=3&.gns=0',1000000):
    if 'basinSizes' in r['properties']:
        basinSizes = json.loads(r['properties']['basinSizes'])

        if(len(basinSizes) > 1):
            print(basinSizes)
            targets.append({'basinSizes':basinSizes, 'percent':basinSizes[0] / sum(basinSizes),'r':r})
        #rs = SemiRadixSystem(r['base'], r['digits'])

m = max(targets, key=lambda x: x['percent'])

print('And the Oscar goes to:')
print(m['basinSizes'])
print(m['r']['id'])