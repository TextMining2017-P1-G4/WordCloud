from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import json
import urllib
import wordcloud
import re

PORT_NUMBER = 6466

#This class will handles any incoming request from the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"
        
        try:
            #Check the file extension required and
            #set the right mime type

            if self.path.endswith(".html"):
                mimetype='text/html'
                staticFiles = True
            elif self.path.endswith(".jpg"):
                mimetype='image/jpg'
                staticFiles = True
            elif self.path.endswith(".gif"):
                mimetype='image/gif'
                staticFiles = True
            elif self.path.endswith(".js"):
                mimetype='application/javascript'
                staticFiles = True
            elif self.path.endswith(".css"):
                mimetype='text/css'
                staticFiles = True
            else:
                mimetype='text/html'
                staticFiles = False

            if staticFiles == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path) 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            else:
                if self.path.startswith('/get_word_cloud?'):
                    pat = re.compile(r'/get_word_cloud\?' + \
                          r'keyword=(?P<keyword>.+)&select=(?P<select>.+)')
                    mat = pat.match(self.path)
                    keyword = mat.group('keyword')
                    keyword = urllib.unquote(keyword).decode('utf-8')
                    select = mat.group('select')

                    wc = wordcloud.word_could(keyword, select)
                    wc = [[ele[0].encode('utf-8'), ele[1]] for ele in wc]
                    wc = json.dumps(wc, ensure_ascii=False, encoding='utf-8')

                    mimetype='text/html'
                    self.send_response(200)
                    self.send_header('Content-type',mimetype)
                    self.end_headers()
                    self.wfile.write(wc)
                    return


        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
        

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
