# PEKA SCRAPER

Program scrapuje stronę [peka.poznan.pl](https://peka.poznan.pl) sprawdzając ile punktów na koncie pozostało, jeśli saldo jest mniejsze niż 10, program wysyła maila do odbiorców podanych w pliku config.

### Example config

```
peka_login_data = {
	'username':'',
	'password':''
}

mail_data = {
	'sender_mail':'',
	'sender_password':''
}

mail_recipients = ['']

notified_user = ''
```

autor: Tomasz Łakomy

![](https://www.peka.poznan.pl/SOP/img/logo/peka-logo.png)
