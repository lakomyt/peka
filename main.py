from bs4 import BeautifulSoup
import requests
import config

login = config.username
password = config.password

login_data = {
	'j_username':str(login),
	'j_password':str(password)
}

with requests.Session() as s:
	url = 'https://www.peka.poznan.pl/SOP/j_spring_security_check'
	r = s.post(url, data=login_data)
	soup = BeautifulSoup(r.content, 'html.parser')
