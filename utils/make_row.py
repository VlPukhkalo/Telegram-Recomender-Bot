import numpy as np
from scipy import sparse as sp

from data.config import posts


def make_coo_row(data):
    if data != []:
        values = [i['rating'] for i in data]
        idx = [i['id'] for i in data]

        return sp.coo_matrix(
            (values, ([0] * len(idx), idx)), shape=(1, posts.shape[0]),
        )
    else:
        return sp.coo_matrix(
            (posts.shape[0])
        )