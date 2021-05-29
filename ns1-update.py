import requests
import socket
import sys
import json
import time

if len(sys.argv) < 4:
    print(f"ns1-update.py -- Usage: python3 ns1-update.py zone domain ns1key")
    sys.exit(1)

zone = sys.argv[1]
domain = sys.argv[2]
ns1key = sys.argv[3]

def curtime():
    current_time = time.strftime("%Y-%b-%d %H:%M:%S", time.localtime())
    return current_time


if zone not in domain:
    print(f"{curtime()} ERROR: host name must be domain name and contain zone name. Exiting.")
    sys.exit(1)


def main(zone, domain, ns1key):
    while True:
        real = check_ip()
        dns = check_dns(domain)
        update(real, dns, zone, domain, ns1key)
        time.sleep(10)


def check_ip():
    try:
        r = requests.get('http://ipv4.icanhazip.com', timeout=1.0)
        real = r.text.rstrip()
    except:
        print(f"{curtime()} WARNING: Unable to determine real IP address. Continuing.")
        real = "0.0.0.0"
    return real


def check_dns(domain):
    try:
        dns = socket.gethostbyname(domain)
    except:
        print(f"{curtime()} WARNING: Unable to lookup IP address of {domain}. Continuing.")
        dns = "0.0.0.0"
    return dns


def update(real, dns, zone, domain, ns1key):
    if dns == "0.0.0.0" or real == "0.0.0.0":
        return
    if str(real) == str(dns):
        print(f"{curtime()} INFO: {dns} matches {real}. No DNS update required.")
    else:
        print(f"{curtime()} INFO: {dns} does not match {real}. Updating DNS.")
        base_url="https://api.nsone.net/v1/zones/"
        url = base_url + zone + "/" + domain + "/A"
        headers = {'user-agent': 'ns1-update-py3', 'x-nsone-key': ns1key }
        payload = {"answers": [ { "answer" : [ real ] } ] }
        try:
            r = requests.post(url, headers=headers, data=json.dumps(payload))
        except:
            print(f"{curtime()} WARNING: Unable to update DNS. Continuing.")
        if r.status_code == 200:
            print(f"{curtime()} INFO: Updated DNS for {domain} to {real}.")


if __name__ == "__main__":
    main(zone, domain, ns1key)
