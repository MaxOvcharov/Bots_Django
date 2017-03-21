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
    request.query = ""

    response = request.getresponse().read()
    obj = json.loads(response, encoding='utf8')
    pprint.pprint(obj)
    print '#*#*#*#' * 12, '\n'
    try:
        alternate_result = obj.get('alternateResult')
        if not alternate_result:
            agent = obj.get('result').get('fulfillment').get('speech')
            print agent
            # pprint.pprint(obj)
        else:
            # pprint.pprint(obj)
            small_talk = obj.get('alternateResult').get('fulfillment').get('speech')
            if not small_talk:
                agent = obj.get('result').get('fulfillment').get('speech')
                print agent
            else:
                print small_talk
    except AttributeError, e:
        print e

if __name__ == '__main__':
    main()