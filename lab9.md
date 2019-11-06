### Cконфигурировать доступ пользователей в сеть Интернет на прокси-сервере SQIUD

Реализация будет на подготовленном ранее стенде (Kali -> CentOS).  
Kali (sword) будет клиентом 192.168.51.66/24, CentOS (shield) будет роутером и прокси-сервером 192.168.51.5/24.  
Будет реализован полноценный прозрачный прокси для протоколов http(80) и https(443), причем без необходимости установки сертификата на клиенте.  

<pre>
shield:
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -s 192.168.51.0/24 -o eth0 -j SNAT --to-source=10.0.2.15
iptables -t nat -A PREROUTING -p tcp -m tcp -s 192.168.51.0/24 --dport 443 -j REDIRECT --to-ports 3129
iptables -t nat -A PREROUTING -p tcp -m tcp -s 192.168.51.0/24 --dport 80 -j REDIRECT --to-ports 3128

yum install squid
squid -v | xargs -n1 | grep ssl
--enable-ssl-crtd
--with-openssl
ls /lib64/squid/ | grep ssl
ssl_crtd

cd /etc/squid
mkdir ssl_cert
chown squid:squid ssl_cert
chmod 700 ssl_cert
cd ssl_cert
openssl req -new -newkey rsa:2048 -sha256 -days 365 -nodes -x509 -keyout myCA.pem -out myCA.pem
Данные: UA,Odessa,Odessa,Home,Room,shield,,

/usr/lib64/squid/ssl_crtd -c -s /var/lib/ssl_db
chown -R squid:squid /var/lib/ssl_db/
Необходимости в настройке SELinux(который был в enforce) не понадобилось.

/etc/squid/squid.conf:
acl localnet src 192.168.51.0/24
acl SSL_ports port 443
acl Safe_ports port 80		# http
acl Safe_ports port 443		# https
acl CONNECT method CONNECT
http_access deny !Safe_ports
http_access deny CONNECT !SSL_ports
http_access allow localhost manager
http_access deny manager
http_access deny to_localhost
http_access allow localnet
http_access allow localhost
http_access deny all
http_port 192.168.51.5:3128 intercept options=NO_SSLv3:NO_SSLv2
http_port 192.168.51.5:3130 options=NO_SSLv3:NO_SSLv2
https_port 192.168.51.5:3129 intercept ssl-bump options=ALL:NO_SSLv3:NO_SSLv2 connection-auth=off cert=/etc/squid/ssl_cert/myCA.pem
always_direct allow all
sslproxy_cert_error allow all
sslproxy_flags DONT_VERIFY_PEER
acl step1 at_step SslBump1
ssl_bump peek step1
ssl_bump splice all
sslcrtd_program /usr/lib64/squid/ssl_crtd -s /var/lib/ssl_db -M 4MB
coredump_dir /var/spool/squid
refresh_pattern ^ftp:		1440	20%	10080
refresh_pattern ^gopher:	1440	0%	1440
refresh_pattern -i (/cgi-bin/|\?) 0	0%	0
refresh_pattern .		0	20%	4320


sword:
ip route add default via 192.168.51.5
Заходил через браузер на разные сайты https:// - все было корректно и данные фиксировались в журнале прокси-сервера.
</pre>

