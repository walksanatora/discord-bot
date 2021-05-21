import logging
import traceback
try:
    import bot
except Exception as e:
    logging.log(e,traceback.format_exc())