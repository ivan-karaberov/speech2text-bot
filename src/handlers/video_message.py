import os
import uuid

from aiogram import Bot
from aiogram.types import Message

from core import config
from services.video import Video


async def video_message(message: Message, bot: Bot) -> None:
    video = message.video or message.video_note

    if not video:
        await message.answer("Не удалось распознать видеофайл.")
        return None

    if video.file_size >= config.max_file_size_mb:
        await message.answer(f"Ошибка: размер файла превышает {config.max_file_size_mb / 1024 / 1024} Mb")
        return None
    
    file = await bot.get_file(video.file_id)
    file_path = config.data_dir / f"{message.from_user.id}_{uuid.uuid4()}.mp4"
    response = await message.answer("В обработке...")

    await bot.download(file, destination=file_path)

    transcribed_text = Video().transcribe_audio(file_path)
    os.remove(file_path)

    await message.answer(transcribed_text)
    await bot.delete_message(chat_id=message.chat.id, message_id=response.message_id)