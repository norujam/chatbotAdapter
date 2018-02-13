from django.shortcuts import render
from django.http import JsonResponse
from chatbot.chatLogObjectMap import ChatLogObjectMap
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
import logging, json, requests, configparser

logger = logging.getLogger("django")

config = configparser.ConfigParser()
config.read('config.properties')


def index(request):
    logger.debug("vue index")
    return render(request, 'chatbot/index.html', )


def message(request):
    message_value = request.POST['message']
    if config['setSite']['dialogLoc'] == "outer":
        url = config['setSite']['dialogUrl']
        payload = {"message": message_value}
        result = json.loads(requests.post(url, data=payload).text)
    else:
        api_call_module = __import__(config['setSite']['apiCallModule'], fromlist=["detect_intent_texts"])
        result = api_call_module.detect_intent_texts([message_value])
        ChatLogObjectMap.insert_log(result)
    return JsonResponse(result)


@csrf_exempt
def test(request):
    logger.debug(request.POST['country'])
    return JsonResponse({'data': {"country": '1, 2, 3'}})


@csrf_exempt
@xframe_options_exempt
def adapter(request):
    json_data = json.loads(request.body.decode())['result']['parameters']
    for key in json_data.keys():
        global pKey
        pKey = key
        logger.debug(pKey)
    # url = ""
    # payload = {}
    if pKey == 'country':
        url = "http://127.0.0.1/chatbot/test/"
        payload = {"country": "123"}
    html = requests.post(url, data=payload)
    logger.debug(html.text)
    return JsonResponse(json.loads(html.text))

