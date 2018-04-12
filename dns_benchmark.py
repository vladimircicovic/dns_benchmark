#!/usr/bin/python
import dns.resolver
import dns.query
import sys

if len(sys.argv) < 2:
    sys.exit('Usage: python %s dns_list.txt' % sys.argv[0])

dns_list = None
with open(sys.argv[1]) as f:
     dns_list = f.readlines()

min_response = 9999999
min_response_server = ""

for dns_server in dns_list:
    dns_server = str(dns_server).strip('\n')
    resolver = dns.resolver.Resolver()
    resolver.timeout = 1
    resolver.lifetime = 1
    resolver.nameservers=[dns_server]
    try:
        answer = resolver.query("www.gmail.com")
    except Exception:
        print("Dns ",dns_server," does not response")
        continue
    print(dns_server,int(answer.response.time*1000),"ms")
    if min_response > int(answer.response.time*1000):
        min_response = int(answer.response.time*1000)
        min_response_server = dns_server

print("Fast response: ",min_response_server," with ", min_response, " ms")
