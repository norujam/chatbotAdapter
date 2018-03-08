import logging
import configparser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("django")

config = configparser.ConfigParser()
config.read('config.properties')


@csrf_exempt
def country_list(request):
    country = request.POST['country']
    result = dict()
    if country in ['나라']:
        result["result"] = "미국, 영국, 일본"
    elif country in ['유럽']:
        result["result"] = "영국"

    return JsonResponse(result)


@csrf_exempt
def study_list(request):
    country = request.POST['country']
    kind = request.POST['kind']
    logger.debug("country="+country)
    logger.debug("kind="+kind)
    result = dict()
    if country in ['미국'] and kind in ['유학']:
        result["result"] = "20개가 있습니다."

    return JsonResponse(result)
