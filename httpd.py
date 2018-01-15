#!/usr/bin/python
import os
import cgi
import L298N_car3
import ConfigParser
import json 
import requests
import urllib
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
from requests.exceptions import ConnectionError, ReadTimeout
from urllib import quote

PORT_NUMBER = 8080


#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        #print self.path
        if self.path=="/":
            self.path="/httpd.html"

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".mp3"):
                mimetype='audio/mpeg3'
                sendReply = True
            if self.path.endswith(".txt"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".png"):
                mimetype='image/png'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path) 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
        if self.path=="/command":
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })

            command = form["command"].value
            time_span = 0.3
            time_span_min = 0.1

            if command == "forward":
                L298N_car3.go(time_span)
                #print "command is: %s" % command
            if command == "backward":
                L298N_car3.back(time_span)
                #print "command is: %s" % command
            if command == "left":
                L298N_car3.left(time_span)
                #print "command is: %s" % command
            if command == "right":
                L298N_car3.right(time_span)
                #print "command is: %s" % command

            self.send_response(200)
            self.end_headers()
            #self.wfile.write("Let's %s !" % command)
            return

        if self.path=="/img_name":
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })
            name = form["name"].value

            fsock = open("img_control.txt", "w")
            fsock.write(name)
            fsock.close()

            self.send_response(200)
            self.end_headers()
            #self.wfile.write("Let's %s !" % command)
            return

        if self.path=="/person":
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })
            tag = form["tag"].value
            tagobj = json.loads(tag)
            #msg = tagobj['name'] + tagobj['description']
            msg = tagobj['name'].encode('UTF-8') + tagobj['description'].encode('UTF-8')

            cf = ConfigParser.ConfigParser()
            cf.read('conf_baidu.ini')
            access_token = cf.get('main', 'access_token')

            # baidu mp3
            url = "http://tsn.baidu.com/text2audio"
            msg_encode = quote(msg)
            body = {'tex': msg_encode, 'lan': 'zh', 'cuid': 'xiaokele', 'ctp': '1', 'tok': access_token}
            r = requests.get(url, params=body)

            #write this file
            fsock = open("voice_baidu/person.mp3", "w")
            fsock.write(r.content);
            fsock.close()

            os.system('mpg123 /home/pi/code/wxBot/voice_baidu/person.mp3')

            fsock = open("person_tag.txt", "w")
            fsock.write(msg)
            fsock.close()

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', "*")
            self.end_headers()
            self.wfile.write("write ok !")
            return

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()

