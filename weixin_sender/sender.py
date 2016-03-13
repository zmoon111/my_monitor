#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
description
1. real sender, save corpid and secret
"""

from common import *
import requests
import time
import os
import logging
import simplejson as json

class Sender(Singleton):
    """
    save corp_id, secret
    save token and refresh every 7200 Seconds
    """
    URL_GET_TOKEN = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"  # get method, 1)corpid,2)corpsecret
    URL_SEND_MSG = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="  # access_token=ACCESS_TOKEN, post method
    TOKEN_COTENT = "TOKEN_CONTENT"
    TOKEN_TIMESTAMP = "TOKEN_TIMESTAMP"

    def __init__(self):
        self._corp_id = "your_corp_id"
        self._secret = "your_secret"
        self.diff = 7000

    def send(self, text):
        token = self.refresh_token()
        payload = {"totag": "1", "msgtype": "text", "agentid": 1, "text": {"content": str(text)}, "safe": "0"}
        logging.debug(json.dumps(payload))

        response = requests.post(self.URL_SEND_MSG + token, data=json.dumps(payload))
        response_json = response.json()
        logging.debug(response_json)

    def refresh_token(self):
        token = ""
        try:
            last_time = 0
            need_refresh = False
            if os.path.exists(self.TOKEN_TIMESTAMP):
                f_time = open(self.TOKEN_TIMESTAMP, 'r')
                last_time = float(f_time.read())

            current_time = time.time()
            if current_time - last_time > self.diff:  # need refresh
                need_refresh = True

            if need_refresh:
                f_time = open(self.TOKEN_TIMESTAMP, 'w')
                f_time.write(str(time.time()))
                f_time.close()

                payload = {"corpid": self._corp_id, "corpsecret": self._secret}
                response = requests.get(self.URL_GET_TOKEN, params=payload)
                response_json = response.json()
                logging.debug(
                    response_json)  # {"access_token":"eqUGlBTiB5o2cNTejdZ2XecuPVbf4ZHbSxE8k7ctbnx_T7ckvoKKJqsauzPZCsqHaTn3YcDiQqpPoTRcia6mIA","expires_in":7200}

                token = response_json['access_token']
                f_content = open(self.TOKEN_COTENT, 'w')
                f_content.write(token)
                f_content.close()
            else:
                f_content = open(self.TOKEN_COTENT, 'r')
                token = f_content.read()
                f_content.close()
            logging.debug("token == %s", token)
            return token
        except Exception, e:
            logging.error("Error %d: %s" % (e.args[0], e.args[1]))
            return ""

