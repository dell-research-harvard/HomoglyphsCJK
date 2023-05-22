# %%
import os
import pandas as pd
from tqdm import tqdm
import pickle
from functools import partial
import numpy as np
import gdown
# import multiprocess
from multiprocess import cpu_count
from multiprocess import Pool
# from concurrent.futures import ProcessPoolExecutor as PoolExecutor
# from .proxy import entry_point
import numpy as np
# from numba import njit, types, prange,jit
# from numba.typed import Dict, List

def download_dict(lang):
    '''
    This function is like if it does not exist, then download, otherwise just load from local machine
    '''
    if lang not in ['ko','ja','zhs','zht']:
        raise Exception("language must be specified as ko, ja, zhs or zht")
    elif lang=='ko':
        ## Download the dicts to the current folder
        if not os.path.exists('./ko/char_char_dist_dict_800_korean.pickle'):
            print(f'downloading {lang} homoglyph dict...')
            url = 'https://drive.google.com/drive/folders/19ElYJaFPUS3ekTUMa7xU8zYDCEFagWQ9?usp=share_link'
            gdown.download_folder(url,quiet=True,use_cookies=False)
            print('downloaded!')
        cluster_dict_path = './ko/char_char_dist_dict_800_korean.pickle'
    elif lang == 'ja':
        if not os.path.exists('./ja/char_char_dist_dict_800_japanese.pickle'):
            print(f'downloading {lang} homoglyph dict...')
            url = 'https://drive.google.com/drive/folders/1nm0wWEMInlslyvafPEA3oxgVtlTsPPeR?usp=sharing'
            gdown.download_folder(url,quiet=True,use_cookies=False)
            print('downloaded!')
        cluster_dict_path = './ja/char_char_dist_dict_800_japanese.pickle'
    elif lang == "zhs":
        if not os.path.exists('./zhs/char_char_dist_dict_800_s_chinese_expanded_easy.pickle'):
            print(f'downloading {lang} homoglyph dict...')
            url = 'https://drive.google.com/drive/folders/1Mgcj4bq83IaYr00VdqHf-_LZ2zbfw2-8?usp=sharing'
            gdown.download_folder(url,quiet=True,use_cookies=False)
            print('downloaded!')
        cluster_dict_path = './zhs/char_char_dist_dict_800_s_chinese_expanded_easy.pickle'

    elif lang == 'zht':
        if not os.path.exists('./zht/char_char_dist_dict_800_t_chinese_expanded_easy.pickle'):
            print(f'downloading {lang} homoglyph dict...')
            url = 'https://drive.google.com/drive/folders/1Cqaswlny2yoUT8V4CwhsYYGeenoggoaP?usp=sharing'
            gdown.download_folder(url,quiet=True,use_cookies=False)
            print('downloaded!')
        cluster_dict_path = './zht/char_char_dist_dict_800_t_chinese_expanded_easy.pickle'

    global cluster_dict
    with open(cluster_dict_path,'rb') as f:
        cluster_dict = pickle.load(f) 
    # return cluster_dict

def homoglyph_distance(str1,str2, homo_lambda=1,insertion=1,deletion=1):
    m = len(str1)
    n = len(str2)
    #dp = np.zeros([m+1,n+1]) # it is m rows, n columns
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)] # This list is quicker than the above numpy array.
    for i in range(m+1):
        for j in range(n+1):
            if i==0 and j==0:
                dp[i][j]=0
            elif i==0:
                dp[i][j]=dp[i][j-1]+1
            elif j==0:
                dp[i][j]=dp[i-1][j]+1         
            elif str1[i-1]==str2[j-1]:
                dp[i][j]=dp[i-1][j-1]
            else:
                global cluster_dict
                if str1[i-1] in cluster_dict:
                    if str2[j-1] in cluster_dict[str1[i-1]]:
                        dist=homo_lambda*(1-cluster_dict[str1[i-1]][str2[j-1]]) # This is gamma actually, the substitution cost is the homoglyphic distance
                    else:
                        dist=1 
                else:
                    dist=1

                dp[i][j] =  min(dp[i][j-1]+insertion,	 # Insert
                                dp[i-1][j]+deletion,	 # Remove
                                dp[i-1][j-1]+dist) 

    return dp[m][n]

def map_2_word_dist(x,list2,dist_list):
    return [str(list2[x]),float(dist_list[x])]


def list_fd(word,list2, homo_lambda, insertion, deletion):
    # try not to pass many things in pool, since it will copy everything, make things as lean as possible!
    dist_list = np.ones(len(list2))
    smallest_dist = 1000
    for id, word2 in tqdm(enumerate(list2)): # The returned value will keep the order as original
        if abs(len(str(word2))-len(str(word))) > smallest_dist:
            dist = 1000
        dist = homoglyph_distance(str(word),str(word2),homo_lambda, insertion,deletion)
        #print(dist)
        dist_list[id] = dist
        if dist < smallest_dist:
            smallest_dist = dist
    min_dist = float(np.min(dist_list)) # Change the distance to Python native float type
    min_dist_word = str(list2[np.argmin(dist_list)]) # Which word in the ground truth dict get matched to
    return [min_dist, min_dist_word]

def same_matched(a,b):
    for ele in a:
        if ele == b: # If any of the ele in a equals b, return 1, after the iter, if nothing returns, just return 0
            return 1
    return 0

def homoglyph_merge(lang, df_1,df_2,key_1,key_2,homo_lambda=1, insertion=1, deletion=1, parallel=False,num_workers=None):
    #cluster_dict = download_dict('ko')
    # Initialize the list 2
    list2 = df_2[key_2].tolist()
    # Initialize the list 1
    result_list = df_1[key_1].tolist() # The result_list is list 1
    assert len(list2) == len(result_list)
    list1 = [] # initialize the list1
    for res, truth in zip(result_list,list2):
        res_dict = {}
        res_dict[key_1] = res
        res_dict[key_2] = truth
        list1.append(res_dict)
    # Save output and initialize the accuracy results storage
    ## add the df_matched
    df_matched = pd.DataFrame(list(zip(list2,result_list)), columns=[key_2,key_1])

    global cluster_dict
    download_dict(lang)

    if parallel==False:
        word_dist_min_list = map(partial(list_fd,list2=list2,homo_lambda=homo_lambda, insertion=insertion, deletion=deletion),result_list)#added the functions
    else:
        if num_workers==None:num_workers=cpu_count()#if the num_workers is specified, just use 
        with Pool(num_workers) as p:
             word_dist_min_list = p.map(partial(list_fd,list2=list2,homo_lambda=homo_lambda, insertion=insertion, deletion=deletion),result_list)
        # Use concurrent future
        # with PoolExecutor(num_workers) as executor:
        #     word_dist_min_list = executor.map(partial(list_fd,list2=list2),result_list)

    matched_list = []
    distance_list = []
    for id, (list1_ele, word_dist_min) in enumerate(zip(list1,word_dist_min_list)):
        list1[id]["matched_word"] = word_dist_min[1]
        matched_list.append(word_dist_min[1])
        list1[id]["matched_word_dist"] = round(word_dist_min[0],2)
        distance_list.append(round(word_dist_min[0],2))

    df_matched = pd.DataFrame(list(zip(result_list, \
        matched_list, distance_list, \
            )),columns=[key_1, \
                f'homo_matched_{key_2}','homo_dist', \
                                        ])
    return df_matched
    
# @njit
# def wagner_fischer_with_cluster_dict_fast(str1, str2, cluster_dict_keys, cluster_dict_values):
#     m = len(str1)
#     n = len(str2)
#     ###If the strings are the same, return zero
#     if str1 == str2:
#         return 0
#     ###Ensure that the inner loop is over the shorter string
#     if m < n:
#         str1, str2, m, n = str2, str1, n, m

#     dp = np.zeros((m + 1, n + 1), dtype=np.float32)

#     for i in range(m + 1):
#         dp[i, 0] = i
#     for j in range(n + 1):
#         dp[0, j] = j

#     for i in range(1, m + 1):
#         for j in range(1, n + 1):
#             if str1[i - 1] == str2[j - 1]:
#                 dp[i, j] = dp[i - 1, j - 1]
#             else:
#                 dist = 1.0
#                 if str1[i - 1] in cluster_dict_keys:
#                     idx = cluster_dict_keys.index(str1[i - 1])
#                     if str2[j - 1] in cluster_dict_values[idx]:
#                         dist = 1 - cluster_dict_values[idx][str2[j - 1]]
#                         print(min(dp[i - 1, j] + 1, dp[i, j - 1] + 1, dp[i - 1, j - 1] + dist))
#                 dp[i, j] = min(dp[i - 1, j] + 1, dp[i, j - 1] + 1, dp[i - 1, j - 1] + dist)

#     return dp[m, n]

# def convert_cluster_dict(cluster_dict):
#     cluster_dict_keys = List([key for key in cluster_dict.keys()])
#     cluster_dict_values = List([Dict.empty(key_type=types.unicode_type, value_type=types.float64) for _ in cluster_dict.values()])
#     for i, sub_dict in enumerate(cluster_dict.values()):
#         for k, v in sub_dict.items():
#             cluster_dict_values[i][k] = v
#     return cluster_dict_keys, cluster_dict_values


# def homoglyph_merge_quick(lang, df_1,df_2,key_1,key_2,parallel=False,num_workers=None):
#     # Implement the numba
#     pass

# %%
