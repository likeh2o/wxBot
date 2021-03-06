#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import ConfigParser
import json
from urllib import quote
from pydub import AudioSegment ###需要安装pydub、ffmpeg
import base64
import L298N_car3

class TulingWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        print(sys.getdefaultencoding())

        self.tuling_key = ""
        self.robot_switch = True
        self.access_token = ""

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')
            self.tuling_key = cf.get('main', 'key')
            cf.read('conf_baidu.ini')
            self.access_token = cf.get('main', 'access_token')
        except Exception:
            pass
        print 'tuling_key:', self.tuling_key

    def get_baidu_mp3(self, msg):
        url = "http://tsn.baidu.com/text2audio"

        fsock = open("voice_baidu/msg.txt", "w")
        fsock.write(msg);
        fsock.close()
        
        fsock = open("voice_baidu/msg.txt", "r")
        msg_content = fsock.read();
        fsock.close()

        msg_encode = quote(msg_content)
        print msg_encode
        body = {'tex': msg_encode, 'lan': 'zh', 'cuid': 'xiaokele', 'ctp': '1', 'tok': self.access_token}
        r = requests.get(url, params=body)

        #write this file
        fsock = open("voice_baidu/tts.mp3", "w")
        fsock.write(r.content);
        fsock.close()

        print 'baidu mp3 ok'
        
    def car_go(self, msg):
        command_go = "开车"
        command_back = "倒车"
        command_left = "左转弯"
        command_right = "右转弯"
        if msg.replace("，", "") == command_go:
                L298N_car3.go(5)
        if msg.replace("，", "") == command_back:
                L298N_car3.back(5)
        if msg.replace("，", "") == command_left:
                L298N_car3.left(1)
        if msg.replace("，", "") == command_right:
                L298N_car3.right(1)

    def tuling_auto_reply(self, uid, msg, msg_type = 'text'):
        if self.tuling_key:
            url = "http://www.tuling123.com/openapi/api"
            user_id = uid.replace('@', '')[:30]
            body = {'key': self.tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
            r = requests.post(url, data=body)
            respond = json.loads(r.text)
            result = ''
            if respond['code'] == 100000:
                result = respond['text'].replace('<br>', '  ')
                if msg_type == 'voice':
                        # 获取mp3 下面一行会转码，之后没法urlencode
                        self.get_baidu_mp3(result)
                        result = result.replace(u'\xa0', u' ')
                        # 播放音乐
                        os.system('mpg123 '+'voice_baidu/tts.mp3')
            elif respond['code'] == 200000:
                result = respond['url']
            elif respond['code'] == 302000:
                for k in respond['list']:
                    result = result + u"【" + k['source'] + u"】 " +\
                        k['article'] + "\t" + k['detailurl'] + "\n"
            else:
                result = respond['text'].replace('<br>', '  ')
                result = result.replace(u'\xa0', u' ')

            print '    ROBOT:', result
            return result
        else:
            return u"知道啦"

    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
        start_cmd = [u'出来', u'启动', u'工作']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已关闭！', msg['to_user_id'])
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', msg['to_user_id'])

    def get_text_by_wav(self, msg_base64, msg_len):
        url = "http://vop.baidu.com/server_api"
        body = {'format': 'wav', 'rate': 8000, 'channel':1, 'cuid': 'xiaokele', 'token': self.access_token, 'lan': 'zh', 'speech': msg_base64, 'len':msg_len}
        r = requests.post(url, data=json.dumps(body))
        rj = json.loads(r.text)

        return rj['result'][0]

    def handle_voice(self, msg):
        sound = AudioSegment.from_mp3(self.voice_path)
        sound.export(self.voice_path + ".wav", format="wav")
        fsock = open(self.voice_path + ".wav", "r")
        print self.voice_path + ".txt"
        msg_mp3 = fsock.read();
        fsock.close()
        msg_len = len(msg_mp3)
        msg_base64 = base64.b64encode(msg_mp3)
        # 调用百度接口识别声音
        msg_baidu = self.get_text_by_wav(msg_base64, msg_len)

        #write this file
        fsock = open(self.voice_path + ".txt", "w")
        fsock.write(msg_baidu)
        fsock.close()

        print msg_baidu
        self.car_go(msg_baidu)

        msg_tuling = self.tuling_auto_reply(msg['user']['id'], msg_baidu, 'voice')

    def handle_msg_all(self, msg):
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            self.auto_switch(msg)
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from contact
            self.car_go(msg['content']['data'])
            self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], msg['content']['data']), msg['user']['id'])
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 4:  # voice 
            self.handle_voice(msg)
        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
            if 'detail' in msg['content']:
                my_names = self.get_group_member_name(msg['user']['id'], self.my_account['UserName'])
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']

                is_at_me = False
                for detail in msg['content']['detail']:
                    if detail['type'] == 'at':
                        for k in my_names:
                            if my_names[k] and my_names[k] == detail['value']:
                                is_at_me = True
                                break
                if is_at_me:
                    src_name = msg['content']['user']['name']
                    #reply = '@' + src_name + ' '
                    #怎么at别人呢？
                    reply = '@' + src_name + '\u2005'.decode('unicode_escape')
                    if msg['content']['type'] == 0:  # text message
                        reply += self.tuling_auto_reply(msg['content']['user']['id'], msg['content']['desc'])
                    else:
                        reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                    self.send_msg_by_uid(reply, msg['user']['id'])


def main():
    bot = TulingWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'

    bot.run()


if __name__ == '__main__':
    main()

