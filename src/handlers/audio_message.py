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
    
    file = await bot.get_file(audio.file_id)
    file_path = config.data_dir / f"{message.from_user.id}_{uuid.uuid4()}.ogg"

    await bot.download(file, destination=file_path)

    response = await message.answer("В обработке...")

    transcribed_text = Audio().transcribe_audio(file_path)
    os.remove(file_path)

    await message.answer(transcribed_text)
    await bot.delete_message(chat_id=message.chat.id, message_id=response.message_id)