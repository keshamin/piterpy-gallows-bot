from gallows_bot import GallowsBot
import config


bot = GallowsBot(
    admin_ids=config.ADMIN_IDS,
    token=config.TOKEN
)

bot.polling(none_stop=True)
