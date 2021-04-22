import sys
import random
import os
import shutil

from cli import CLI
from server import UDPServer
from api import RESTServer
from utils import query_builder, udp_send_recv, query_parser, generate_random_file
from routing import RoutingTable
import configuration as cfg

class Node:

    def __init__(self):

        self.udp_ip = cfg.UdpServer['ip']
        self.udp_port = cfg.UdpServer['port']
        self.flask_ip = cfg.FlaskServer['ip']
        self.flask_port = cfg.FlaskServer['port']
        self.username = cfg.Application['name']
        self.dir =  cfg.Application['dir']
        self.bs_ip = cfg.BoostrapServer['ip']
        self.bs_port = cfg.BoostrapServer['port']

        self.routing_table = RoutingTable()
        self.cli = CLI()
        self.udp_server = UDPServer(self.udp_ip, self.udp_port)
        self.rest_server = RESTServer(self.flask_ip, self.flask_port)

    def run(self):

        # generate random files to be shared
        self.generate_files(random.randint(2, 5))

        self.reg_in_bs()
        self.connect_to_network()

        # starting udp server in a new process
        self.udp_server.run()

        # starting rest server in a new process
        self.rest_server.run()

        # starting cli in the main process
        self.cli.run()

        self.udp_server.terminate()
        self.rest_server.terminate()

        self.unreg_from_bs()
        self.disconnect_from_network()
        shutil.rmtree(self.dir)

    def reg_in_bs(self):

        query = query_builder("REG", data=[self.udp_ip, self.udp_port, self.username])
        data = udp_send_recv(self.bs_ip, self.bs_port, query)
        
        try:
            res_type, data = query_parser(data)
        except Exception as e:
            print("Error:", str(e))
            sys.exit("Exiting, Couldn't connect to BS")
        else:
            if res_type == "REGOK":
                for i in range(0, len(data), 2):
                    self.routing_table.add(data[i], data[i + 1])
            else:
                print("Error: Invalid response from BS")
                sys.exit("Exiting, Couldn't connect to BS")

    def unreg_from_bs(self):
        query = query_builder("UNREG", data=[self.udp_ip, self.udp_port, self.username])
        res = udp_send_recv(self.bs_ip, self.bs_port, query)
        try:
            res_type, res = query_parser(res)
        except Exception as e:
            pass

    def connect_to_network(self):
        for ip,port in self.routing_table.get():
            query = query_builder("JOIN", data=[self.udp_ip, self.udp_port])
            data = udp_send_recv(ip, port, query)
            try:
                res_type, data = query_parser(data)
            except Exception as e:
                print("Error:", str(e))
                self.routing_table.remove((ip, port))
            else: 
                if res_type == "JOINOK":
                    pass
                   

    def disconnect_from_network(self):
        for ip,port in self.routing_table.get():
            query = query_builder("LEAVE", data=[self.udp_ip, self.udp_port])
            data = udp_send_recv(ip, port, query)
            try:
                res_type, data = query_parser(data)
            except Exception as e:
                print("Error:", str(e))
            else: 
                if res_type == "LEAVEOK":
                    pass
    
    def generate_files(self, num_files):
        if os.path.isdir(self.dir):
            print("path already exist")
        else:
            os.mkdir(self.dir)
            f = open(f"{self.dir}/film_details.txt", "w")
            f.close()


        file_names = []
        with open("File Names.txt", 'r') as in_file:
            for line in in_file:
                file_names.append(line.strip())
        random.shuffle(file_names)

        for i in range(num_files):
            generate_random_file(self.dir, file_names[i], random.randint(2, 10))

if __name__ == "__main__":
    args = sys.argv[1:]
    cfg.UdpServer['port'] = args[0]
    cfg.FlaskServer['port'] = args[1]
    cfg.Application['name'] = args[2]
    cfg.Application['dir'] = f"data/{args[2]}"

    node = Node()
    node_data = node.run()