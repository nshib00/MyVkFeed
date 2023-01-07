# -*- coding: utf-8 -*-

import logging


class VkAuthError(Exception): pass
class VkAPIError(Exception): pass


logger = logging.getLogger('logic.logic')


def check_vk_api_errors(checked_logic_class):
    request = None
    if 'error' in checked_logic_class.feed_req.json():
        request = (checked_logic_class.feed_req.json(), 'logic.feed_req')
    elif 'error' in checked_logic_class.groups_req.json():
        request = (checked_logic_class.groups_req.json(), 'logic.groups_req')

    if request is not None:
        error_code = request[0]['error']['error_code']
        error_msg = request[0]['error']['error_msg']
        logger.error(f'VK API error #{error_code} in {request[1]}: {error_msg}')
        if error_code == 5:
            raise VkAuthError('Ошибка авторизации: авторизуйтесь в ВК в вашем браузере, затем попробуйте зайти еще раз.')
        else:
            raise VkAPIError(f'VK API error #{error_code} in {request[1]}: {error_msg}')