'''
Created on Aug 14, 2016

@author: sam
'''
from oauthlib.common import urldecode
APP_NAME = __name__

import platform

if platform.system() != 'Windows':
    from pydbus import SessionBus
    import notify2 as notif

import SimpleHTTPServer as http
import SocketServer as serv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse
import urllib
import time,datetime
import os,sys
import cStringIO

import ntfy

#if "ntfy" in sys.modules:
#    import ntfy


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        curdir = os.getcwd()
        sep = os.sep

        try:
            print self.command, self.path

            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in urllib.unquote_plus(query).split("&"))

#            query_components = urllib.unquote(query)

            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

#            self.wfile.write("<PRE>")
            self.wfile.write(query_components)
            self.wfile.write("\n")

            self.wfile.close()

            show_message(query_components['title'], query_components['msg'])

        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

        self.wfile.close()
#        self.finish()

def show_message(title,message):
    ntfy_show_message(title, message)

def notif_show_message(title,message):
    notif.init(APP_NAME)

    new_msg = notif.Notification(title,message)
    new_msg.timeout = 1
    new_msg.show()
    new_msg.close()

def pydbus_show_message(title,message):
    bus = SessionBus()
    notifications = bus.get('.Notifications')
    notifications.Notify('test', 0, 'dialog-information', title,message, [], {}, 1000)

def ntfy_show_message(title,message):
    ntfy.notify(title,message)


def main():
    handler = MyHandler

    port = int(sys.argv[1])

    httpd = serv.TCPServer(("", port), handler)

    print 'Listening at', port
    try:
        httpd.serve_forever()
    except:
        httpd.shutdown()
    #show_message("test!","A new message")

if __name__ == '__main__':
    main()
