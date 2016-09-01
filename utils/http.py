# -*- coding: utf-8 -*-

import logging

import requests

logger = logging.getLogger('Utils.HTTP')


def get(url, headers=None, proxies=None, timeout=3, retry_times=5):
    for i in range(retry_times):
        try:
            rsp = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
            if rsp.status_code == 200:
                return rsp
            if i+1 <= retry_times:
                logger.debug('远端内容异常，重试#%d %s', i+1, url)
        except requests.exceptions.RequestException:
            if i+1 <= retry_times:
                logger.debug('连接远端错误，重试#%d %s', i + 1, url)
    logger.warning('请求失败 %s', url)
    return None


def get_raw_content(*args, **kwargs):
    rsp = get(*args, **kwargs)
    if rsp is None:
        return None
    else:
        return rsp.content


def get_content(url, encoding='UTF-8', *args, **kwargs):
    rsp = get(url, *args, **kwargs)
    if rsp is None:
        return None
    else:
        rsp.encoding = encoding
        return rsp.text


def get_json(url, *args, **kwargs):
    rsp = get(url, *args, **kwargs)
    if rsp is None:
        return None
    try:
        return rsp.json()
    except ValueError:
        logger.warning('远端内容不是JSON %s', url)
        return None
