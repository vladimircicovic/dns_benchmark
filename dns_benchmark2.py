#!/usr/bin/python
from multiprocessing import Process
import multiprocessing
import dns.resolver
import dns.query
import sys
MAX_PROCCESS = 4
MAX_TIMEOUT = 0.055
if len(sys.argv) < 2:
    sys.exit('Usage: python %s dns_list.txt' % sys.argv[0])

#dns_list = ["1.1.1.1","8.8.8.8","9.9.9.9","147.91.249.61"]
dns_list = None
with open(sys.argv[1]) as f:
     dns_list = f.readlines()

def dns_test_speed(num_process,dns_list,return_dict):
    min_response = 9999999
    min_response_server = ""

    for dns_server in dns_list:
        dns_server = str(dns_server).strip('\n')
        resolver = dns.resolver.Resolver()
        resolver.timeout = MAX_TIMEOUT
        resolver.lifetime = MAX_TIMEOUT
        resolver.nameservers=[dns_server]
        try:
           answer = resolver.query("www.gmail.com")
        except Exception:
           #print("Dns ",dns_server," does not response")
           continue
        print(dns_server,int(answer.response.time*1000),"ms")
        if min_response > int(answer.response.time*1000):
           min_response = int(answer.response.time*1000)
           min_response_server = dns_server
    #print(min_response," ",min_response_server)
    if min_response != 9999999:
       return_dict[num_process] = (min_response,min_response_server)

manager = multiprocessing.Manager()
return_dict = manager.dict()

jobs = []
for i in range(MAX_PROCCESS):
    p = multiprocessing.Process(target=dns_test_speed(i,dns_list[i::MAX_PROCCESS],return_dict))
    jobs.append(p)
    p.start()

for proc in jobs:
    proc.join()
print(return_dict.values())

