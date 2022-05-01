import os
import pandas as pd
import numpy as np
from math import sqrt
from sklearn.metrics.pairwise import cosine_similarity

path = 'dataset/movielens'
ratings_df = pd.read_csv(os.path.join(path, 'ratings.csv'), encoding='utf-8')

# sparse_matrix 생성
sparse_matrix = ratings_df.groupby('movieId').apply(lambda x: pd.Series(x['rating'].values, index=x['userId'])).unstack()
sparse_matrix.index.name = 'movieId'

# 코사인 유사도 
def cossim_matrix(a, b):
    cossim_values = cosine_similarity(a.values, b.values)
    cossim_df = pd.DataFrame(data=cossim_values, columns = a.index.values, index=a.index)
    return cossim_df

item_sparse_matrix = sparse_matrix.fillna(0)
item_cossim_df = cossim_matrix(item_sparse_matrix, item_sparse_matrix)

userId_grouped = ratings_df.groupby('userId')
item_prediction_result_df = pd.DataFrame(index=list(userId_grouped.indices.keys()), columns=item_sparse_matrix.index)

for userId, group in userId_grouped:
    # user가 rating한 movieId * 전체 movieId
    user_sim = item_cossim_df.loc[group['movieId']]
    # user가 rating한 movieId * 1
    user_rating = group['rating']
    # 전체 movieId * 1
    sim_sum = user_sim.sum(axis=0)
    # userId의 전체 rating predictions (8938 * 1)
    pred_ratings = np.matmul(user_sim.T.to_numpy(), user_rating) / (sim_sum+1)
    item_prediction_result_df.loc[userId] = pred_ratings
    
item_prediction_result_df.to_csv('./dataset/item_prediction/item_pred.csv', index=False)