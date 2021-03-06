#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import json
import pprint

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '3a54443227c44c73971ea5f8dd8c88cb'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'ru'  # optional, default value equal 'en'
    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    request.query = "Привет Бот"

    response = request.getresponse().read()
    obj = json.loads(response, encoding='utf8')
    pprint.pprint(obj)
    print '#*#*#*#' * 12, '\n'
    try:
        alternate_result = obj.get('alternateResult')
        if not alternate_result:
            # If response with answer from domain(result) - Small Talk
            answer = obj.get('result').get('fulfillment').get('speech')
            print answer, "DOMAIN1"
        else:
            # If response with answer from agent(result)
            small_talk = obj.get('alternateResult').get('fulfillment').get('speech')
            if not small_talk:
                answer = obj.get('result').get('fulfillment').get('speech')
                print answer, "AGENT1"
            else:
                # If response with answer from domain(alternate result) - Small Talk
                print small_talk, "DOMAIN2"
    except AttributeError, e:
        print e

if __name__ == '__main__':
    main()