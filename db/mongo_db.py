import configparser
import logging
from mongoengine import *

logger = logging.getLogger("django")

CONFIG = configparser.ConfigParser()
CONFIG.read('config.properties')


class MongoDb:
    def __init__(self):
        self.db_connect = None

    @staticmethod
    def connect_db():
        try:
            MongoDb.db_connect = connect(
                db=CONFIG['DB']['db'],
                host=CONFIG['DB']['host'],
                port=int(CONFIG['DB']['port']),
                username=CONFIG['DB']['username'],
                password=CONFIG['DB']['password'],
                authSource=CONFIG['DB']['authSource'],
                maxPoolSize=50,
            )
        except Exception as err:
            logger.error(err)
            raise err

    @staticmethod
    def close_db():
        try:
            MongoDb.db_connect.close()
        except NameError:
            pass

    @staticmethod
    def insert_document(obj_doc):
        try:
            MongoDb.connect_db()
            obj_doc.save()
        except Exception as err:
            logger.error(err)
            raise err
        finally:
            MongoDb.close_db()
