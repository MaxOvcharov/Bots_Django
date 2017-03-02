# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from models import DialogStepRouting, UserInfo

logger = logging.getLogger('telegram')


class ContextHandler:

    def __init__(self, context):
        self.context = context

    def context_serializer(self):
        """
        Serialize context data and handle different message type
        :return: serialize object
        """
        # Check chat section in message
        if self.context['message']['chat'] and \
                self.context['message']['entities'].get(u'type', '') == u'bot_command':
            return self.get_chat_data()
        else:
            return [self.context['message']['chat'], '', 0]

    def get_chat_data(self):
        """
        Get chat data from context, if it's first conversation save user info data
        :return: dialog dict with: chat_id, command, step
        """
        dialog, created = DialogStepRouting.objects.\
                            get_or_create(chat_id=self.context['message']['chat']['id'],
                                          defaults={'chat_id': self.context['message']['chat']['id'],
                                                    'command': self.context['message']['from']['text'],
                                                    'step': 0})
        if created:
            # If new dialog safe user info
            user_info = UserInfo(first_name=self.context['message']['from'].get('first_name', ''),
                                 last_name=self.context['message']['from'].get('last_name', ''),
                                 username=self.context['message']['from'].get('last_name', ''),
                                 chat_id=self.context['message']['from']['id'])
            user_info.save()

        return list(dialog)





