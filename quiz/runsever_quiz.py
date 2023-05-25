# noinspection SpellCheckingInspection
"""
Первое задание для специалиста уровня Junior, компания - Bewise.ai

Композиция задачи:

[INFO]  В сервисе должен быть реализован POST REST метод,
        принимающий на вход запросы с содержимым вида {"questions_num": integer}
        Пример тела запроса (JSON format):
        {
            "questions_num": 6
        }

[INFO]  После получения запроса сервис, в свою очередь, запрашивает с публичного API
        (англоязычные вопросы для викторин) https://jservice.io/api/random?count={questions_num}
        указанное в полученном запросе количество вопросов

[INFO]  Полученные ответы должны сохраняться в базе данных из п. 1, причем сохранена должна быть как минимум
        следующая информация:
        1. ID вопроса
        2. Текст вопроса
        3. Текст ответа
        4. Дата создания вопроса
        В случае, если в БД имеется такой же вопрос, к публичному API с викторинами
        должны выполняться дополнительные запросы до тех пор пока не будет получен уникальный вопрос для викторины

[INFO]  Ответом на запрос из п.2.a должен быть предыдущей сохранённый вопрос для викторины.
        В случае его отсутствия - пустой объект.
        Пример вывода:
        [
            {
                "id": 200627,
                "question_text": "These mountains in the northeast are the site of many resort facilities",
                "answer_text": "the Poconos",
                "create_data": "2022-12-30T21:46:01.928Z"
            }
        ]
"""
import os
import requests

from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from datetime import datetime
from typing import List
from dotenv import load_dotenv

from quiz_models import Base, Question, QuizRequest


load_dotenv()

app = FastAPI()

SQLALCHEMY_DATABASE_URL = f'postgresql://{os.getenv("USER")}:{os.getenv("PASSWD")}@{os.getenv("IP")}:5432/{os.getenv("NAME")}'
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_timeout=10)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def _save_question_to_db(db: SessionLocal, question: dict) -> None:
    """Функция для сохранения вопросов в БД"""
    db_question = Question(
        question_text=question['question'], answer_question=question['answer'], create_data=datetime.now()
    )

    db.add(db_question)
    db.commit()


def _get_unique_question_from_api(question_num: int) -> dict:
    """Функция для проверки уникального вопроса из API"""
    url = f'https://jservice.io/api/random?count={question_num}'
    response = requests.get(url=url)
    questions = response.json()

    for question in questions:
        if not SessionLocal().query(Question).filter_by(question_text=question['question']).first():
            return question

    return _get_unique_question_from_api(question_num)


@app.post("/quiz")
def get_and_save_post_request(quiz_request: QuizRequest) -> List[dict]:
    """POST метод для получение и сохранение вопросов в БД"""
    response_questions = []

    with SessionLocal() as db:
        for i in range(quiz_request.questions_num):
            question = _get_unique_question_from_api(1)
            _save_question_to_db(db, question)
            response_questions.append(
                {
                    "id": question['id'],
                    "question_text": question['question'],
                    "answer_text": question['answer'],
                    "create_data": question['created_at']
                }
            )

    return response_questions
