import logging

from faster_whisper import WhisperModel # type: ignore

logger = logging.getLogger(__name__)


class Audio:
    def __init__(
        self,
        *,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8"
    ) -> None:
        self.model = WhisperModel(
            model_size_or_path=model_size,
            device=device,
            compute_type=compute_type
        )

    def transcribe_audio(self, audio_file: str) -> str | None:
        try:
            segments, _ = self.model.transcribe(audio_file)
            return "".join([segment.text for segment in segments])
        except Exception as e:
            logger.error("Error during transcription audio: %s", e)
            return None
