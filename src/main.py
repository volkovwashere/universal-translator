from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from src.internal.ml_services import SpeechToText
import uvicorn
import aiofiles
import os
import requests
from src.constants import API_KEY, DEEPL_URL
from gtts import gTTS
from pathlib import Path

transcriber = SpeechToText()
app = FastAPI()


def _remove_audio_files() -> None:
    # get audio files dynamically
    audio_files = Path(__file__).parent.glob("*.wav")
    for file in audio_files:
        os.remove(file)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/translate/")
async def create_upload_file(
        file: UploadFile,
        source_language: str,
        target_language: str,
        background_tasks: BackgroundTasks,
) -> FileResponse:

    # part one - save the file
    async with aiofiles.open(file.filename, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    # part two - transcription
    transcription = transcriber.transcribe_audio(audio_file=file.filename, language=source_language)
    print(transcription)

    # # part three - translation
    payload = {
        "text": transcription,
        "target_lang": target_language,
    }
    headers = {
        "Authorization": f"DeepL-Auth-Key {API_KEY}"
    }
    res = requests.post(
        url=DEEPL_URL,
        data=payload,
        headers=headers,
    )
    translation = res.json()["translations"][0]["text"]

    # step 4 - text2speech
    tts = gTTS(text=translation, lang=target_language)
    tts.save(file_name := "translated_text.wav")

    headers = {'Content-Disposition': f'attachment; filename={file_name}'}
    background_tasks.add_task(_remove_audio_files)
    return FileResponse(file_name, headers=headers, media_type="audio/wav")
    # return {"transcription": transcription} | res.json()["translations"][0]

# Todo readbytes instead of upload file and stuff
# @app.post("/translate/")
# async def translate():
#

if __name__ == '__main__':
    uvicorn.run(app=app)