import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms



def init_df():
    df = pd.read_csv('systems.csv')
    df = df[~df['optimizer:volume:twoTransform2:IsGNSTime'].isnull()]
    df = df[df['dimension'] < 8]
    for c in df.columns:
        if not c.startswith('period'):
            print(c)

    return df

def calculate_closest_witness():
    '''
    >>> calculate_closest_witness()
    '''
    df = pd.read_csv('systems.csv')
    df = df[~df['period1sourceDistances'].isna()]

    least_close_by_constant_term = {dim: -1 for dim in range(2,50)}
    for row in df.to_dict(orient="records"):
        closest = None
        # print('---')
        # print('ID:', row['id'])
        # print(row['base'])
        constant_term_abs = len(json.loads(row['digits']))
        for i in range(1,100):
            val = row[f'period{i}sourceDistances']
            if not isinstance(val, str) and np.isnan(val):
                break
            else:
                parsed = json.loads(val)
                first_non_zero_index = next((i for i, x in enumerate(parsed) if x), None)
                #print(parsed, first_non_zero_index)
                if closest is None or first_non_zero_index < closest:
                    closest = first_non_zero_index
        #print(closest)
        if closest > least_close_by_constant_term[constant_term_abs]:
            least_close_by_constant_term[constant_term_abs] = closest

    print(least_close_by_constant_term)

def scatter_plot():
    '''
    >>> scatter_plot()
    '''
    df = init_df()
    plt.figure()
    offset = lambda p: transforms.ScaledTranslation(p / 72., 0, plt.gcf().dpi_scale_trans)
    trans = plt.gca().transData

    plt.scatter(df['dimension'], df['optimizer:volume:IsGNSTime'], c='blue', s=25, transform=trans + offset(-5))
    plt.scatter(df['dimension'], df['optimizer:volume:twoTransform:IsGNSTime'], c='red', s=25)
    plt.scatter(df['dimension'], df['optimizer:volume:twoTransform2:IsGNSTime'], c='green', s=25,
                transform=trans + offset(5))
    plt.savefig('scatter.png')

def smart_plot():
    '''
    >>> smart_plot()
    '''
    df = pd.read_csv('smart.csv')
    plt.figure()
    ax = plt.gca()
    ax.scatter(df['volume'], df['Simple Decide'], c='blue')
    ax.scatter(df['volume'], df['Smart Decide'], c='red')
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.savefig('numsys_smart_decide.png')


def bydimension():
    '''
    >>> bydimension()
    '''
    df = init_df()
    df['twoTransform'] = df['optimizer:volume:twoTransform:IsGNSTime'] / df['optimizer:volume:IsGNSTime']
    df['twoTransform2'] = df['optimizer:volume:twoTransform2:IsGNSTime'] / df['optimizer:volume:IsGNSTime']
    df['complex'] = df['optimizer:complex:IsGNSTime'] / df['optimizer:volume:IsGNSTime']
    df['twoTransformc'] = df['optimizer:complex:twoTransform:IsGNSTime'] / df['optimizer:volume:IsGNSTime']
    df['twoTransformc2'] = df['optimizer:complex:twoTransform2:IsGNSTime'] / df['optimizer:volume:IsGNSTime']

    df = df.groupby('dimension', as_index=False).mean()
    plt.figure()
    plt.plot(df['dimension'], df['twoTransform'], label='twoTransform', c = 'blue')
    plt.plot(df['dimension'], df['twoTransform2'], label='twoTransform2', c = 'red')
    plt.plot(df['dimension'], df['complex'], label='complex', c = 'green')
    plt.plot(df['dimension'], df['twoTransformc'], label='twoTransformc', c = 'orange')
    plt.plot(df['dimension'], df['twoTransformc2'], label='twoTransformc2', c = 'black')

    plt.legend(loc="upper left")
    plt.savefig('numsys_optimization_speedup_per_dimension.png')

def bestones(targets):
    '''
    >>> bestones(['complex','complex_plus_complexphi','complex_plus_phi','vol_plus_volphi','vol_plus_phi'])
    '''
    df = pd.read_csv('systems3.csv')
    df = df[df['gns'] == 1]
    df['optimize:complex'] = (df['optimize:complex:decide'] < df['optimize:vol:decide']).astype('int')
    df['optimize:complex_plus_complexphi'] = (df['optimize:complex_plus_complexphi:decide'] < df['optimize:vol:decide']).astype('int')
    df['optimize:complex_plus_phi'] = (df['optimize:complex_plus_phi:decide'] < df['optimize:vol:decide']).astype('int')
    df['optimize:vol_plus_phi'] = (df['optimize:vol_plus_phi:decide'] < df['optimize:vol:decide']).astype('int')
    df['optimize:vol_plus_volphi'] = (df['optimize:vol_plus_volphi:decide'] < df['optimize:vol:decide']).astype('int')


    result_df = df.groupby('dimension', as_index=False).sum()
    result_df['casecount'] = df.groupby('dimension', as_index=False).count()['id']
    for target in targets:
        result_df[f'optimize:{target}:percent'] = result_df[f'optimize:{target}'] / result_df['casecount']

    result_df.index = result_df['dimension']
    target_fields = [f'optimize:{target}:percent' for target in targets]

    plt.figure()
    ax = plt.gca()
    result_df[target_fields].plot.bar(rot=0, ax = ax)
    if len(targets) == 1:
        ax.get_legend().remove()
    plt.savefig('numsys_optimize_bar.png')

def optimize_draw(target):
    '''
    >>> optimize_draw('vol_plus_phi')
    '''
    df = pd.read_csv('systems3.csv')
    #df = df[df['gns'] == 1]
    #df = df[df['dimension'] == 2]
    df = df[df['optimize:vol:decide'] > 1]
    plt.figure()
    ax = plt.gca()
    print((df['optimize:vol:decide'] / df[f'optimize:{target}:decide']).min())
    print((df['optimize:vol:decide'] / df[f'optimize:{target}:decide']).max())
    print((df['optimize:vol:decide'] / df[f'optimize:{target}:decide']).mean())
    print((df['optimize:vol:decide'] / df[f'optimize:{target}:decide']).describe())
    #ax.scatter(df['volume'], df['optimize:vol:decide'] / df['optimize:complex:decide'], c='blue', alpha=0.5)
    ax.scatter(df['volume'], df['optimize:vol:decide'], c='blue', alpha=0.5)
    ax.scatter(df['volume'], df[f'optimize:{target}:decide'], c='red', alpha=0.5)
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.savefig(f'numsys_{target}_optimize_ratio.png')

def bydimension2():
    '''
    >>> bydimension2()
    '''
    df = pd.read_csv('optimized.csv')
    df = df.groupby('dimension', as_index=False).mean()
    plt.figure()
    plt.plot(df['dimension'], df['optimize:vol:decide'], label='vol', c = 'black')
    plt.plot(df['dimension'], df['optimize:vol_plus_phi:decide'], label='vol_plus_phi', c = 'blue')
    plt.plot(df['dimension'], df['optimize:vol_plus_volphi:decide'], label='vol_plus_volphi', c = 'red')
    plt.plot(df['dimension'], df['optimize:complex:decide'], label='complex', c = 'green')
    plt.plot(df['dimension'], df['optimize:complex_plus_phi:decide'], label='complex_plus_phi', c = 'orange')
    plt.plot(df['dimension'], df['optimize:complex_plus_complexphi:decide'], label='complex_plus_complexphi', c = 'purple')
    plt.yscale('log')
    plt.legend(loc="upper left")
    plt.savefig('numsys_optimization_speedup_per_dimension2.png')
