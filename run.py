from gallows_bot import GallowsBot
import config
import traceback


bot = GallowsBot(
    admin_ids=config.ADMIN_IDS,
    token=config.TOKEN
)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        traceback.print_exc()
