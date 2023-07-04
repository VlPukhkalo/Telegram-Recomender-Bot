import numpy as np

from data.config import model
from db_api.dal.user_dal import UserDAL
from db_api.dal.user_item_dal import UserItemDAL
from utils.business_rules import _filter_recommend
from utils.make_row import make_coo_row


async def recalculate(user_id: int):
    user = await UserDAL.get(user_id=user_id)
    user_recommend = eval(user.recommend)
    history = await UserItemDAL.get(many=True, user_id=user_id)

    history = [{'rating': action.rating, 'id': action.item_id} for action in history]
    history_row = make_coo_row(history).tocsr()
    history_row.dtype = np.float64

    recommed_list = list(model.recommend(user_id, history_row, N=50, filter_already_liked_items=True, recalculate_user=True)[0])
    recommed_list = await _filter_recommend(user_id, user_recommend, recommed_list)
    await UserDAL.update(where={'user_id': user_id}, recommend=str(recommed_list))


