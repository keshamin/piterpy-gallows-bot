from typing import Iterable, List

import mongoengine as me
import config
from logger import logger


logger.info(f'DB connection string: {config.DB_URI}')
db = me.connect(host=config.DB_URI)


class User(me.Document):
    telegram_id = me.LongField(required=True, primary_key=True)
    username = me.StringField(max_length=100)
    full_name = me.StringField(max_length=100)
    current_word = me.StringField(max_length=100)
    complete_word = me.StringField(max_length=100)
    used_letters = me.ListField(me.StringField(regex='[a-zа-я0-9]{1}', null=False))
    wins = me.IntField(null=False, default=0)
    games = me.IntField(null=False, default=0)

    @classmethod
    def top_by_wl_diff(cls) -> List:
        return sorted(cls.objects.all(), reverse=True, key=lambda u: u.wl_diff)

    @classmethod
    def top_by_wins(cls) -> Iterable:
        return sorted(cls.objects.all(), reverse=True, key=lambda u: u.wins)

    def is_playing(self) -> bool:
        return self.current_word is not None

    @property
    def mistakes(self):
        letters_played = len(set(self.used_letters))
        correct_letters_played = len(set(self.current_word)) - 1    # Minus 1 is to remove '_' from set
        return letters_played - correct_letters_played

    @property
    def loses(self):
        return self.games - self.wins

    @property
    def wl_diff(self):
        return self.wins - self.loses

    def new_game(self, word: str):
        self.complete_word = word
        self.current_word = '_' * len(word)
        self.save()

    def _end_game(self):
        self.current_word = None
        self.complete_word = None
        self.used_letters = []

        self.games += 1

    def win(self):
        self.wins += 1
        self._end_game()
        self.save()

    def lose(self):
        self._end_game()
        self.save()

    def guess_letter(self, letter: str):
        if len(letter) != 1:
            raise ValueError('Only 1 letter accepted!')

        if letter in self.used_letters:
            return

        self.used_letters.append(letter)

        if letter in self.complete_word:
            # Fill all occurrences of the letter in self.current_word
            for idx, i_letter in enumerate(self.complete_word):
                if i_letter == letter:
                    self.current_word = ''.join((self.current_word[:idx], letter, self.current_word[idx + 1:]))

        self.save()


class Word(me.Document):
    word = me.StringField(primary_key=True, regex=r'[a-zа-я0-9]+')

    @classmethod
    def get_random_word(cls) -> str:
        word = cls.objects.aggregate({'$sample': {'size': 1}}).next()['_id']
        return word.lower()
