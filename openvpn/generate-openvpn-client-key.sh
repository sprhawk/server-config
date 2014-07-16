#!/bin/sh
if [ $# -eq 0 ]; then
	echo "usage: $(basename $0) client-name";
	exit 1;
fi

CLIENT=$1
CONFIG_FILE=nutspace.ovpn
EASY_RSA=/etc/openvpn/easy-rsa
sudo sh -c "source $EASY_RSA/vars 
	export KEY_EMAIL=$CLIENT
	export KEY_NAME=$CLIENT
	$EASY_RSA/pkitool $CLIENT 
	cp $EASY_RSA/keys/$CLIENT.{key,crt} .
 	chown cloud-user:cloud-user $CLIENT.{key,crt}"

echo "Generating $CLIENT.ovpn"
sed -e "{s/^key client.key/key $CLIENT.key/
s/^cert client.crt/cert $CLIENT.crt/}" client.conf > $CONFIG_FILE

zip "$CLIENT.zip" "$CLIENT.{key,crt}" ca.crt $CONFIG_FILE

rm -f $CLIENT.{key,crt} $CONFIG_FILE

