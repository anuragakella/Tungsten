from tungsten.request_handler import HTTPHandler, Response
import tungsten.socket_handler as socket_handler
import tungsten.settings as s

# start the server
# this method connects all of the classes / files
def start(self):
    s.parse_settings()

    # listen for connections in a loop
    # get a request, serve and disconnect
    # wait for the next connection
    l = socket_handler.connect()
    while True:
        try:
            request, conn, _ = socket_handler.listen(l)
            http_handler = HTTPHandler()
            r = http_handler.parse_request(request)
            r.parse_req_line()
            try:
                processor = getattr(http_handler, "request_{0}".format(r.http_method))
            except AttributeError:
                processor = http_handler.handle_501
            response = processor(Response(r))
            socket_handler.respond(response, conn)
        except Exception as e:
            print(e)