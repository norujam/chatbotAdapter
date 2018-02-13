from chatbot.mongoDb import MongoDb
from chatbot.models import ChatLog
import logging
logger = logging.getLogger("django")


class ShortSentenceError(Exception):
    def __init__(self, sentence):
        logger.debug("no pattern/unknown short: "+sentence)


class ChatLogObjectMap:
    @staticmethod
    def insert_log(param):
        try:
            if param["action"] == 'input.unknown' and len(param["text"][0]) < 5:
                raise ShortSentenceError(param["text"][0])

            MongoDb.connect_db()
            chat_log = ChatLog(sentence=param["text"][0], actionType=param["action"])
            try:
                chat_log.keywords = param["parameters"]
            except KeyError:
                chat_log.keywords = []
            chat_log.save()
        except Exception as err:
            logger.error(err)
        except ShortSentenceError:
            pass
        finally:
            MongoDb.close_db()
