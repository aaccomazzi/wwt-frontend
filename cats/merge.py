from glob import glob
import pandas as pd
import numpy as np
import json

def ten(x):
    denom = 1.
    result = 0
    neg = -1 if x[0].startswith('-') else 1
    if len(x) == 1:
        return float(x[0])
    if len(x) == 2:
        return float(x[0]) + float(x[1]) / 60 * neg
    return float(x[0]) + float(x[1]) / 60 * neg + float(x[2]) / 3600 * neg

files = glob('Npix*tsv')

#some tiles are empty
dne = set('Npix%i.tsv' % i for i in
          [1037, 1073, 1973, 2661, 2922, 2933, 2997, 3005, 38, 389])
files = [f for f in files if f not in dne]

tables = [pd.read_csv(f, delimiter='\t')
          for f in files]

table = pd.concat(tables, ignore_index=True)

ra = table['RA'].str.split(' ')
dec = table['DEC'].str.split(' ')

ra = np.array([ten(r) for r in ra])
dec = np.array([ten(d) for d in dec])

table['RA'] = ra
table['DEC'] = dec
table = table.dropna(subset=['RA', 'DEC'])
table = table[['MAIN_ID', 'RA', 'DEC']]


data = [dict(name=row['MAIN_ID'], ra=row['RA'] * 15, dec=row['DEC'])
        for i, row in table.iterrows()]

with open('merged.json', 'w') as outfile:
    json.dump(data, outfile, indent=1)
