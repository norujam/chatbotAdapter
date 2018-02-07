from chatbot.mongoDb import MongoDb
from chatbot.models import ChatData
import logging

logger = logging.getLogger("django")

class ChatDataObjectMap:
    async def insertData(param):
        try:
            logger.debug(param)
            MongoDb.connect_db()
            chatData = ChatData(sentence=param["text"][0])
            chatData.keywords = param["parameters"]
            chatData.save()
        finally:
            MongoDb.close_db()
