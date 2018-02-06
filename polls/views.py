from django.shortcuts import render
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def index(request):
    logger.debug('call index')
    return HttpResponse("Hello, world. You're at the polls index.")
