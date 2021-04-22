import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

Application = {
    "name" : "node1",
    "dir" : "data/node1"
}

BoostrapServer = {
    "ip" : "127.0.0.1",
    "port" : "55555"
}

UdpServer = {
    "ip" : ip_address,
    "port" : "5555"
}

FlaskServer = {
    "ip" : ip_address,
    "port" : "5000"
}
