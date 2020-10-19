import requests
from bs4 import BeautifulSoup
import getpass
import sys

def login():
    username = input("Input email (without @binus.ac.id) : ")
    password = getpass.getpass("Input password : ")

    sess = requests.session()

    try:
        loginPage = sess.get("https://binusmaya.binus.ac.id/login",timeout=10)
    except requests.exceptions.ReadTimeout:
        print('Cannot access login page')
        sys.exit(1)
    
    usernamePrompt = BeautifulSoup(loginPage.text,'html.parser').findAll('input',attrs={'placeholder':'Username'})[0]['name']
    passwordPrompt = BeautifulSoup(loginPage.text,'html.parser').findAll('input',attrs={'placeholder':'Password'})[0]['name']
    submit = BeautifulSoup(loginPage.text,'html.parser').findAll('input',attrs={'type':'submit','value':'Login'})[0]['name']
    
    try:
        loaderSrc = BeautifulSoup(loginPage.text,'html.parser').findAll('script')[4]['src']
        loaderPage = sess.get("https://binusmaya.binus.ac.id/login/" + loaderSrc,timeout=10)
        loader = BeautifulSoup(loaderPage.text,'html.parser').findAll('input')
    except requests.exceptions.ReadTimeout:
        print('Cannot access loader page')
        sys.exit(1)
    
    data = {
        usernamePrompt : username,
        passwordPrompt : password,
        submit : 'Login',
        loader[0]['name'] : loader[0]['value'],
        loader[1]['name'] : loader[1]['value']
    }

    resp = sess.post("https://binusmaya.binus.ac.id/login/sys_login.php",data=data)

    if "binusmaya.binus.ac.id/login" in resp.url:
        print('Invalid username and / or password')
        sys.exit(1)

    cookies = ''

    return sess, 'PHPSESSID=' + sess.cookies['PHPSESSID']
