### Фильтрация трафика с помощью межсетевого экрана iptables

#### 1. Почему нельзя так делать на удаленной машине? И что делать если вдруг это произошло на виртуальной машине? <pre># iptables -P INPUT DROP

Потому что в случае очистки цепочек (-F) будет заблокирован доступ по сети на данную машину.  
Если новая конфигурация не была сохранена - то просто перегрузить виртуалку.
Если была сохранена - то через консоль.

#### 2. Приведите пример настройки iptables, который разрешит только порт 22 и дальше проверять не будет. Те же, кто идет не на 22 порт, те будут отброшены.

<pre>
iptables -F INPUT
iptables -P INPUT ACCEPT
iptables -I INPUT -m conntrack --ctstate NEW,ESTABLISHED -m tcp -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -j REJECT --reject-with icmp-host-prohibited
</pre>

#### 3. Настроить сетевой фильтр, чтобы был доступ только к сервисам HTTP(S) и SSH.

<pre>
iptables -F INPUT
iptables -P INPUT ACCEPT
iptables -I INPUT -m conntrack --ctstate NEW,ESTABLISHED -m tcp -p tcp -m multiport --dport 22,80,443 -j ACCEPT
iptables -A INPUT -j REJECT --reject-with icmp-host-prohibited
</pre>

#### 4. Настроить правила iptables, чтобы из внешней сети можно было обратиться только к портам 2002, 8080 и 8081. Запросы, идущие на внешний порт 8080, перенаправлять на внутренний порт 80, запросы на порт 8081 - перенаправлять на 443 порт и запросы на 2002 перенаправлять на внутренний 22-й порт.

<pre>
iptables -t nat -F
iptables -t nat -A PREROUTING -p tcp --dport 2002 -j REDIRECT --to-port 22
iptables -t nat -A PREROUTING -p tcp --dport 8080 -j REDIRECT --to-port 80
iptables -t nat -A PREROUTING -p tcp --dport 8081 -j REDIRECT --to-port 443
iptables -F INPUT
iptables -P INPUT ACCEPT
iptables -I INPUT -m conntrack --ctstate NEW,ESTABLISHED -m tcp -p tcp -m multiport --dport 22,80,443 -j ACCEPT
iptables -A INPUT -j REJECT --reject-with icmp-host-prohibited
</pre>

#### 5. Настроить доступ по SSH только из указанного адреса или сетевого диапазона.

<pre>
iptables -F INPUT
iptables -P INPUT ACCEPT
iptables -I INPUT -m conntrack --ctstate NEW,ESTABLISHED -m tcp -p tcp -s 192.168.100.100 --dport 22 -j ACCEPT
iptables -I INPUT -m conntrack --ctstate NEW,ESTABLISHED -m tcp -p tcp -s 192.168.8.0/24 --dport 22 -j ACCEPT
iptables -A INPUT -j REJECT --reject-with icmp-host-prohibited
</pre>

#### 6*. Реализовать Port Knocking (см. ссылку в презентации)


**CentOS 7**
<pre>
systemctl stop firewalld
yum install nginx
yum install iptables-services
systemctl start iptables
iptables -N KNOCK
iptables -N KN1
iptables -N KN2
iptables -I INPUT 5 -j KNOCK
iptables -A KNOCK -m state --state NEW -m tcp -p tcp --dport 80 -m recent --rcheck --seconds 30 --name WEB2 -j ACCEPT
iptables -A KNOCK -m state --state NEW -m tcp -p tcp -m recent --name WEB2 --remove -j DROP
iptables -A KNOCK -m state --state NEW -m tcp -p tcp --dport 3333 -m recent --rcheck --name WEB1 -j KN2
iptables -A KNOCK -m state --state NEW -m tcp -p tcp -m recent --name WEB1 --remove -j DROP
iptables -A KNOCK -m state --state NEW -m tcp -p tcp --dport 2222 -m recent --rcheck --name WEB0 -j KN1
iptables -A KNOCK -m state --state NEW -m tcp -p tcp -m recent --name WEB0 --remove -j DROP
iptables -A KNOCK -m state --state NEW -m tcp -p tcp --dport 1111 -m recent --name WEB0 --set -j DROP
iptables -A KN1 -m recent --name WEB1 --set -j DROP
iptables -A KN2 -m recent --name WEB2 --set -j DROP
iptables -A KNOCK -j RETURN
systemctl start nginx
</pre>

**Kali**
<pre>
# apt install knockd
vagrant@sword:~$ nmap -Pn -sT -p 80 192.168.51.5
Starting Nmap 7.70 ( https://nmap.org ) at 2019-10-17 15:54 EDT
Nmap scan report for host-192-168-51-5.soho.net.ua (192.168.51.5)
Host is up (0.00093s latency).

PORT   STATE    SERVICE
80/tcp filtered http

Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds

vagrant@sword:~$ knock 192.168.51.5 1111 2222 3333
vagrant@sword:~$ nmap -Pn -sT -p 80 192.168.51.5
Starting Nmap 7.70 ( https://nmap.org ) at 2019-10-17 15:55 EDT
Nmap scan report for host-192-168-51-5.soho.net.ua (192.168.51.5)
Host is up (0.00057s latency).

PORT   STATE SERVICE
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds
vagrant@sword:~$
</pre>

#### 7*. Реализовать проход на порт 80 без маскарадинга (подсказка: SNAT)

Внешний адрес шлюза - 1.2.3.4  
Внутренний адрес вэб-сервера - 192.168.0.10
<pre>
iptables -t nat -I PREROUTING -m tcp -p tcp -d 1.2.3.4 --dport 80 -j DNAT --to-destination 192.168.0.10:80
iptables -t nat -I POSTROUTING -m tcp -p tcp -s 192.168.0.10 --sport 80 -j SNAT --to-source 1.2.3.4:80
</pre>
