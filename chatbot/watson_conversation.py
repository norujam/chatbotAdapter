import json, logging, configparser
from watson_developer_cloud import ConversationV1

logger = logging.getLogger("django")

config = configparser.ConfigParser()
config.read('config.properties')


def detect_intent_texts(texts):
    api_user_name = config['watsonApi']['apiUsername']
    api_password = config['watsonApi']['apiPassword']
    version = config['watsonApi']['version']
    workspace_id = config['watsonApi']['workspaceId']

    conversation = ConversationV1(
        username=api_user_name,
        password=api_password,
        version=version
    )

    response = conversation.message(
        workspace_id=workspace_id,
        input={
            'text': texts[0]
        }
    )

    dict_result = dict()
    dict_result["text"] = texts
    try:
        action = response['intents'][0]['intent'].split("-")[0]
    except IndexError:
        action = "input.unknown"
    dict_result["action"] = action
    dict_result["main_message"] = response['output']['text'][0]
    if action in ['outer_retrieve']:
        dict_result["parameters"]=[]
        for entities in response['entities']:
            dict_result["parameters"].append(entities['value'])

    if action in ['outer_retrieve']:
        dict_result[action] = {}
        for entities in response['entities']:
            dict_result[action][entities['entity']] = entities['value']

    return dict_result
