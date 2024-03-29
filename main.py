import json
import random
import eventlet
import socketio
from loguru import logger

from settings import QUESTIONS, INDEX, ASSETS
from src.player import Player
from src.riddle import Riddle

sio = socketio.Server()

app = socketio.WSGIApp(
    sio,
    static_files={
        # Разрешаем открывать главную страницу
        '/': {'content_type': 'text/html', 'filename': INDEX},
        '/assets/': ASSETS,
    },
)

riddle_data: list[dict] = json.load(open(QUESTIONS))
riddles = [Riddle(**r) for r in riddle_data]
players: dict[str: Player] = {}


@sio.event
def connect(sid, environ):
    """ Обработчик события - подключение. """
    players[sid] = Player()
    logger.info(f"Пользователь {sid} подключился")


@sio.event
def disconnect(sid):
    """ Обработчик события - отключение. """
    logger.info(f"Пользователь {sid} отключился")


@sio.on("next")
def get_next(sid, data):
    """ Обработчик события - вывод следующей загадки. """
    logger.info(f"Пользователь {sid} запросил загадку")

    riddle = random.choice(riddles)
    riddle_text = riddle.riddle

    player = players[sid]
    player.current_riddle = riddle

    logger.info(f"Отправили пользователю {sid} загадку {riddle_text}")
    sio.emit("riddle", data={"text": riddle_text})


@sio.on("answer")
def check_answer(sid, data):
    """ Обработчик события - вывода результата и верного ответа. """
    logger.info(f"Пользователь {sid} прислал ответ {data}")

    player_attempt = data.get("text")
    player = players.get(sid)

    current_riddle = player.current_riddle
    riddle = current_riddle.riddle

    is_correct = current_riddle.check(player_attempt)
    correct_answer = current_riddle.answers

    if is_correct:
        player.add_score()

    logger.info(f"Отправляем пользователю {sid} обратную связь {player_attempt} is_correct {is_correct}")
    logger.info(f"Очки {sid}: {player.score}")

    sio.emit("result", data={"text": riddle, "is_correct": is_correct, "answer": correct_answer})
    sio.emit("score", data={"value": player.score})


eventlet.wsgi.server(
    eventlet.listen(('', 80)),
    app
)
