import asyncio
import logging
import traceback

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

import handlers
from core import config

logger = logging.getLogger(__name__)

COMMAND_HANDLERS = {
    "start": handlers.start,
    "help": handlers.help
}


def register_message_handlers(dp: Dispatcher) -> None:
    for key, value in COMMAND_HANDLERS.items():
        dp.message.register(value, Command(key))

    dp.message.register(handlers.audio_message, F.audio | F.voice)
    dp.message.register(handlers.video_message, F.video | F.video_note)


async def main() -> None:
    bot = Bot(config.tg.token.get_secret_value())
    dp = Dispatcher()
    register_message_handlers(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        logger.warning(traceback.format_exc())
