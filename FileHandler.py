import os
import random
import time
from utils import query_builder,udp_send_recv
import requests
import configuration as cfg
from tqdm import tqdm
from exceptions import ResourceNotFoundError

def show_files():
    file_names = []
    dir = cfg.Application['dir']
    if os.path.exists(dir):
        available_files = os.listdir(dir)
        for file in available_files:
            if file=="film_details.txt":
                continue
            file_names.append(file)
    return file_names

def downloadFile(filename):
    dir = cfg.Application['dir']
    f = open(f"{dir}/film_details.txt")
    for line in f.readlines():
        entry = line.split("|")
        if filename==entry[0]:
            filename = filename.replace(" ","-")
            url = 'http://' + entry[1] + ":" + entry[2][:-1] + "/" + filename
            try:
                r = requests.get(url, allow_redirects=True, stream=True)
                if r.status_code == 404:
                    raise ResourceNotFoundError
                total = int(r.headers.get('content-length', 0))
                fname = filename.replace("-"," ")
                fname = f"{cfg.Application['dir']}/{fname}"
                with open(fname, 'wb') as file, tqdm(desc=fname, total=total, unit='iB', unit_scale=True,unit_divisor=1024,) as bar:
                    for data in r.iter_content(chunk_size=1024):
                        size = file.write(data)
                        bar.update(size)
                print(">>>>> Successfully Downloaed File : " + filename)
                return ""
            except:
                continue

    print("!!!! The Requested Resource Does Not Exist !!!!!")

def search_file(filename, local_search = False):
    file_name = filename.lower().split(" ")
    file_found = False
    file_names = []
    dir = cfg.Application['dir']
    if os.path.exists(dir):
        available_files = os.listdir(dir)
        for file in available_files:
            file_tokens = file.lower().split(" ")

            for token in file_name:
                if token not in file_tokens:
                    break
            else:
                file_found = True
                file_names.append(file)
    
    if local_search:
        if file_found:
            print(">>>>> File Found in the Local Repository")
        else:
            dir = cfg.Application['dir']
            f = open(f"{dir}/film_details.txt", "w")
            f.truncate()
            f.close()
            ip = cfg.UdpServer['ip']
            port = cfg.UdpServer['port']
            request = query_builder("SER", [ip,port, filename, 3])  #NO of HOPS = 3
            return udp_send_recv(ip, port, request, recieve=False)
    else:
        return file_found, ",".join(file_names)
