import dialogflow, json, logging, configparser

logger = logging.getLogger("django")

config = configparser.ConfigParser()
config.read('config.propertis')

def detect_intent_texts(texts):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    project_id=config['googleApi']['projectId']
    session_id=config['googleApi']['sessionId']
    language_code="ko"
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    dictResult={}
    dictResult["action"] = response.query_result.action
    #print(response.query_result)
    dictResult["main_message"] = response.query_result.fulfillment_messages[0].text.text[0]
    if response.query_result.action in ['outer_retrieve']:
        parameters = response.query_result.parameters
        dictResult[response.query_result.action]={}
        for i in parameters.keys():
            logger.debug(parameters[i])
            dictResult[response.query_result.action][i] = parameters[i]

    if response.query_result.action in ['outer_response']:
        payloadData = response.query_result.webhook_payload
        dictResult[response.query_result.action]={}
        for i in payloadData.keys():
            dictResult[response.query_result.action][i] = payloadData[i]

    return dictResult
