import pandas as pd
import numpy as np

df = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]],columns=['a','b','c'], index = [11,12,13])

print(df)

sum1 = df.loc[13].sum()
print(sum1)

# for row in df.index.values:
#     df['total'] = df.loc[row].sum()

df['total'] = df.sum(axis=1)
print(df)

test_sum = df['a'].sum(axis=0)
print(test_sum)
