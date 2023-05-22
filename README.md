HomoglyphsCJK
=====

An efficient and useful tool to fuzzy match Japanese, Korean, Simplified Chinese or Traditional Chinese words, particular useful for OCRed text record linkage.

## Installation
```
pip install HomoglyphsCJK
```

## Usage
There are two functionalities of this package: calculate homoglyph distance between two strings, or merge two dataframes based on keys using homoglyph distance.

When you firstly use this on one language, the homoglyph dict will be downloaded automatically in the current directory you run your script. So please make sure you run the script from a folder that has permission to write.

+ Merge two dataframes. When you merge two dataframes, you can specify the parallel argument to run multiprocessing. Mac users probably want to use Python version == 3.7 for multiprocessing.

```python
    from HomoglyphsCJK import homoglyph_distance,homoglyph_merge,download_dict
    import pandas as pd
    df_1 = pd.DataFrame(list(['苏萃乡','办雄','虐格给','雪拉普岗']),columns=['ocred_text'])
    df_2 = pd.DataFrame(list(['雪拉普岗日','小苏莽乡','协雄','唐格给']),columns=['truth_text'])

    # merge two dataframes, note that the homoglyph dict of specified language will be downloaded automatically when first run.
    ## run in parallel with pool of 4, if num_workers is not specified, all available CPU cores are used.
    dataframe_merged = homoglyph_merge('zhs',df_1,df_2,'ocred_text','truth_text',homo_lambda=1, insertion=1, deletion=1,parallel=True,num_workers=4)
    
    ## not run in parallel
    dataframe_merged = homoglyph_merge('zhs',df_1,df_2,'ocred_text','truth_text',homo_lambda=1, insertion=1, deletion=1) 
    '''
    lang: choose from zhs, zht, ja, ko
    dataframe 1: the first dataframe
    dataframe 2: the second dataframe
    key from dataframe 1
    key from dataframe 2
    weight on substitution homoglyph distance, default is 1
    weight on insertion cost, default is 1
    weight on deletion cost, default is 1
    '''
```

| ocred_text | homo_matched_truth_text | homo_dist |
| ---------- | ----------------------- | --------- |
| 苏萃乡      | 小苏莽乡                 | 1.88      | 
| 办雄        | 协雄                    | 0.15      |
| 虐格给      | 唐格给                   | 0.87      |
| 雪拉普岗    | 雪拉普岗日                | 1.0       | 

+ Homoglyph distance between two strings. The default weight on substitution, insertion, deletion is 1.

```python
    download_dict('zhs')
    homoglyph_distance('苏萃乡','小苏莽乡',homo_lambda=1, insertion=1, deletion=1)
    # 1.88
```
