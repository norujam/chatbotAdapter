from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from chatbot import google_dialog
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
import logging
import json
import requests

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)

def index(request):
    logger.debug("vue index")
    return render(request, 'chatbot/index.html')

def message(request):
    message  = request.POST['message']    
    result = google_dialog.detect_intent_texts([message]) 
    return JsonResponse(result)
    #return JsonResponse(result)

@csrf_exempt
def test(request):
    logger.debug(request.POST['country'])
    return JsonResponse({'data':{"country":'1, 2, 3'}}) 

@csrf_exempt
@xframe_options_exempt
def adapter(request):
    jsonData = json.loads(request.body.decode())['result']['parameters']
    #pKey = "test";
    for key in jsonData.keys():
        global pKey
        pKey = key
        logger.debug(pKey)
    #url = ""
    #payload = {}
    if pKey == 'country':
        global url, payload
        url = "http://127.0.0.1/chatbot/test/"
        payload = {"country":"123"}
    html = requests.post(url, data=payload)
    logger.debug(html.text)
    return JsonResponse(json.loads(html.text))

