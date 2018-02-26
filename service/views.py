from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def country_list(request):
    return JsonResponse({'data': {"country": '1, 2, 3'}})
