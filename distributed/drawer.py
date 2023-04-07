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

def bestones():
    '''
    >>> bestones()
    '''
    df = init_df()
    df['complex'] = (df['optimizer:complex:IsGNSTime'] < df['optimizer:volume:IsGNSTime']).astype('int')
    df['twoTransform'] = (df['optimizer:volume:twoTransform:IsGNSTime'] < df['optimizer:volume:IsGNSTime']).astype('int')
    df['twoTransform2'] = (df['optimizer:volume:twoTransform2:IsGNSTime'] < df['optimizer:volume:IsGNSTime']).astype('int')
    df['twoTransformc'] = (df['optimizer:complex:twoTransform:IsGNSTime'] < df['optimizer:volume:IsGNSTime']).astype('int')
    df['twoTransformc2'] = (df['optimizer:complex:twoTransform2:IsGNSTime'] < df['optimizer:volume:IsGNSTime']).astype('int')

    result_df = df.groupby('dimension', as_index=False).sum()
    result_df['casecount'] = df.groupby('dimension', as_index=False).count()['id']

    print(result_df)
