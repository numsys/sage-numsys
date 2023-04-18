import pandas as pd


def create_merged_txt(from_degree = 0, to_degree = 7, from_constant = 0, to_constant = 5):
    '''
    >>> create_merged_txt(0,6,0,5)
    '''
    with open(f'../polynoms/c{from_constant}-{to_constant}d{from_degree}-{to_degree}.txt' ,'w') as target_f:
        for c in range(2,11):
            if not (from_constant <= c and c <= to_constant):
                continue


            with open(f'../polynoms/c{c}.txt','r') as f:
                for line in f.readlines():
                    degree = len(line.split()) - 1
                    if from_degree <= degree and degree <= to_degree:
                        print(line)
                        target_f.write(line)


def collect_counts():
    '''
    >>> collect_counts()
    '''
    df_data = []
    for c in range(2, 11):
        result = {d: 0 for d in range(2, 61)}
        with open(f'../polynoms/c{c}.txt', 'r') as f:
            for line in f.readlines():
                degree = len(line.split()) - 1
                result[degree] += 1

        for d in result:
            if result[d] > 0:
                df_data.append({'constant':c, 'degree': d, 'count':result[d]})

    df = pd.DataFrame.from_records(df_data)
    df.to_csv('polynom_counts.csv')


def count_stat():
    '''
    >>> count_stat()
    '''
    df = pd.read_csv('polynom_counts.csv')

    df_data = []
    for c in range(2,11):
        if c <= 6:
            maxd = 8
        elif c == 7:
            maxd = 7
        else:
            maxd = 6

        for d in range(2,maxd + 1):
            df_data.append({'constant':c, 'degree':d, 'cumcount': df[(df['constant'] <= c) & (df['degree'] <= d)]['count'].sum()})

    df2 = pd.DataFrame.from_records(df_data)
    df2.to_csv('polynom_cum_counts.csv')
