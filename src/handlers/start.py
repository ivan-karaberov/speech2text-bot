from aiogram.types import Message

from utils.template import render_template


async def start(message: Message) -> None:
    await message.answer(render_template("start.j2"))