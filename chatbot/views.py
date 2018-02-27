from django.shortcuts import render
from django.http import JsonResponse
from chatbot.chatLogObjectMap import ChatLogObjectMap
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from chatbot import doNotCallApi as DoNotCallApi
import logging
import json
import requests
import configparser

logger = logging.getLogger("django")

config = configparser.ConfigParser()
config.read('config.properties')


def index(request):
    logger.debug("vue index")
    return render(request, 'chatbot/index.html')


def message(request):
    message_value = request.POST['message']
    result = DoNotCallApi.check_message(message_value)
    if result is None and config['setSite']['dialogLoc'] == "outer":
        url = config['setSite']['dialogUrl']
        payload = {"message": message_value}
        result = json.loads(requests.post(url, data=payload).text)
    elif result is None:
        api_call_module = __import__(config['setSite']['apiCallModule'], fromlist=["detect_intent_texts"])
        result = api_call_module.detect_intent_texts([message_value])
        ChatLogObjectMap.insert_log(result)
    return JsonResponse(result)


@csrf_exempt
@xframe_options_exempt
def web_hook(request):
    json_data = json.loads(request.body.decode())
    action = json_data['result']['action']
    json_data = json_data['result']['parameters']
    for key in json_data.keys():
        global pKey
        pKey = key
        logger.debug(pKey)
    # url = ""
    # payload = {}
    if pKey == 'country':
        url = config['service']['service_url']+"service_country_list/"
        payload = {"param": pKey}
    html = requests.post(url, data=payload)
    # logger.debug(html.text)
    return JsonResponse(json.loads(html.text))

