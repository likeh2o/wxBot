#!/usr/bin/env python
# coding: utf-8

import os
import sys
import traceback
import webbrowser
import pyqrcode
import requests
import mimetypes
import json
import xml.dom.minidom
import urllib
import time
import re
import random
from traceback import format_exc
from requests.exceptions import ConnectionError, ReadTimeout
import HTMLParser
import ConfigParser
import json


class Baidu:
    def get_token(self):
	url = "https://openapi.baidu.com/oauth/2.0/token"
	body = {'grant_type': 'client_credentials', 'client_id': 'dNIfNdOhC57xZMe8hBSxxPly', 'client_secret': 'TG33eq2Q65zW3r7YbYyllhLO6ShKwOLw'}
	r = requests.post(url, data=body)
	respond = json.loads(r.text)
	access_token = respond['access_token']

	#write this file
	fsock = open("./conf_baidu.ini", "w")
	fsock.write("[main]\n");
	fsock.write("access_token="+access_token);
	fsock.close()

	print 'access_token='+access_token

def main():
    bd = Baidu()
    bd.get_token()


if __name__ == '__main__':
    main()

