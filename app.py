import os

import tqdm
from aiogram import Dispatcher
from aiogram.utils import executor
from aiohttp import web

from db_api.dal.key_to_post_dal import PostIndexDAL
from db_api.model import PostIndex
from db_api.postgresql import db
import asyncio
from loader import dp
import handlers, utils, keyboards
import csv


async def on_startup(dp: Dispatcher):
    # await db.drop_all()
    await db.create_all()

    # app = web.Application()
    # loop = asyncio.get_event_loop()
    # port = int(os.environ.get("PORT", 17995))
    # loop.create_task(web._run_app(app, port=port))

async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await db.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
