from smtplib import SMTP

host='localhost'
port=8025

client = SMTP(host, port)
client.sendmail('aperson@example.com', ['bperson@example.com'], """\
From: Anne Person <anne@example.com>
To: Bart Person <bart@example.com>
Subject: A test
Message-ID: <ant>

Hi Bart, this is Anne.
""")
client.quit()
