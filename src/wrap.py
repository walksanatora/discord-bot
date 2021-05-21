import logging
import traceback
try:
    import bot
except Exception as e:
    logging.log(e,traceback.log_exc())