# Тестовое задание на позицию Junior в компанию Bewise.ai 📄
Ссылка на вакансию - [link](https://tomsk.hh.ru/vacancy/80456354?hhtmFrom=chat)

В этом тест-кейсе я старался сделать как можно больше, ну и конечно, как понимаю. Не скажу, что работа
сделана идеально. Много минусов и пробелов, на которые стоит обратить внимание и исправить.
Я очень старался, так как хочу попасть к Вам на работу. FastAPI до этого знал лишь по названию.
Большое спасибо за возможность и интересное задание 😊

# Getting Started ✅
Для разработки использовалась ОС Manjaro. Приведенный ниже cheat sheet сделан для Manjaro. Шаги легко повторяются на любом Linux дистрибутиве.
Если Вы работаете на Window там будет слегка по-другому, но смысл тот же и можно так же повторить шаги работая по аналогии.

### Installing 🔨
Для работы использовал python/pip следующей версии:

![1](https://github.com/acolyte-py/test-case-bewise.ai/assets/75732226/420329e8-f693-49e8-9fd9-ba5d5dd83930)

Прежде чем начинать работу необходимо убедится:
  * установлен python/pip;
  * установлен Docker/docker-compose;
  * установлен PostgreSQL (если Вы хотите использовать локальную БД, а не в контейнере).

Здесь не будет инструкции по установки софта в списке выше, поскольку это очень простые действия:
```
sudo pacman -S <something>
```
Далее небольшие правки и все. Легко можно найти в интернете. Если все жё будет проблемы, пишите помогу :)

Следующий шаг будет клонирование репозитория с проектом и установка зависимостей проекта. Делается это следующим образом:

Клонирование репозитория:
```
git clone https://github.com/acolyte-py/case-bewise.ai.git
```
Устновка зависимостей проекта:
```
cd case-bewise.ai
```
```
pip3.10 install -r requirements.txt
```

### Starting DB using docker-compose 💿
В проекте есть готовый docker-compose.yml файл, который включает в себя образ PostgreSQL. Так же там инициалируется бд и пользователь.
Для корректной работы нам нужно узнать адрес контейнера. Запустим контейнер и узнаем его адрес следующими командами:
```
docker-compose up -d
```
```
sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <id или name контейнера>
```
Пример вывода команды:

![2](https://github.com/acolyte-py/case-bewise.ai/assets/75732226/73682cd6-8591-429b-ada1-4c8f9b94fe96)

На этом этапе нужно сохранить информацию в .env файл. Получится примерно так:
```
USER="user"
PASSWD="password"
NAME="bewise_fastapi"
IP="172.25.0.2"
```

# Launch project 🐾
Данный пункты выполнять исключительно если - пункт "Starting DB using docker-compose" выполнился без ошибок.

### Warning!!!
Я использовал одну базу данных для оба кейса. Если Вы хотите использовать для каждого кейса отдельную базу данных, необходимо кое-что изменить.
Первое - это запустить ещё один контейнер, изменив docker-compose.yml:
```
version: '3'

services:
  db:
    image: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: <something> <-- Новое название для базы данных.
    volumes:
      - data:/var/lib/postgresql/data
    ports:
      - "5433:5432" <-- Другой порт, для примера 5433.

volumes:
  data:
```
Запуск нового контейнера:
```
docker-compose up -d
```
Изменить порт в переменной SQLALCHEMY_DATABASE_URL на порт, который был задан в файле docker-compose.yml:
```
SQLALCHEMY_DATABASE_URL = f'postgresql://{os.getenv("USER")}:{os.getenv("PASSWD")}@{os.getenv("IP")}:5433/{os.getenv("NAME")}'
```
Так же внести изменения в ".env" файл:
```
USER="user"
PASSWD="password"
NAME="<новое название базы данных>"
IP="<ip контейнера>"
```

### Quiz (1 case) 🔴
Для того чтобы запустить сервис Quiz и иметь возможность обратится к нему, необходимо вылонить следующую команду:
```
cd quiz/
```
```
uvicorn runserver_quiz:app --reload
```
Дальше можно протестировать сервис Quiz. Я использовал Postman для такой задачи (В качестве аналога можно обратиться с помощью "curl")
Создадим Post запрос для генерации 3 вопросов:

![3](https://github.com/acolyte-py/case-bewise.ai/assets/75732226/416b234b-2844-49bc-b5fd-d656254da90c)

Отличный результат. Проверим, что сохранилось в базу данных. Выполнив ряд команд:
```
sudo docker exec -it <id или name контейнера> psql -U <пользователь базы данных> -d <название базы данных>
```
Напишем простой запрос в базу данных:
```
SELECT * FROM questions; 
```
Вот такой пример вывода Вы можете получить:

![4](https://github.com/acolyte-py/case-bewise.ai/assets/75732226/ff39147c-d113-4ed6-934c-4aa3e069e105)

### Audio (2 case) 🔵
Для того чтобы запустить сервис Audio и иметь возможность обратится к нему, необходимо вылонить следующую команду:
```
cd audio/
```
```
uvicorn runserver_audio:app --reload
```
Дальше можно протестировать сервис Audio. Я использовал Postman для такой задачи (В качестве аналога можно обратиться с помощью "curl")
Создадим Post запрос для регистрации пользователя:

![5](https://github.com/acolyte-py/case-bewise.ai/assets/75732226/af74fbe3-430a-4793-b3ea-ee0c184b9252)

Создадим Post запрос для загрузки .wav аудиофайла:

![6 (2)](https://github.com/acolyte-py/case-bewise.ai/assets/75732226/2c9904f9-1536-4c8e-a7cd-359f06a1e36d)

Проверим ссылку из Post запроса - либо можно создать Get запрос заполнив нужные параметры:

![7 (2)](https://github.com/acolyte-py/case-bewise.ai/assets/75732226/64301866-d84c-4bac-bd95-9839988f673d)

Функционал работает. Проверим, что скачалось и какие записи сохранились в базу данных:

![8](https://github.com/acolyte-py/case-bewise.ai/assets/75732226/362c1813-db08-4d03-8abb-5c01abbeadc3)

После зайдем снова в базу данных:
```
sudo docker exec -it <id или name контейнера> psql -U <пользователь базы данных> -d <название базы данных>
```
Напишем простые запросы в базу данных:
```
SELECT * FROM users; 
```
```
SELECT * FROM audio; 
```
![9](https://github.com/acolyte-py/case-bewise.ai/assets/75732226/b0f40b7c-8e03-41c2-9e05-b7092e5e44e0)

В результате будет отображено две таблицы с данными.

## In Future 📌
Это не идеальное решение задачи. Есть много проблем я уверен:
* считаю что можно лучше обрабатывать транзакции, я наверника сделал это не очень грамотно;
* лучше проработать логику различных HTTPException. добавить их по больше, чтобы покрыть множество возможных исходов;
* добавить функционал с миграциями (я пытался у меня не получилось, пробовал alembic);
* скрыть информацию в docker-compose.yml файле (для примера в python есть os.getenv("KEY") - такое же решение добавить в docker-compose.yml файл).


## Built With 🔧
* [FastAPI](https://fastapi.tiangolo.com/) - Для разработки приложения;
* [PostgreSQL](https://www.postgresql.org/docs/) - Для работы с базой данных;
* [docker-compose](https://docs.docker.com/compose/) - Для запуска контейнера с нужным образом;
* [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) - Для работы с базы данными в python.

## Authors 🗿

* **Миронов Миша** - *Изначальная работа* - [vk](https://vk.com/acolyte_py) | tg - @acolytee.

## License ©

Данный проект использует лицензию MIT - [LICENSE](LICENSE) для деталей.
