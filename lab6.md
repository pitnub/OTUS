### Управление паролями и выполнение от root

####1. Пароли пользователей - http://rus-linux.net/MyLDP/BOOKS/Linux_Foundations/27/ch27.html
Данная работа уже отражена в предыдущем домашнем задании.

####2. Скрипты экспресс-аудита безопасности для Linux

<pre>
Список пользователей с доступом к /bin/bash:
# grep /bin/bash /etc/passwd | cut -d: -f1 | sort
otus
root
vagrant

Список статусов всех пользователей системы:
# for i in $(cut -d: -f1 /etc/shadow); do passwd -S $i; done
root PS 1969-12-31 0 99999 7 -1 (Password set, MD5 crypt.)
bin LK 2018-10-30 0 99999 7 -1 (Alternate authentication scheme in use.)
daemon LK 2018-10-30 0 99999 7 -1 (Alternate authentication scheme in use.)
adm LK 2018-10-30 0 99999 7 -1 (Alternate authentication scheme in use.)
lp LK 2018-10-30 0 99999 7 -1 (Alternate authentication scheme in use.)
sync LK 2018-10-30 0 99999 7 -1 (Alternate authentication scheme in use.)
shutdown LK 2018-10-30 0 99999 7 -1 (Alternate authentication scheme in use.)
halt LK 2018-10-30 0 99999 7 -1 (Alternate authentication scheme in use.)
mail LK 2018-10-30 0 99999 7 -1 (Alternate authentication scheme in use.)
operator LK 2018-10-30 0 99999 7 -1 (Alternate authentication scheme in use.)
games LK 2018-10-30 0 99999 7 -1 (Alternate authentication scheme in use.)
ftp LK 2018-10-30 0 99999 7 -1 (Alternate authentication scheme in use.)
nobody LK 2018-10-30 0 99999 7 -1 (Alternate authentication scheme in use.)
systemd-network LK 2019-06-01 -1 -1 -1 -1 (Password locked.)
dbus LK 2019-06-01 -1 -1 -1 -1 (Password locked.)
polkitd LK 2019-06-01 -1 -1 -1 -1 (Password locked.)
rpc LK 2019-06-01 0 99999 7 -1 (Password locked.)
rpcuser LK 2019-06-01 -1 -1 -1 -1 (Password locked.)
nfsnobody LK 2019-06-01 -1 -1 -1 -1 (Password locked.)
sshd LK 2019-06-01 -1 -1 -1 -1 (Password locked.)
postfix LK 2019-06-01 -1 -1 -1 -1 (Password locked.)
chrony LK 2019-06-01 -1 -1 -1 -1 (Password locked.)
vagrant PS 1969-12-31 0 99999 7 -1 (Password set, MD5 crypt.)
utime LK 2019-09-11 0 99999 7 -1 (Password locked.)
otus PS 2019-09-11 0 10 7 -1 (Password set, DES crypt.)

Активность текущего пользователя:
# yum install psacct
[root@shield ~]# ac
	total        9.79
[root@shield ~]# ac -d
Aug 25	total        1.13
Today	total        8.66
И определенного пользователя:
[root@shield ~]# ac vagrant
	total        9.85
Журнал подключений в систему:
[root@shield ~]# last | grep -v reboot
vagrant  pts/0        10.0.2.2         Wed Sep 11 08:06   still logged in   
vagrant  pts/0        10.0.2.2         Sun Aug 25 21:35 - 21:41  (00:06)    
vagrant  pts/0        10.0.2.2         Sun Aug 25 20:22 - 21:24  (01:01)

Список пользователей с пустыми паролями:
# cat /etc/shadow | awk -F: '($2==""){print($1)}'

Проверка наличия парольной политики.
Для этого должен быть установлен pam-модуль pam_pwquality.
# grep pam_pwquality /etc/pam.d/*
password-auth:password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 authtok_type=
password-auth-ac:password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 authtok_type=
system-auth:password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 authtok_type=
system-auth-ac:password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 authtok_type=

Проверка установлена ли политика смены паролей путем анализа файла /etc/login.defs
# grep PASS_MAX_DAYS /etc/login.defs | grep -v ^#
PASS_MAX_DAYS	99999
В данном случае такой политики нет.
Рекомендуется установить для этой переменной какое-то количество дней, скажем 30 дней.
Если необходимо установить этот параметр индивидуально, то можно воспользоваться командой chage.
# chage -M 30 otus

Убедиться что запрещен вход в систему для пользоватлея root.
# grep PermitRootLogin /etc/ssh/sshd_config 
#PermitRootLogin yes
В данном случае вход запрещен.

Для защиты от брутфорса полезно установить пакет denyhosts или fail2ban.

Убедиться что в системе ведется журналирование используя демон rsyslogd.
# systemctl status rsyslog
● rsyslog.service - System Logging Service
   Loaded: loaded (/usr/lib/systemd/system/rsyslog.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2019-09-11 08:05:04 UTC; 1 day 1h ago
     Docs: man:rsyslogd(8)
           http://www.rsyslog.com/doc/
 Main PID: 2417 (rsyslogd)
   CGroup: /system.slice/rsyslog.service
           └─2417 /usr/sbin/rsyslogd -n
           
Проверка текущих открытых сетевых портов в режиме LISTEN:
# ss -lntu
Netid State      Recv-Q Send-Q  Local Address:Port Peer Address:Port              
udp   UNCONN     0      0       *:68               *:*                  
udp   UNCONN     0      0       *:111              *:*                  
udp   UNCONN     0      0       127.0.0.1:323      *:*                  
udp   UNCONN     0      0       *:642              *:*                  
udp   UNCONN     0      0       :::111             :::*                  
udp   UNCONN     0      0       ::1:323            :::*                  
udp   UNCONN     0      0       :::642             :::*                  
tcp   LISTEN     0      128     *:111              *:*                  
tcp   LISTEN     0      128     *:22               *:*                  
tcp   LISTEN     0      100     127.0.0.1:25       *:*                  
tcp   LISTEN     0      128     :::111             :::*                  
tcp   LISTEN     0      128     :::22              :::*                  
tcp   LISTEN     0      100     ::1:25             :::*

Можно также воспользоваться командой lsof:
# lsof -ni
COMMAND   PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
systemd     1    root   66u  IPv4  16176      0t0  TCP *:sunrpc (LISTEN)
systemd     1    root   67u  IPv4  16177      0t0  UDP *:sunrpc 
systemd     1    root   68u  IPv6  16178      0t0  TCP *:sunrpc (LISTEN)
systemd     1    root   69u  IPv6  16179      0t0  UDP *:sunrpc 
chronyd  1789  chrony    1u  IPv4  17812      0t0  UDP 127.0.0.1:323 
chronyd  1789  chrony    2u  IPv6  17813      0t0  UDP [::1]:323 
rpcbind  1805     rpc    4u  IPv4  16176      0t0  TCP *:sunrpc (LISTEN)
rpcbind  1805     rpc    5u  IPv4  16177      0t0  UDP *:sunrpc 
rpcbind  1805     rpc    6u  IPv6  16178      0t0  TCP *:sunrpc (LISTEN)
rpcbind  1805     rpc    7u  IPv6  16179      0t0  UDP *:sunrpc 
rpcbind  1805     rpc   10u  IPv4  17736      0t0  UDP *:esro-emsdp 
rpcbind  1805     rpc   11u  IPv6  17785      0t0  UDP *:esro-emsdp 
sshd     2416    root    3u  IPv4  20933      0t0  TCP *:ssh (LISTEN)
sshd     2416    root    4u  IPv6  20949      0t0  TCP *:ssh (LISTEN)
master   2743    root   13u  IPv4  21970      0t0  TCP 127.0.0.1:smtp (LISTEN)
master   2743    root   14u  IPv6  21971      0t0  TCP [::1]:smtp (LISTEN)
dhclient 4152    root    6u  IPv4  26559      0t0  UDP *:bootpc 
sshd     4751    root    3u  IPv4  28420      0t0  TCP 10.0.2.15:ssh->10.0.2.2:49790 (ESTABLISHED)
sshd     4754 vagrant    3u  IPv4  28420      0t0  TCP 10.0.2.15:ssh->10.0.2.2:49790 (ESTABLISHED)

Проверить запущен ли межсетевой экран firewalld:
# systemctl status firewalld
● firewalld.service - firewalld - dynamic firewall daemon
   Loaded: loaded (/usr/lib/systemd/system/firewalld.service; disabled; vendor preset: enabled)
   Active: inactive (dead)
     Docs: man:firewalld(1)
В данном случае он выключен.

Проверить доступны ли новые обновления при помощи команды yum:
# yum list updates

Проверить включен ли режим безопасности SELinux:
# getenforce 
Enforcing
</pre>

####3,4. Права суперпользователя Linux. sudo или su ?

<pre>
Для переключения работы под другим пользователем используется команда su, если не указывать конкретного пользователя используется root.

Пример без использования окружения пользователя:
[vagrant@shield ~]$ echo $PATH
/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/vagrant/.local/bin:/home/vagrant/bin
[vagrant@shield ~]$ whoami
vagrant
[vagrant@shield ~]$ su
Password: 
[root@shield vagrant]# whoami
root
[root@shield vagrant]# echo $PATH
/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/vagrant/.local/bin:/home/vagrant/bin
[root@shield vagrant]# pwd
/home/vagrant
[root@shield vagrant]# exit
exit

Пример с использованием окружения пользователя:
[vagrant@shield ~]$ su -
Password: 
Last login: Thu Sep 12 22:31:12 UTC 2019 on pts/0
[root@shield ~]# whoami
root
[root@shield ~]# echo $PATH
/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
[root@shield ~]# pwd
/root
[root@shield ~]#

Примеры запуска команд.
[vagrant@shield ~]$ su -c date
Password: 
Thu Sep 12 22:35:54 UTC 2019
[vagrant@shield ~]$ su -c date otus
Password: 
Thu Sep 12 22:37:55 UTC 2019

Запуск команд под другим пользователем без переключения при помощи утилиты sudo:
[vagrant@shield ~]$ sudo date
Thu Sep 12 23:05:07 UTC 2019
[vagrant@shield ~]$ sudo -u otus date
Thu Sep 12 23:05:20 UTC 2019
[vagrant@shield ~]$ 

Запрос пароля не запрашивался по причине директивы NOPASSWD в файле /etc/sudoers.d/vagrant
[vagrant@shield ~]$ sudo -l
Matching Defaults entries for vagrant on shield:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin, env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS", env_keep+="MAIL PS1 PS2 QTDIR USERNAME
    LANG LC_ADDRESS LC_CTYPE", env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES", env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE", env_keep+="LC_TIME LC_ALL
    LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY", secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User vagrant may run the following commands on shield:
    (ALL) NOPASSWD: ALL

Правильнее использовать в работе команду sudo, т.к. в этом случае нет необходимости знать пароль рута, а достаточно ввести только свой пароль.
</pre>

####5. Настройка sudo в Linux.

<pre>
Настройки для использования sudo находятся в файле /etc/sudoers.
Модификация этих настроек выполняется при помощи команды visudo.
В данном файле есть следующие разделы:
 - задание настроек по умолчанию (директива Defaults)
 - создание алиасов для пользователей (тип User_Alias), хостов (тип Host_Alias), команд (тип Cmnd_Alias), целевых пользователей (тип Runas_Alias)
 - создание правил вида Users Hosts = [Runas] [flag] Commands
 - примером флагов может быть например NOPASSWD (без запроса пароля), NOEXEC (запрет выполненя команды)
 - директива #includedir /etc/sudoers.d для создания собственных файлов конфигураций.

В качестве примера создадим правило, разрешающее пользователю otus запуск команд touch и fdisk с машины shield:
[otus@shield ~]$ fdisk -l
fdisk: cannot open /dev/sda: Permission denied

[vagrant@shield ~]$ sudo cat /etc/sudoers.d/otus
otus shield = /bin/touch, /sbin/fdisk

vagrant@shield ~]$ sudo -u otus -i
[otus@shield ~]$ sudo /bin/touch /root/1
[sudo] password for otus: 
[otus@shield ~]$ exit
logout
[vagrant@shield ~]$ sudo ls -la /root/1
-rw-r--r--. 1 root root 0 Sep 13 06:17 /root/1

[otus@shield ~]$ sudo /sbin/fdisk -l

Disk /dev/sda: 42.9 GB, 42949672960 bytes, 83886080 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x0009ef88

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048    83886079    41942016   83  Linux
</pre>

