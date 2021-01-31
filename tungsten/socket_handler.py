import socket
from tungsten.settings import settings
import tungsten.logger

HOST = settings["host"]
PORT = int(settings["port"])
logger = tungsten.logger.Logger()

# sockets library, handles TCP connections and accepts requests
def connect():
    # socket setup
    global HOST, PORT
    HOST = settings["host"]
    PORT = int(settings["port"])
    logger.log("Listening for connections: HOST:" + HOST + " PORT: " + str(PORT))
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind address and listen for connections
    listener.bind((HOST, PORT))
    listener.listen(1) # listen for 1 connection
    return listener

# accepts connections and returns the connection object and the requesr
def listen(listener):
    conn, addr = listener.accept()
    req = conn.recv(1024)
    r = req.decode('utf-8')
    logger.log("-> Request from " + str(addr[0]) + ":" + str(addr[1]))
    return r, conn, addr

# responds with a HTTP response (after some work in other files of course)
def respond(response, conn):
    conn.sendall(response)
    conn.close()