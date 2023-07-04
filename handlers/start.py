import asyncio
import datetime
import random

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text
from sqlalchemy import desc

from data.config import WEBAPP_URL, cold_start, posts
from db_api.dal.key_to_post_dal import PostIndexDAL
from db_api.dal.user_item_dal import UserItemDAL
from db_api.dal.user_dal import UserDAL
from db_api.model import UsersItem
from keyboards.next_kbd import next_kb
from loader import dp, bot
from utils.make_row import make_coo_row
from utils.recommend import recalculate


@dp.message_handler(CommandStart(), chat_type=[types.ChatType.PRIVATE])
async def bot_start(message: types.Message):
    await message.answer('Привет. \nЭто персонализированная бесконечная лента. \n Нажимай кнопку "Листать" и получай свежие посты на базе твоих предпочтений.',
                         reply_markup=next_kb)

    await asyncio.sleep(0.5)

    await UserDAL.add(user_id=message.chat.id, time=datetime.datetime.now(),
                      recommend=str(cold_start['emdeddings'][101:200].to_list()))

    await message.answer(f'<a href="https://t.me/{cold_start.loc[100]["username"]}/{cold_start.loc[100]["msg_id"]}">⚡</a>')
    await UserItemDAL.adds(
        UsersItem(
            user_id=message.chat.id,
            item_id=int(cold_start['emdeddings'][100]),
            rating=0,
            time=datetime.datetime.now()
        )
    )

@dp.message_handler(Text(equals='❤️'), chat_type=[types.ChatType.PRIVATE])
async def bot_like(message: types.Message):
    user_id = message.chat.id
    user = await UserDAL.get(user_id=user_id)
    recommed_list = eval(user.recommend)

    if not recommed_list:
        _offset = 100*(user.offset + 1)
        recommed_list.extend(cold_start['emdeddings'][_offset+1:_offset+100].to_list())
        await UserDAL.update(where={'user_id': user_id}, recommend=str(recommed_list), offset=_offset+1)

        await message.answer(
            f'<a href="https://t.me/{cold_start.loc[_offset]["username"]}/{cold_start.loc[_offset]["msg_id"]}">⚡</a>')
        await UserItemDAL.adds(
            UsersItem(
                user_id=message.chat.id,
                item_id=int(cold_start['emdeddings'][_offset]),
                rating=0,
                time=datetime.datetime.now()
            )
        )
        return

    post_last = await UserItemDAL.get(user_id=user_id, orderby=(UsersItem.time), desc=True)
    post = posts.loc[recommed_list[0]]

    await message.answer(
        f'<a href="https://t.me/{post["username"]}/{post["msg_id"]}">⚡</a>')

    await UserItemDAL.adds(
        UsersItem(
            user_id=user_id,
            item_id=post.name,
            rating=0,
            time=datetime.datetime.now()
        )
    )
    await UserDAL.update(where={'user_id': user_id}, recommend=str(recommed_list[1:]))

    await UserItemDAL.update(
        where={'user_id': user_id, 'item_id': post_last.item_id},
        rating=1
    )
    await recalculate(user_id=user_id)


@dp.message_handler(chat_type=[types.ChatType.PRIVATE])
async def bot_next(message: types.Message):

    user_id = message.chat.id
    user = await UserDAL.get(user_id=user_id)
    recommed_list = eval(user.recommend)

    if not recommed_list:
        _offset = 100*(user.offset + 1)
        recommed_list.extend(cold_start['emdeddings'][_offset+1:_offset+100].to_list())
        await UserDAL.update(where={'user_id': user_id}, recommend=str(recommed_list), offset=_offset+1)

        await message.answer(
            f'<a href="https://t.me/{cold_start.loc[_offset]["username"]}/{cold_start.loc[_offset]["msg_id"]}">⚡</a>')
        await UserItemDAL.adds(
            UsersItem(
                user_id=message.chat.id,
                item_id=int(cold_start['emdeddings'][_offset]),
                rating=0,
                time=datetime.datetime.now()
            )
        )
        return

    post_last = await UserItemDAL.get(user_id=user_id, orderby=(UsersItem.time), desc=True)
    post = posts.loc[recommed_list[0]]

    await message.answer(
        f'<a href="https://t.me/{post["username"]}/{post["msg_id"]}">⚡</a>')

    await UserItemDAL.adds(
        UsersItem(
            user_id=user_id,
            item_id=post.name,
            rating=0,
            time=datetime.datetime.now()
        )
    )
    await UserDAL.update(where={'user_id': user_id}, recommend=str(recommed_list[1:]))

    if post_last.time + datetime.timedelta(minutes=5) >= datetime.datetime.now() and post_last.time + datetime.timedelta(seconds=30) <= datetime.datetime.now():
        await UserItemDAL.update(
            where={'user_id':user_id, 'item_id': post_last.item_id},
            rating=1
        )
        await recalculate(user_id=user_id)