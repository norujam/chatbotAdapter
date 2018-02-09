from chatbot.mongoDb import MongoDb
from chatbot.models import ChatData
import logging

logger = logging.getLogger("django")

class ChatDataObjectMap:
    def insertData(param):
        try:
            MongoDb.connect_db()
            chatData = ChatData(sentence=param["text"][0]
                    ,actionType=param["action"])
            try:
                chatData.keywords = param["parameters"]
            except KeyError:
                chatData.keywords = []
            chatData.save()
        except Exception as err:
            logger.error(err)
            raise
        finally:
            MongoDb.close_db()
