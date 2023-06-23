HomoglyphsCJK
=====
An efficient and useful tool to fuzzy match Japanese, Korean, Simplified Chinese or Traditional Chinese words, using character visual similarity.

## Installation
```
pip install HomoglyphsCJK
```

## Usage
The package provides two functionalities:
+ The **homoglyph_pairwise_distance** calculates the homoglyph distance between two strings. It determines the similarity between strings by considering characters that have similar visual representations. This function can be used to measure the distance between pairs of strings.
+ The **homoglyph_merge** merges two dataframes based on keys using homoglyphic edit distance. It considers the visual similarity of characters and performs a merge operation on the specified columns. When merging dataframes, you can specify the columns to merge on. Additionally, the merging process can be parallelized using multiprocessing by setting the parallel argument. If the number of workers is not specified, the package will automatically utilize all available CPU cores.
+ It's important to note that when using **homoglyph_merge** or **homoglyph_pairwise_distance** for a specific language, the package will download the required dictionary if it doesn't already exist. Otherwise, it will load the dictionary from the current directory. Ensure that you run the script from a folder with write permissions. The available languages for homoglyph operations are simplified Chinese (zhs), traditional Chinese (zht), Korean (ko), and Japanese (ja).
+ When using **homoglyph_merge**, it de-duplicates the query and key columns provided for efficiency. The function returns only the unique matches. Matching these unique matches back to the dataset is a standard operation in data wrangling and can be done using pandas or other environments. The package focuses on the merge operation and leaves the post-merge matching to the user.

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
