#!/bin/env python
# -*- encoding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

FROM = "from@domain.com"
def send_email(from_address, to_address, body, file_name, file_obj):
	try:
		
		msg = MIMEMultipart()
		
		me = from_address
		to = to_address
		msg["From"] = me
		msg["To"] = to
		msg["Subject"] = u"OpenVPN配置及密钥"

		text = MIMEText(_text = body, _subtype = "plain", _charset="utf-8")
		msg.attach(text)
		
		attachment = MIMEBase("application", "octet-stream")
		attachment.set_payload(file_obj.read())
		encoders.encode_base64(attachment)
		attachment.add_header("Content-Disposition", "attachment", filename=file_name)
		msg.attach(attachment)
		try:	
			server = smtplib.SMTP_SSL("smtp.domain.com", 465, "domain.com")
			print("login ...")
			server.login("user", "pass")
			print("sending ...")
			server.sendmail(me, to, msg.as_string())
			server.quit()
		except Exception as e:
			print("Failed to send email:")
			print(e)
	except Exception as e:
		print("Faile to prepare email body")	
		print(e)

if "__main__" == __name__:
	import sys
	import os
	if len(sys.argv) < 3:
		print("usage: %s to_address file" % os.path.basename(sys.argv[0]))
		sys.exit(1)
	to_address = sys.argv[1]
	file_name = sys.argv[2]
	user, domain = to_address.split("@")
	body = u"""
	Hi user, 
		各平台使用的客户端：
		Windows: http://swupdate.openvpn.net/privatetunnel/client/privatetunnel-win-2.3.exe
		MacOSX: https://code.google.com/p/tunnelblick/wiki/DownloadsEntry#Tunnelblick_Stable_Release
		Android: https://play.google.com/store/apps/details?id=net.openvpn.privatetunnel
		iOS: https://itunes.apple.com/us/app/openvpn-connect/id590379981
	""" 
	with open(file_name) as f:
		send_email(FROM, to_address, body, file_name, f)
