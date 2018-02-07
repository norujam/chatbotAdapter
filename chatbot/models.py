from mongoengine import *

class ChatData(Document):
    sentence = StringField(max_length=300, required=True)
    keywords = ListField(StringField(max_length=30))