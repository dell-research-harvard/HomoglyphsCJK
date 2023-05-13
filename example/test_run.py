


# %%
import pandas as pd

# df_1 = pd.read_csv('df_1.csv')
# df_2 = pd.read_csv('df_2.csv')

# df_1 = df_1.head(100)
# df_2 = df_2.head(100)

# df_1.to_csv('df_1_small.csv')

# df_2.to_csv('df_2_small.csv')

# %%

import homo_test

df_1 = pd.read_csv('./df_1_small.csv')
df_2 = pd.read_csv('./df_2_small.csv')

## Dataframe merge
dataframe_merged = homo_test.homoglyph_merge('ja',df_1,df_2,'result','truth',parallel=True,num_workers=4)
'''
Parameters:
lang
dataframe 1
dataframe 2
key on dataframe 1
key on dataframe 2
'''
## Also need to pass in dataframe later on
dataframe_merged.to_csv('./merged.csv')


# %%
cluster_dict = homo_test.download_dict('ja')
print(homo_test.homoglyph_distance('我','我是'))

