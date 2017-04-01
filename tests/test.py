from smtplib import SMTP

host = 'localhost'
port = 8025

client = SMTP(host, port)
client.sendmail('aperson@example.com', ['bperson@example.com'], """\
From: Anne Person <anne@example.com>
To: Bart Person <bart@example.com>
Subject: A test
Message-ID: <ant>

Hi Bart, this is Anne. This will fail
""")
client.sendmail('aperson@example.com', ['abc@a.com'], """\
From: Anne Person <anne@example.com>
To: abc@a.com
Subject: A test
Message-ID: <ant>

Hi Bart, this is Anne. This will pass
""")
client.quit()
