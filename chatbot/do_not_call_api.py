import re
from chatbot import make_return_message


def check_character(param):
    pattern = re.compile('[^a-zA-Z0-9가-핳?.,]')
    return pattern.match(param)


def check_message(param):
    if param is None or param == '':
        return make_return_message.create_message("메세지가 없습니다.")
    elif check_character(param) is not None:
        return make_return_message.create_message("확인할 수 없는 단어가 존재합니다.")
