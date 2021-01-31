from tungsten.logger import Logger
from tungsten.html_status_codes import status_codes
from tungsten.settings import settings

from time import strftime, gmtime

import os
import mimetypes


logger = Logger()

# Request class -- stores a request, but parsed and chopped up
class Request:
    req_line = ""
    http_method = ""
    http_version = ""
    uri = ""
    headers = {}
    body = ""
    def parse_req_line(self):
        print("   -> " + self.req_line)
        r_spl = self.req_line.split(' ')
        if(len(r_spl) < 3):
            raise Exception("empty request line")
        self.http_method = r_spl[0]
        self.uri = r_spl[1]
        self.http_version = r_spl[2]

# stores a response and is also connected to a request
class Response:
    req = Request()

    def __init__(self, req):
        self.req = req

    # serialize headers into a string
    def headify_ext(self, mimetype, length):
        headers = "Date: "
        headers += strftime("%Y-%m-%d %H:%M:%S GMT", gmtime()) + "\r\n"
        headers += "Content-Type: " + mimetype + "\r\n"
        headers += "Content-Length: " + length + "\r\n"
        headers += "Server: Tungsten\r\n\r\n"
        return headers

    def headify(self):
        headers = "Date: "
        headers += strftime("%Y-%m-%d %H:%M:%S GMT", gmtime()) + "\r\n"
        headers += "Content-Type: text/html;charset=UTF-8\r\n"
        headers += "Server: Tungsten\r\n\r\n"
        return headers

    # concatinate headers, status line and the body and return
    def serialize(self, status):
        r_line = self.req.http_version + " " + status_codes[status] + "\r\n"
        return (r_line + self.headify()).encode('utf-8')

    def serialize_ext(self, status, body):
        r_line = self.req.http_version + " " + status_codes[status] + "\r\n"
        return (r_line + self.headify()).encode('utf-8') + body

    def serialize_ext_2(self, status, body, mime, length):
        r_line = self.req.http_version + " " + status_codes[status] + "\r\n"
        return (r_line + self.headify_ext(mime, length)).encode('utf-8') + body

# main class, handles the main http stuff
class HTTPHandler:

    # parses headers from the request string into a dictionary
    def parse_request(self, req):
        header_line = ["", ""]
        selector = 0
        r = Request()
        for i in range(0, len(req)):
            if(req[i] == '\r' and req[i+1] == '\n'):
                r.req_line = req[:i]
                req = req[i+2:]
                i+=1
                break
            
        i = 0
        while i < len(req):
            if(req[i] == '\r' and req[i+1] == '\n'):
                i+=2
                if(req[i] == '\r' and req[i+1] == '\n'):
                    i+=1
                    break
                selector = 0
                r.headers[header_line[0]] = header_line[1]
                header_line = ['', '']
                continue

            if(req[i] == ':'):
                i+=2
                selector = 1
                continue
            header_line[selector] += req[i]
            i+=1
        req = req[i+2:]
        r.body = req[i:]
        return r

    # handles a GET request
    # reads the file from the request line's URI
    def request_GET(self, res):
        file = settings["serve_folder"] + res.req.uri
        if(res.req.uri == '/'):
            file += settings["home_file"]
        logger.log("   -> " + file + " [" + res.req.uri + "]")
        try:
            with open(file, "rb") as f:
                body = f.read()
            size = len(body)
            mime = mimetypes.guess_type(file)[0]
            logger.log("   -> " + mime + " " + str(size))
        except FileNotFoundError:
            with open("tungsten/resources/404.html", "rb") as f:
                body = f.read()
            return res.serialize_ext("404", body)

        return res.serialize_ext_2("200", body, mime, str(size))

    # handles a HEAD request
    # reads the file from the request line's URI
    # but DOES NOT send the file with the response: only sends the headers and the status
    def request_HEAD(self, res):
        file = settings["serve_folder"] + res.req.uri
        if(res.req.uri == '/'):
            file += settings["home_file"]
        logger.log("   -> " + file + " [" + res.req.uri + "]")
        try:
            with open(file, "rb") as f:
                body = f.read()
            size = len(body)
            mime = mimetypes.guess_type(file)[0]
            logger.log("   -> " + mime + " " + str(size))
        except FileNotFoundError:
            with open("tungsten/resources/404.html", "rb") as f:
                body = f.read()
            return res.serialize_ext("404", body)

        return res.serialize_ext_2("200", b'', mime, str(size))


    # tungsten is a simple server
    # this was made for educational purposes only, to learn how stuff works
    # tungsten only supports HTTP GET and HEAD for now.
    # the rest return a HTTP 501 Not Implemented response
    def handle_501(self, res):
        return res.serialize("501")
