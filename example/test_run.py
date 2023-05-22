# %%
import pandas as pd
from HomoglyphsCJK import homoglyph_distance,homoglyph_merge,download_dict

df_1 = pd.read_csv('./df_1_small.csv')
df_2 = pd.read_csv('./df_2_small.csv')

## Dataframe merge
dataframe_merged = homoglyph_merge('ko',df_1,df_2,'ocred_text','truth_text',homo_lambda=1, insertion=1, deletion=1,parallel=True,num_workers=4)

## Non-parallel
dataframe_merged = homoglyph_merge('ko',df_1,df_2,'ocred_text','truth_text',homo_lambda=1, insertion=1, deletion=1) 
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

download_dict('zhs')
homoglyph_distance('苏萃乡','小苏莽乡',homo_lambda=1, insertion=1, deletion=1)


# %%
