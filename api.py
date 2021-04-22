import sys
import logging
from flask import Flask, Response, request, send_file, abort
from multiprocessing import Process
import configuration as cfg
from os import path

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# return the requested file
class EndpointAction(object):
    def __init__(self,  dir):
        self.dir = dir

    def __call__(self, file):
        file = file.replace("-", " ")
        if path.exists(self.dir+"/"+file):
            return send_file(self.dir+"/"+file)
        else:
            abort(404)


class RESTServer(object):
    app = None

    def __init__(self, ip, port, endpoint='/<file>', endpoint_name='download file endpoint'):
        self.ip = ip
        self.port = int(port)
        self.dir = cfg.Application['dir']
        self.app = Flask("file-server")
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(self.dir))
        self.server_process = Process(target=self.async_run)

    # start the flask server on separate thread
    def async_run(self):
        self.app.run(host = self.ip, port = self.port)

    def run(self):
        self.server_process.start()

    def terminate(self):
        self.server_process.terminate()
