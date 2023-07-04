from environs import Env
import redis
import implicit
import pandas as pd
import numpy as np


env = Env()
env.read_env()

DATABASE_URL = env.str('DATABASE_URL')
BOT_TOKEN = env.str('BOT_TOKEN')
WEBAPP_URL = env.str('WEBAPP_URL')
REDIS_URL = env.str('REDIS_URL')

# emdeddings = np.load('data/embeddings20_last_month.npy')
posts = pd.read_csv('data/last_month_posts.csv')
cold_start = pd.read_csv('data/cold_start_dataframe_last_month.csv')

model = implicit.nearest_neighbours.CosineRecommender(K=50)
model = model.load('data/model_last.npz')

