from aiogram.types import Message

from utils.template import render_template


async def help(message: Message) -> None:
    await message.answer(render_template("help.j2"))