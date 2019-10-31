from random import choice


class Messages(object):
    def __getattribute__(self, item):
        attr = super().__getattribute__(item)
        if isinstance(attr, tuple):
            return choice(attr)

        return attr

    # Main menu
    GALLOWS_BUTTON = 'Играть в виселицу ⚔️'
    INFO_BUTTON = 'Инфо'
    STATS_BUTTON = 'Рейтинг игроков 🔝'

    START_MESSAGE = 'Привет! Здесь будет стартовый текст.'
    # TODO: add description
    HELP = 'ЗДЕСЬ ДОЛЖНО БЫТЬ КАКОЕ_ТО ОПИСАНИЕ БОТА И ПРАВИЛА ПОЛУЧЕНИЯ СТАФИКА 💰'
    NOT_FOUND = 'Не могу распарсить сообщение. Воспользуйтесь главным меню.'
    NOT_FOUND_IN_GAME = 'Не могу распарсить сообщение. Воспользуйтесь игровым меню.'
    INFO = 'ЗДЕСЬ ДОЛЖНА БЫТЬ ИНФОРМАЦИЯ О КОМПАНИИ И ЧТО-НИБУДЬ ЕЩЕ ЧТО НУЖНО!'
    WL_TOP_HEAD = '*Топ игроков по разнице win/loose:*\n'

    # Gallows
    ALREADY_PLAYING = 'Вы уже в игре!'
    THINK_OF_LETTERS = lambda x: f'Я загадал слово из {x} букв.'
    USED_LETTER = 'Эта буква уже сыграна.'
    IT_WAS = lambda x: f'Это было слово "{x}"'
    YOU_WIN = 'Да! Вы выиграли!'
    STATS = lambda user: f'🏆 Побед: {user.wins}\n' \
                         f'💣 Поражений: {user.looses}'

    # TODO: Write rules text!
    RULES = 'ЗДЕСЬ БУДУТ ПРАВИЛА!'

    # Game menu
    RULES_BUTTON = 'Правила'
    GIVEUP_BUTTON = 'Сдаюсь'
