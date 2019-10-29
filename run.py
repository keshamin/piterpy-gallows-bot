from gallows_bot import GallowsBot
import config
import traceback
import time


bot = GallowsBot(
    admin_ids=config.ADMIN_IDS,
    token=config.TOKEN,
    threaded=False
)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        traceback.print_exc()
        time.sleep(5)
