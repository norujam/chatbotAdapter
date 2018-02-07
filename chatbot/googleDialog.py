from chatbot.chatDataObjectMap import ChatDataObjectMap
import dialogflow, json, logging, configparser

logger = logging.getLogger("django")

config = configparser.ConfigParser()
config.read('config.properties')

async def detectIntentTexts(texts):
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
    dictResult["text"] = texts
    dictResult["action"] = response.query_result.action
    #logger.debug(response.query_result)
    dictResult["main_message"] = response.query_result.fulfillment_messages[0].text.text[0]
    if response.query_result.action in ['outer_retrieve', 'outer_response']:
        dictResult["parameters"]=[]
        parameters = response.query_result.parameters
        for i in parameters.keys():
            dictResult["parameters"].append(parameters[i])

    if response.query_result.action in ['outer_retrieve']:
        parameters = response.query_result.parameters
        dictResult[response.query_result.action]={}
        for i in parameters.keys():
            dictResult[response.query_result.action][i] = parameters[i]

    if response.query_result.action in ['outer_response']:
        payloadData = response.query_result.webhook_payload
        dictResult[response.query_result.action]={}
        for i in payloadData.keys():
            dictResult[response.query_result.action][i] = payloadData[i]

    await ChatDataObjectMap.insertData(dictResult)

    return dictResult
