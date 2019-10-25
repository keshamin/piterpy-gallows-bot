from telebot import types
from messages import Messages as M
import re


main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
main_menu.add(*[types.KeyboardButton(text) for text in (M.GALLOWS_BUTTON, M.INFO_BUTTON)])

digits = ['1234567890']
english = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
russian = ['йцукенгшщзхъ', 'фывапролджэ', 'ячсмитьбю']


def get_letters(word):
    if len(re.findall('[а-я]+', word.lower())):
        return russian
    if len(re.findall('[a-z]+', word.lower())):
        return english
    raise ValueError(f'The word {word} doesn\'t match neither english or russian language!')


def gen_game_markup(word, used_letters):
    game_markup = types.ReplyKeyboardMarkup()

    all_keys = digits + get_letters(word)

    for key_row in all_keys:
        row = []

        for key in key_row:
            if key in used_letters:
                continue
            row.append(types.KeyboardButton(key))

        game_markup.row(*row)

    game_markup.row(*[types.KeyboardButton(M.RULES_BUTTON),
                      types.KeyboardButton(M.GIVEUP_BUTTON)])
    return game_markup
