#!/usr/bin/env python
# coding: utf-8

import os
import sys
import requests
import mimetypes
import json
import urllib
import time
import re
import random
from traceback import format_exc
from requests.exceptions import ConnectionError, ReadTimeout
import HTMLParser
import ConfigParser
from urllib import quote
from pydub import AudioSegment ###需要安装pydub、ffmpeg
#import wave
#import io
import base64


class Baidu:
    def __init__(self):
        self.access_token = ""

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf_baidu.ini')
            self.access_token = cf.get('main', 'access_token')
        except Exception:
            pass
        print 'access_token:', self.access_token

    def get_mp3(self, msg):
	url = "http://tsn.baidu.com/text2audio"
	msg_encode = quote(msg)
	body = {'tex': msg_encode, 'lan': 'zh', 'cuid': 'xiaokele', 'ctp': '1', 'tok': self.access_token}
	r = requests.get(url, params=body)

	#write this file
	fsock = open("voice_baidu/tts.mp3", "w")
	fsock.write(r.content);
	fsock.close()

	os.system('mpg123 /home/pi/code/wxBot/voice_baidu/tts.mp3')

	print 'ok'

    def get_text_by_wav(self, msg_base64, msg_len):
	print self.access_token
	url = "http://vop.baidu.com/server_api"
	body = {'format': 'wav', 'rate': 8000, 'channel':1, 'cuid': 'xiaokele', 'token': self.access_token, 'lan': 'zh', 'speech': msg_base64, 'len':msg_len}
	r = requests.post(url, data=json.dumps(body))

	print r.text

    def mp3_2_wav(self):
	sound = AudioSegment.from_mp3("voice_baidu/tts.mp3")
	sound.export("voice_baidu/tts.wav", format="wav") 

    def test(self):
	#sound = AudioSegment.from_mp3("temp/voice_7282711500764964372.mp3")
	#sound.export("temp/voice_7282711500764964372.wav", format="wav")
	fsock = open("temp/voice_7282711500764964372.wav", "r")
	msg = fsock.read();
	fsock.close()
	msg_len = len(msg)
	msg_base64 = base64.b64encode(msg)
	# 调用百度接口识别声音
	self.get_text_by_wav(msg_base64, msg_len)

def main():
	bd = Baidu()
	fsock = open("voice_baidu/msg.txt", "r")
	msg = fsock.read();
	fsock.close()
	#msg = '媳妇儿真漂亮';
	bd.get_mp3(msg)
	bd.mp3_2_wav()
	bd.test()


if __name__ == '__main__':
    main()

