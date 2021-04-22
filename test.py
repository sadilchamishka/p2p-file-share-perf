import random
import os
import time
import sys

args = sys.argv[1:]
nodeId = int(args[0])
query = args[1]
port = 5500 + nodeId

search_query = f"00XX SER 127.0.1.1 {port} {query} 3"
command = f"echo '{search_query}' | nc -u 127.0.1.1 {port} &"

os.system(command)
time.sleep(5)

logs = open("demo.log").readlines()
os.system("kill -9 $(ps -aux | grep  '[n]c -u 127.0.1.1' | awk '{print $2}')")

start_time = 0
end_time = 0
no_requests = 0
no_forwards = 0
no_resolves = 0
min_hops = 3

nodes_got_messages = []

for line in logs:
    if f"to start search film {query}" in line:
        start_time = float(line.split(' ')[-1])
    
    if end_time == 0 and f"Found {query}" in line:
        end_time = float(line.split(' ')[-1])
    
    if f"to search film {query}" in line:
        no_requests+=1
        nodes_got_messages.append(line.split(' ')[-1][:-1])

    if f"for the film {query} is Forwarded by" in line:
        no_forwards+=1
    
    if f"resolved for film {query}" in line:
        no_resolves+=1
        hops = int(line.split(' ')[-1])
        if hops < min_hops:
            min_hops = hops

print("Latency ", (end_time-start_time)*1000)
print("no_requests ", no_requests)
print("no_forwards ", no_forwards)
print("no_resolves ", no_resolves)
print("min_hops ", min_hops)

for i in range(10):
    print(f"Node{i} got ",nodes_got_messages.count(f"node{i}"), " messages")
