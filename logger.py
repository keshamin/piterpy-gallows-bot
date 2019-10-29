import logging
from functools import wraps

from telebot.types import Message, CallbackQuery

logger = logging.getLogger('Bot')
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(
    logging.Formatter('%(filename)-10s[LINE:%(lineno)04d]# %(levelname)-8s [%(asctime)s]  %(message)s')
)
logger.addHandler(stream_handler)


def handler_log(func: callable) -> callable:

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        log_string = ''
        if len(args) > 0:
            if isinstance(args[0], Message):
                msg = args[0]
                log_string = f'Chat ID: {msg.chat.id}, Handler: {func.__name__}, Text: {msg.text}'
            if isinstance(args[0], CallbackQuery):
                cb = args[0]
                log_string = f'Chat ID: {cb.message.chat.id}, Handler: {func.__name__}, Data: {cb.data}'
        if len(args) > 1:
            log_string += f', Additional args: {args[1:]}'

        logger.info(log_string)
        return func(self, *args, **kwargs)

    return wrapper
