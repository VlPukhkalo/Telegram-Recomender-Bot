import pandas as pd
import numpy as np

import scipy.sparse as sp
import implicit

emdeddings = np.load('/Users/veron/Downloads/embeddings20.npy')

df = pd.read_csv('/Users/veron/PycharmProjects/lenta/data/filtered_post_without_embeddings_with_labels.csv', index_col=0)

from dateutil.relativedelta import relativedelta
import datetime

date_after_month = datetime.datetime.today() -  relativedelta(months=1)
df['posted'] = pd.to_datetime(df['posted'])

df = df[df['posted'] >= date_after_month]

df.to_csv('last_month_posts.csv')
emdeddings20_last_month = emdeddings[list(df.index)]
model = implicit.nearest_neighbours.CosineRecommender(K=50)
emdeddings_csr = sp.csr_matrix(emdeddings20_last_month).tocsr()
model.fit(emdeddings_csr.T)
model.save('model_last.npz')

with open('embeddings20_last_month.npy', 'wb') as f:
    np.save(f, np.array(emdeddings20_last_month))

df_last_month = df.reset_index(drop=True)
df_last_month.to_csv('last_month_posts.csv')

labels_df = []

for i in sort_labels:
    loc_df = df_last_month[df_last_month['label'] == i].sort_values(by='er', ascending=False)
    labels_df.append(loc_df)

for i in range(len(sort_labels)):
    labels_df[i] = labels_df[i][labels_df[i]['er'] < 1]

for i in range(40):
    labels_df[i]['position'] =  (np.array(range(labels_df[i].shape[0])) * 30) + i

df_recommend = pd.concat(labels_df).sort_values(by='position')
df_recommend['emdeddings'] = df_recommend.index
df_recommend = df_recommend.drop('position', axis=1)

df_recommend.to_csv('cold_start_dataframe_last_month.csv')
df_recommend = pd.read_csv('cold_start_dataframe_last_month.csv')