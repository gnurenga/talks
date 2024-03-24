"""Initilize the generator outside the function call
to avoid reset
"""

from pathlib import Path
import re

pattern_ip = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"

domains1 = ["www.cnn.com |80|443|", "*chennaipy.org", "192.168.1.12 |2000|9000|"]
domains2 = ["www.chennaipy.com |80|443|", "*chennaipy.org/home", "192.168.1.45 |2003|9004|"]


def id_generator():
    n = 0
    while True:
        n = n + 1
        yield n

def check_ip(ip):
    ip = ip.split(" ")[0]

    match = re.match(pattern_ip, ip)

    if match:
        return 1

    return 0

def check_port(domain):
    if "|" in domain:
        return 1
    else:
        return 0

def split_port(domain):
    if domain.count("|") == 2:
        return domain.split("|")[1]
    else:
        return domain.split("|")[1:]


def initialize_config_template(config):
    config["id"] =  None
    config["description"] =  None
    
def build_config(config, domains, domain_string):
    categories = {}
    id_gen = id_generator()
    _ports = []
    for value in domains:
        ports = split_port(value)
        if check_port(value):
            for port in ports:
                _id = next(id_gen)
                if check_ip(value):
                    _desc = domain_string + " IP " + port
                else:
                    _desc = domain_string + " URL " + port

                if port not in _ports:
                    _ports.append(port)
                    config["id"] = _id
                    config["description"] = _desc
                    categories[_id] = config.copy()
             
    return categories



def main():
    config = {}
    initialize_config_template(config)
    _cat1 = build_config(config, domains1, "client 1")
    _cat2 = build_config(config, domains2, "client 2")

    print(_cat1)
    print(_cat2)

main()


        
