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

    def mp3_2_wav(self):
	sound = AudioSegment.from_mp3("voice_baidu/tts.mp3")
	sound.export("voice_baidu/tts.wav", format="wav")

    def test(self):
	fsock = open("voice_baidu/tts.mp3",'rb')
	data=fsock.read()
	fp.close()

	#主要部分
	aud=io.BytesIO(data)
	sound=AudioSegment.from_file(aud,format='mp3')
	raw_data = sound._data

	#写入到文件，验证结果是否正确。
	l=len(raw_data)
	f=wave.open("voice_baidu/tts.wav",'wb')
	f.setnchannels(1)
	f.setsampwidth(2)
	f.setframerate(16000)
	f.setnframes(l)
	f.writeframes(raw_data)
	f.close()

def main():
	bd = Baidu()
	fsock = open("voice_baidu/msg.txt", "r")
	msg = fsock.read();
	fsock.close()
	#msg = '媳妇儿真漂亮';
	bd.get_mp3(msg)
	bd.mp3_2_wav()


if __name__ == '__main__':
    main()

