import logging


logger = logging.getLogger('Bot')
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(
    logging.Formatter('%(filename)-10s[LINE:%(lineno)04d]# %(levelname)-8s [%(asctime)s]  %(message)s')
)
logger.addHandler(stream_handler)
