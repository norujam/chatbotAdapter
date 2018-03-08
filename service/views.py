import logging
import configparser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("django")

config = configparser.ConfigParser()
config.read('config.properties')


@csrf_exempt
def country_list(request):
    param_value = request.POST['paramValue']
    logger.debug("param="+param_value)
    result = dict()
    result["data"] = {}
    if param_value in ['나라']:
        result["data"]["result"] = "미국, 영국, 일본"

    return JsonResponse(result)
