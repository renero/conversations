import itertools as it
filename='test.dat'

with open(filename,'r') as f:
    for key,group in it.groupby(f,lambda line: line.startswith('=======')):
        if not key:
            group = list(group)
            print(group)