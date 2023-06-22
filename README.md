HomoglyphsCJK
=====
An efficient and useful tool to fuzzy match Japanese, Korean, Simplified Chinese or Traditional Chinese words, using character visual similarity.

## Installation
```
pip install HomoglyphsCJK
```

## Usage
There are two functionalities of this package: use **homoglyph_pairwise_distance** to calculate homoglyph distance between two strings, or use **homoglyph_merge** to merge two dataframes based on keys using homoglyphic edit distance which uses substitution cost considering character visual similarity.
+ If you use **homoglyph_merge** or **homoglyph_pairwise_distance** on specific language, the dict will be downloaded automatically if not already exist, otherwise load from your current directory. So please make sure you run the script from a folder that has permission to write. The available languages are [zhs, zht, ko, ja] for simplified Chinese, traditional Chinese, Korean and Japanese respectively.
+ **homoglyph_merge** merges two dataframes. When you merge two dataframes, you can specify the parallel argument to use multiprocessing. If you don't specify the num_workers when using parallel, it will automatically use the number of all detected CPU cores.
+ Note that homoglyph_merge de-duplicates your passed in key columns and will in the end only return one unique value of the key specified. if you need to merge panel dataset to cross-sectional dataset for instance, you can de-duplicate the panel dataset key before you pass it in, then you will need to merge back your panel data using the matched key.

```python
from HomoglyphsCJK import  homoglyph_pairwise_distance,homoglyph_merge
import pandas as pd
df_1 = pd.DataFrame(list(['苏萃乡','办雄','虐格给','雪拉普岗']),columns=['query'])
df_2 = pd.DataFrame(list(['雪拉普岗日','小苏莽乡','协雄','唐格给','太阳村','月亮湾']),columns=['key'])

# merge two dataframes, note that the homoglyph dict of specified language will be downloaded automatically when first run.
## run in parallel with pool of 4, if num_workers is not specified, all available CPU cores are used.
dataframe_merged = homoglyph_merge('zhs',df_1,df_2,'query','key',homo_lambda=1, insertion=1, deletion=1,parallel=True,num_workers=4)

## not run in parallel
dataframe_merged = homoglyph_merge('zhs',df_1,df_2,'query','key',homo_lambda=1, insertion=1, deletion=1) 
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

+ **homoglyph_pairwise_distance** calculates homoglyphic edit distance between two strings. The default weight on substitution, insertion, deletion is 1.

```python
homoglyph_pairwise_distance('苏萃乡','小苏莽乡','zhs',homo_lambda=1, insertion=1, deletion=1)
# 1.88
```
## Contributing
We encourage you to contribute to HomoglyphsCJK!

## Questions
If you have any questions using this package, you can open an issue under our [GitHub repository](https://github.com/dell-research-harvard/HomoglyphsCJK/issues). We are maintaining and updating this package, so stay tuned!

## Citation
```bibtex
@misc{yang2023quantifying,
      title={Quantifying Character Similarity with Vision Transformers}, 
      author={Xinmei Yang and Abhishek Arora and Shao-Yu Jheng and Melissa Dell},
      year={2023},
      eprint={2305.14672},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
