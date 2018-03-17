import json
import logging
import configparser
import dialogflow

logger = logging.getLogger("django")

CONFIG = configparser.ConfigParser()
CONFIG.read('config.properties')


def detect_intent_texts(texts):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    project_id = CONFIG['googleApi']['projectId']
    session_id = CONFIG['googleApi']['sessionId']
    language_code = "ko"
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=texts[0], language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    # logger.debug("call detect="+response.query_result)
    dict_result = dict()
    dict_result["text"] = texts
    dict_result["action"] = response.query_result.action
    dict_result["main_message"] = response.query_result.fulfillment_messages[0].text.text[0]

    if any(response.query_result.action.find(s) > -1
           for s in ['outer_retrieve', 'outer_response']):
        parameters = response.query_result.parameters
        dict_result["parameters"] = {}
        for i in parameters.keys():
            dict_result["parameters"][i] = parameters[i]

    logger.debug(dict_result)
    return dict_result
