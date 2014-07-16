if [ $# -eq 0 ]; then
	echo "$(basename $0) client-email-address";
	exit 1;
fi

CLIENT=$1
./generate-openvpn-client-key $CLIENT
./send_email.py $CLIENT $CLIENT.zip
