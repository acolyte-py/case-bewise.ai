# noinspection SpellCheckingInspection
"""
Второе задание для специалиста уровня Junior, компания - Bewise.ai

Композиция задачи:

[INFO] Post запрос для регистрации пользователей:
       На вход принимает "name" пользователя. Пользователь создается в базе данных с уникальным токеном
       Возвращает запрос -> "id" и "token" пользователя
       
[INFO] Post запрос для загрузки аудиофайла:
       На вход принимает "id" "token" пользователя и "file" в формате .wav
       Возвращает url для скачивания аудиофайла, за ранее который был преобразован в формат .mp3

[INFO] Get запрос для возможности скачать аудиофайл:
       На вход получается ссылка в виде - http://0.0.0.0:8000/record?user=1&num=a1a1a1a1a1a1a1a
"""
import os

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from dotenv import load_dotenv
from uuid import uuid4, UUID
from contextlib import contextmanager, closing
from pathlib import Path

from audio_models import Users, Audio, Base, UsersRequests, AudioRequests


load_dotenv()

app = FastAPI()

SQLALCHEMY_DATABASE_URL = f'postgresql://{os.getenv("USER")}:{os.getenv("PASSWD")}@{os.getenv("IP")}:5432/{os.getenv("NAME")}'
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_timeout=10)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


@contextmanager
def _get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        with closing(db):
            pass


@app.post("/users")
def create_user(name: UsersRequests) -> dict:
    """Функция для регистрации пользователя"""
    with _get_db() as db:
        user = Users(name=name.name)
        db.add(user)
        db.flush()

        _dict = {
            "id": user.id,
            "token": user.token
        }
        return _dict


@app.post("/audio/{user_id}")
async def upload_audio(user_id: int, file: UploadFile = File(...)) -> AudioRequests:
    """Функция для загрузки музыки"""
    with _get_db() as db:
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail='[E] User not found!')

        if not file.filename.lower().endswith(('.wav', '.WAV')):
            raise HTTPException(status_code=400, detail='[W] Only ".wav" format allowed!')

        filename = f'{user_id}_{str(uuid4())}.mp3'
        audio_path = Path(filename)
        contents = await file.read()
        with open(audio_path, 'wb') as f:
            f.write(contents)

        audio = Audio(user=user, filename=str(audio_path))
        db.add(audio)
        db.flush()

        _response = AudioRequests(
            url=f'http://0.0.0.0:8000/record?user={user_id}&num={audio.url}',
            user_id=user_id,
            audio_id=audio.url
        )
        return _response


@app.get("/record", responses={404: {"description": "File not found"}})
def download_audio(user: int, num: UUID) -> FileResponse:
    """Функция для доступа к музыки"""
    with _get_db() as db:
        audio = db.query(Audio).filter(Audio.user_id == user, Audio.url == str(num)).first()
        if not audio:
            raise HTTPException(status_code=404, detail='[E] Audio not found!')

        return FileResponse(audio.filename, media_type='audio/mpeg')
