import os
import logging

from moviepy import VideoFileClip # type: ignore

from services.audio import Audio

logger = logging.getLogger(__name__)


class Video:
    def __init__(self) -> None:
        self.audio = Audio()

    def transcribe_audio(self, video_file: str) -> str | None:
        if audio_file := self.extract_audio(video_file):
            transcribed_text = self.audio.transcribe_audio(audio_file)
            os.remove(audio_file)
            return transcribed_text

        return None
    
    def extract_audio(self, video_file: str) -> str | None:
        audio_file = None

        try:
            with VideoFileClip(video_file) as video_clip:
                audio_clip = video_clip.audio
                audio_file = f"{str(video_file)[:-4]}.mp3"
                audio_clip.write_audiofile(audio_file)
                return audio_file
        except Exception as e:
            logger.error("Failed extract audio from video > %s", e)
            return None