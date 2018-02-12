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

    dictResult={}
    dictResult["text"] = texts
    try:
        action = response['intents'][0]['intent'].split("-")[0]
    except IndexError:
        action = "input.unknown"
    dictResult["action"] = action
    dictResult["main_message"] = response['output']['text'][0]
    if action in ['outer_retrieve']:
        dictResult["parameters"]=[]
        for entities in response['entities']:
            dictResult["parameters"].append(entities['value'])

    if action in ['outer_retrieve']:
        dictResult[action]={}
        for entities in response['entities']:
            dictResult[action][entities['entity']] = entities['value']

    return dictResult
