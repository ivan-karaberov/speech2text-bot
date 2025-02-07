import os
import uuid

from aiogram import Bot
from aiogram.types import Message

from core import config
from services.audio import Audio


async def audio_message(message: Message, bot: Bot) -> None:
    audio = message.voice or message.audio

    if not audio:
        await message.answer("Не удалось распознать аудиофайл.")
        return None
    
    if audio.file_size >= config.max_file_size_mb:
        await message.answer(f"Ошибка: размер файла превышает {config.max_file_size_mb / 1024 / 1024} Mb")
        return None

    file = await bot.get_file(audio.file_id)
    file_path = config.data_dir / f"{message.from_user.id}_{uuid.uuid4()}.ogg"
    response = await message.answer("В обработке...")

    await bot.download(file, destination=file_path)


    transcribed_text = Audio().transcribe_audio(file_path)
    os.remove(file_path)

    await message.answer(transcribed_text)
    await bot.delete_message(chat_id=message.chat.id, message_id=response.message_id)