# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from models import DialogStepRouting, UserInfo

logger = logging.getLogger('telegram')


class ContextHandler:

    def __init__(self, context):
        self.context = context
  
    def __str__(self):
        return str(self.context)

    def context_serializer(self):
        """
        Serialize context data and handle different message type
        :return: serialize object
        """
        # Check chat section in message
        try:  # FIXME
            if self.context['message']['chat'] and \
                    self.context['message'].get('text', '').startswith('/'):
                return self.get_chat_data
            else:
                return self.get_prev_step
        except Exception, e:
            logger.debug("HANDLE_ERROR: {}\n\n\n".format(e))

    @property
    def get_chat_data(self):
        """
        Get chat data from context, if it's first conversation save user info data
        :return: dialog_data(list) with: chat_id, command, step
        """
        dialog, created = DialogStepRouting.objects.\
            update_or_create(chat_id=self.context['message']['chat']['id'],
                             defaults={'chat_id': self.context['message']['chat']['id'],
                                       'command': self.context['message']['text'],
                                       'step': 0})
        if created:
            # If new dialog safe user info
            user_info = UserInfo(first_name=self.context['message']['from'].get('first_name', ''),
                                 last_name=self.context['message']['from'].get('last_name', ''),
                                 username=self.context['message']['from'].get('last_name', ''),
                                 chat_id=self.context['message']['from']['id'])
            user_info.save()
        dialog_data = {'chat_id': dialog.chat_id, 'command': dialog.command, 'step': dialog.step, 'created':created}
        return dialog_data

    @property
    def get_prev_step(self):
        """
        Get previous step of dialog for this chat ID
        :return: dialog_date(list) with: chat_id, command, step
        """
        dialog, created = DialogStepRouting.objects. \
            get_or_create(chat_id=self.context['message']['chat']['id'],
                          defaults={'chat_id': self.context['message']['chat']['id'],
                                    'command': self.context['message'].get('text', ''),
                                    'step': 0})
        if created:
            # If new dialog safe user info
            user_info = UserInfo(first_name=self.context['message']['from'].get('first_name', ''),
                                 last_name=self.context['message']['from'].get('last_name', ''),
                                 username=self.context['message']['from'].get('last_name', ''),
                                 chat_id=self.context['message']['from']['id'])
            user_info.save()
        dialog_data = {'chat_id': dialog.chat_id, 'command': dialog.command, 'step': dialog.step, 'created':created}
        return dialog_data
