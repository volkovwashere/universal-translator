import whisper
import json
from typing import Dict


class SpeechToText:
    def __init__(self):
        self.__model = whisper.load_model(name="tiny")

    def transcribe_audio(self, audio_file: str, language: str = None) -> str:
        assert type(audio_file) == str, "Only string type is supported ..."

        print(f"Transcribing the following language: {language}")
        res = self.__model.transcribe(audio=audio_file, **{"language": language if language else "en"})
        return res["text"]

    @staticmethod
    def save_text(output_file: str, data: Dict[str, str]) -> None:
        assert output_file.endswith(".json"), "Only json extension is supported ..."

        with open(output_file, "w") as f:
            json.dump(data, f)
