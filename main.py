from bs4 import BeautifulSoup
import requests, smtplib, ssl, subprocess
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

login_data = {
	"j_username":config.peka_login_data["username"],
	"j_password":config.peka_login_data["password"]
}

with requests.Session() as s:
	url = "https://www.peka.poznan.pl/SOP/j_spring_security_check"
	r = s.post(url, data=login_data)
	soup = BeautifulSoup(r.content, "html.parser")

	account_info = str(soup.find_all("td",attrs={"class":"col-2","colspan":"3"})[1])
	start = account_info.find("Kwota:")
	end = account_info.find("zł")
	money_left = account_info[start+6:end].replace("\t","").replace("\n","").replace("\r","")
	owner = soup.find_all("td",attrs={"class":"col-2"})[0].text.strip().replace("\t","")

if float(money_left.replace(",",".")) > 10.00:
	exit()

msg = MIMEMultipart("alternative")
msg["From"] = config.mail_data["sender_mail"]
msg["To"] = ", ".join(config.mail_recipients)
msg["Subject"] = "Peka saldo"
text = f"Pozostałe saldo: {money_left} zł"
html = f"""\
<html style="font-family: Arial; text-align: center">
	<head></head>
	<body style="border: solid; border-color: #199cfa; padding: 10px; margin: 20px;">
		<div style="margin: auto;">
			<h3>Właściciel karty</h3>
			<h2>{owner}</h2>
			<h3>Na karcie PEKA zostało</h3>
			<h2>{money_left} zł</h2>
			<a href="https://www.peka.poznan.pl/SOP/account/home.jspb?execution=e1s3" style="text-decoration: none; color: White;">
				<div style="margin: auto; background-color: #199cfa; width: 150px; height: 40px; display: flex; align-items: center; justify-content: center;">
				<b>DOŁADUJ PEKĘ</b>
				</div>
			</a>
		</div><br><br>
		<img src="https://www.peka.poznan.pl/SOP/img/logo/peka-logo.png" style="display: block; margin: auto;"><br><br>
	</body>
</html>
"""

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
msg.attach(part1)
msg.attach(part2)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.wp.pl", 465, context=context) as server:
	server.login(config.mail_data["sender_mail"],config.mail_data["sender_password"])
	server.sendmail(config.mail_data["sender_mail"],config.mail_recipients,msg.as_string())

if config.notified_user != "":
	subprocess.call(f"./notify_send.sh {config.notified_user} 'Peka saldo' 'pozostało {money_left}'", shell=True)
