import logging
import json
import requests
import configparser
from django.shortcuts import render
from django.http import JsonResponse
from chatbot.chat_log_object_map import ChatLogObjectMap
from chatbot import do_not_call_api

LOGGER = logging.getLogger("django")

CONFIG = configparser.ConfigParser()
CONFIG.read('config.properties')


def index(request):
    LOGGER.debug("vue index")
    return render(request, 'chatbot/index.html')


def message(request):
    message_value = request.POST['message']
    result = do_not_call_api.check_message(message_value)
    if result is None and CONFIG['setSite']['dialogLoc'] == "outer":
        url = CONFIG['setSite']['dialogUrl']
        payload = {"message": message_value}
        result = json.loads(requests.post(url, data=payload).text)
    elif result is None:
        api_call_module = __import__(CONFIG['setSite']['apiCallModule'],
                                     fromlist=["detect_intent_texts"])
        result = api_call_module.detect_intent_texts([message_value])
        if any(result["action"].find(s) > -1 for s in ['outer_retrieve', 'outer_response']):
            result["result"] = web_hook(result)

        ChatLogObjectMap.insert_log(result)

    return JsonResponse(result)


def web_hook(result):
    try:
        action = result['action'].split("_")
        parameters = result['parameters']
        payload = {}
        for key in parameters.keys():
            payload[key] = parameters[key]
        # url = ""
        # payload = {}

        url = CONFIG['service']['service_url']+action[2]+"/"
        html = requests.post(url, data=payload)
        logging.debug(html)
    except Exception as err:
        logging.error(err)
        raise err
    return json.loads(html.text)["result"]

