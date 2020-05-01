#!/usr/bin/python
import dns.resolver
import dns.query
import sys
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    sys.exit('Usage: python %s dns_list.txt' % sys.argv[0])

dns_list = None
with open(sys.argv[1]) as f:
     dns_list = f.readlines()

min_response = 9999999
min_response_server = ""

times = []
servers = []


for dns_server in dns_list:
    dns_server = str(dns_server).strip('\n')
    resolver = dns.resolver.Resolver()
    resolver.timeout = 1
    resolver.lifetime = 1
    resolver.nameservers=[dns_server]
    try:
        answer = resolver.query("www.github.com")
    except Exception:
        print("Dns ",dns_server," does not response")
        continue

    response_ms = int(answer.response.time * 1000)
    print(dns_server, response_ms, "ms")
    if min_response > response_ms:
        min_response = response_ms
        min_response_server = dns_server

    times.append(response_ms)
    servers.append(dns_server)

print("Fast response: ", min_response_server, " with ", min_response, " ms")

times, servers = zip(*sorted(zip(times, servers)))
plt.barh(servers, times)
plt.show()
