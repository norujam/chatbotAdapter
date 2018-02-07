from mongoengine import *
import configparser

config = configparser.ConfigParser()
config.read('config.properties')

class MongoDb:
    def connect_db():
        global db
        db = connect(
            db=config['DB']['db'],
            host=config['DB']['host'],
            port=int(config['DB']['port']),
            username=config['DB']['username'],
            password=config['DB']['password'],
            authSource=config['DB']['authSource'],
            maxPoolSize=50,
        )

    def close_db():
        global db
        db.close