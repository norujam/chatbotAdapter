import json, logging, configparser
from watson_developer_cloud import ConversationV1

logger = logging.getLogger("django")

config = configparser.ConfigParser()
config.read('config.properties')

def detectIntentTexts(texts):
    apiUsername=config['watsonApi']['apiUsername']
    apiPassword=config['watsonApi']['apiPassword']
    version=config['watsonApi']['version']
    workspaceId=config['watsonApi']['workspaceId']

    conversation = ConversationV1(
        username=apiUsername,
        password=apiPassword,
        version=version
    )

    response = conversation.message(
        workspace_id=workspaceId,
        input={
            'text':texts[0]
        }
    )
    logger.debug(response)

    dictResult={}
    dictResult["text"] = texts
    dictResult["action"] = "watson_test"
    dictResult["main_message"] = response['output']['text']

    return dictResult
