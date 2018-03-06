import dialogflow, json, logging, configparser

logger = logging.getLogger("django")

config = configparser.ConfigParser()
config.read('config.properties')


def detect_intent_texts(texts):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    project_id=config['googleApi']['projectId']
    session_id=config['googleApi']['sessionId']
    language_code="ko"
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
    if any(response.query_result.action in s for s in ['outer_retrieve', 'outer_response']):
        dict_result["parameters"] = []
        parameters = response.query_result.parameters
        for i in parameters.keys():
            dict_result["parameters"].append(parameters[i])

    if any(response.query_result.action in s for s in ['outer_retrieve']):
        parameters = response.query_result.parameters
        dict_result[response.query_result.action] = {}
        for i in parameters.keys():
            dict_result[response.query_result.action][i] = parameters[i]

    if any(response.query_result.action in s for s in ['outer_response']):
        payload_data = response.query_result.webhook_payload
        for i in payload_data.keys():
            dict_result[i] = payload_data[i]
    logger.debug(dict_result)
    return dict_result
