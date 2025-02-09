import os
import uuid
import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor

from aiogram import Bot
from aiogram.types import Message

from core import config
from services.video import Video

logger = logging.getLogger(__name__)

def transcribe_video(file_path: str) -> str:
    return Video().transcribe_audio(file_path)


async def video_message(message: Message, bot: Bot) -> None:
    video = message.video or message.video_note

    if not video:
        await message.answer("Не удалось распознать видеофайл.")
        return None

    if video.file_size >= config.max_file_size_mb * 1024 * 1024:
        await message.answer(f"Ошибка: размер файла превышает {config.max_file_size_mb} Mb")
        return None
    
    file_path = config.data_dir / f"{message.from_user.id}_{uuid.uuid4()}.mp4"
    try:
        file = await bot.get_file(video.file_id)
        response = await message.answer("В обработке...")

        await bot.download(file, destination=file_path, timeout=60)

        with ProcessPoolExecutor(max_workers=5) as executor:
            future = executor.submit(transcribe_video, file_path)
            transcribed_text = await asyncio.wrap_future(future)

        await message.answer(transcribed_text)
    except Exception as e:
        logger.error("Failed transcribed video message > %s", e)
        await message.answer("Произошла ошибка при обработке видеосообщения.")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

        await bot.delete_message(chat_id=message.chat.id, message_id=response.message_id)