from typing import List

from telebot import TeleBot
from telebot.types import Message

from messages import Messages as M
from markups import main_menu, gen_game_markup
from models import User, Word
from stickers import MISTAKE_SICKERS, LOOSE_STICKER
from logger import logger


class GallowsBot(TeleBot):

    def __init__(self, admin_ids: List[int], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mistakes_allowed = 10  # max == 10

        self.register_handlers()

        for admin_id in admin_ids:
            self.send_message(admin_id, f'PiterPy Gallows бот запущен!')

    def register_handlers(self):
        self.message_handler(commands=['start'])(self.start)

        # Gallows
        self.message_handler(commands=['play'])(self.new_game)
        self.message_handler(regexp=f'^{M.GALLOWS_BUTTON}$')(self.new_game)

        self.message_handler(commands=['giveup'])(self.give_up)
        self.message_handler(regexp=f'^{M.GIVEUP_BUTTON}')(self.give_up)

        self.message_handler(func=lambda m: len(m.text.strip()) == 1 and m.text.isalnum())(self.guess_letter)

        self.message_handler(commands=['rules'])(self.rules)
        self.message_handler(regexp=f'^{M.RULES_BUTTON}$')(self.rules)

        self.message_handler(lambda: True)(self.not_found)

    # --- Handlers ---

    def start(self, message: Message):
        if len(User.objects.filter(telegram_id=message.chat.id)) == 0:
            user = User(telegram_id=message.chat.id)
            user.save()

            self.send_message(message.chat.id, M.START_MESSAGE, reply_markup=main_menu)
            logger.info(f'New user: {user.telegram_id}, username: {message.from_user.username}')
        else:
            self.send_message(message.chat.id, M.HELP, reply_markup=main_menu)
    
    # Gallows section
    def new_game(self, message: Message):
        user = User.objects.get(telegram_id=message.chat.id)
    
        if user.is_playing():
            self.send_message(message.chat.id, M.ALREADY_PLAYING)
            self._send_current_word(user)
            return

        random_word = Word.get_random_word()

        user.new_game(random_word)

        self.send_message(message.chat.id, M.THINK_OF_LETTERS(len(random_word)))
        self._send_current_word(user)

    def give_up(self, message: Message):
        user = User.objects.get(telegram_id=message.chat.id)
        self._loose(user)

    def guess_letter(self, message: Message):
        user = User.objects.get(telegram_id=message.chat.id)
        letter = message.text.strip().lower()

        # Letter is already played
        if letter in user.used_letters:
            self.send_message(message.chat.id, M.USED_LETTER)
            self._send_current_word(user)
            return

        user.guess_letter(letter)

        if letter not in user.complete_word:
            if user.mistakes > self.mistakes_allowed:
                self._loose(user)
                user.loose()
                self._send_stats(user)
            else:
                self._mistake(user)
        else:
            if user.current_word == user.complete_word:
                self._win(user)
                user.win()
                self._send_stats(user)
            else:
                self._send_current_word(user)

    def rules(self, message: Message):
        self._send_rules(chat_id=message.chat.id)

    def not_found(self, message: Message):
        user = User.objects.get(telegram_id=message.chat.id)

        if user.is_playing():
            self.send_message(message.chat.id, M.NOT_FOUND_IN_GAME)
        else:
            self.send_message(message.chat.id, M.NOT_FOUND)

    # --- Shortcut methods ---

    def _send_current_word(self, user: User):
        spaced_word = ' '.join(user.current_word)

        game_markup = gen_game_markup(word=user.complete_word, used_letters=user.used_letters)
        self.send_message(user.telegram_id, spaced_word, reply_markup=game_markup)

    def _loose(self, user: User):
        self.send_sticker(user.telegram_id, LOOSE_STICKER)
        self.send_message(user.telegram_id, M.IT_WAS(user.complete_word), reply_markup=main_menu)

    def _mistake(self, user: User):
        self.send_sticker(user.telegram_id, self.get_mistake_sticker(user.mistakes))
        self._send_current_word(user)

    def _win(self, user: User):
        self.send_message(user.telegram_id, M.YOU_WIN)
        self.send_message(user.telegram_id, M.IT_WAS(user.complete_word), reply_markup=main_menu)

    def _send_rules(self, chat_id: int):
        self.send_message(chat_id, M.RULES)

    def _send_stats(self, user: User):
        self.send_message(user.telegram_id, M.STATS(user))

    # --- Utility methods ---

    def get_mistake_sticker(self, mistake_num: int) -> str:
        return MISTAKE_SICKERS[mistake_num]
