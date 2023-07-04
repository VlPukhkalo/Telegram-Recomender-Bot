from data.config import posts
from db_api.dal.user_item_dal import UserItemDAL
from db_api.model import UsersItem


async def _filter_recommend(user_id, user_recommend, recommed_list):
    posts_last = (await UserItemDAL.get(many=True, user_id=user_id, orderby=(UsersItem.time), desc=True))[:2]
    posts_last = [posts.loc[posts_last[0].item_id], posts.loc[posts_last[1].item_id]]

    _count = 0
    for post in recommed_list:

        cur_post = posts.loc[post]
        labels_last = [i['label'] for i in posts_last]

        if posts_last[-1]['channel_id'] != cur_post['channel_id'] and cur_post['label'] not in labels_last and cur_post.name not in user_recommend:
            user_recommend.insert(0, cur_post.name)
            posts_last.append(cur_post)
            posts_last = posts_last[1:]

            _count += 1

        if _count >= 15:
            break
    return user_recommend