#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
description
1. send message from wechat account to employee which watch this wechat account
"""
from sender import Sender
import sys


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage : python weixin_sender.py text_to_send. "
        exit()

    sender = Sender()
    sender.send(str(sys.argv[1]))
