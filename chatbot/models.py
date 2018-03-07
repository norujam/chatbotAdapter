from mongoengine import *
import datetime


class ChatLog(Document):
    actionType = StringField(max_length=30, required=True)
    sentence = StringField(max_length=300, required=True)
    keywords = ListField(StringField(max_length=30))
    regDate = DateTimeField(default=datetime.datetime.now)