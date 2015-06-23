__author__ = 'Zhe'


import requests, json
from yunsoo.__init__ import __data_server__

login_url = __data_server__ + "/user/login"

def get_cookie():
    r = requests.post(login_url, files={'email': ('', 'zhe@yunsu.com'),'passwd': ('', '888888')})
    return r.cookies

