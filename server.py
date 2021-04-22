import socket
import time
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor
import logging
logging.basicConfig(level=logging.INFO)

from routing import RoutingTable
from utils import query_builder, udp_send_recv
from FileHandler import search_file 
from threading import Lock

import constants as CONST

import configuration as cfg


class UDPServer:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.ip, self.port))
        self.server_process = Process(target=self._start)
        self.routing_table = RoutingTable()
        self.lock = Lock()
        self.name = cfg.Application['name']

    def run(self):
        self.server_process.start()

    def terminate(self):
        self.server_process.terminate()

    def _start(self):
        executor = ThreadPoolExecutor(max_workers=3)
        while True:
            msg, addr = self.server.recvfrom(CONST.BUFFER_SIZE)
            executor.submit(self._process_request, msg=msg, addr=addr)

    def _process_request(self, msg, addr):
        msg = msg.decode("utf-8")
        tokens = msg.split()

        if tokens[1] == "JOIN":
            logging.info("Request recieved to Join network from node%s to %s", tokens[3][-1], self.name)
            self.routing_table.add(tokens[2], tokens[3])
            response = query_builder("JOINOK", ["0"])
            udp_send_recv(addr[0], addr[1], response, recieve=False)

        elif tokens[1] == "LEAVE":
            logging.info("Request recieved to leave network from node%s to %s", tokens[3][-1], self.name)
            for node in self.routing_table.get():
                if node[1] == tokens[3]:
                    self.routing_table.remove(node)
                    break
            response = query_builder("LEAVEOK", ["0"])
            udp_send_recv(addr[0], addr[1], response, recieve=False)

        elif tokens[1] == "SER":
            hops = int(tokens[5])
            if hops==3:
                logging.info("Request recieved to start search film %s from node%s to %s at time %s", tokens[4], tokens[3][-1], self.name, str(time.time()))
                #logging.info("%s Started %s at time %s", self.name, tokens[4], str(time.time()))
            else:
                logging.info("Request recieved to search film %s from node%s to %s", tokens[4], tokens[3][-1], self.name)
                #logging.info("%s Requested %s", self.name, tokens[4])
            files_found, file_names = search_file(tokens[4])

            if files_found > 0:
                logging.info("Request resolved for film %s by %s after hop count of %s", tokens[4],  self.name, 3-hops)
                response = query_builder("SEROK", [files_found, cfg.FlaskServer['ip'], cfg.FlaskServer['port'], hops, file_names])
                udp_send_recv(tokens[2], tokens[3], response, recieve=False)

            elif hops > 0:
                request = query_builder("SER", [tokens[2], tokens[3], tokens[4], hops-1])
                for node in self.routing_table.get():
                    udp_send_recv(node[0], node[1], request, recieve=False)
                    logging.info("Request for the film %s is Forwarded by %s to node%s", tokens[4], self.name, node[1][-1])
        
        elif tokens[1] == "SEROK":
            dir = cfg.Application['dir'] 
            films = " ".join(tokens[6:]).strip()
            logging.info("Response got for film %s by node%s to %s at time %s", films, tokens[4][-1], self.name, str(time.time()))

            self.lock.acquire()
            f = open(f"{dir}/film_details.txt", "a")
            file1 = open(f"{dir}/film_details.txt")

            for film in films.split(','):
                found = False
                for line in file1.readlines():
                    if film in line:
                        found = True
                if not found:
                    print(f"\t* {film}")
                    f.write(f"{film}|{tokens[3]}|{tokens[4]}\n")
                    
            f.close()
            file1.close()
            self.lock.release()