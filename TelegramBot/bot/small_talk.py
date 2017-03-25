#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os.path
import sys

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

from TelegramBot.settings import BOT_TOKEN, CLIENT_ACCESS_TOKEN

logger = logging.getLogger('telegram')


def small_talk(message):
    """
        This method connect to Api.ai Small Talk domain
        :param message: input message
        :return: output message from Api.ai
    """
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'ru'  # optional, default value equal 'en'
    request.session_id = BOT_TOKEN[:35]
    request.query = message

    response = request.getresponse().read()
    obj = json.loads(response, encoding='utf8')
    try:
        alternate_result = obj.get('alternateResult')
        if not alternate_result:
            # If response with answer from domain(result) - Small Talk
            answer = obj.get('result').get('fulfillment').get('speech')
            return answer
        else:
            domain = obj.get('alternateResult').get('fulfillment').get('speech')
            if not domain:
                # If response with answer from agent(result)
                answer = obj.get('result').get('fulfillment').get('speech')
                return answer
            else:
                # If response with answer from domain(alternate result) - Small Talk
                return domain
    except AttributeError, e:
        logger.error('Handle ERROR: {0}'.format(e))


def main():
    message = raw_input("Введите фразу: ")
    # message = 'Как тебя зовут'
    print small_talk(message)

if __name__ == '__main__':
    main()
