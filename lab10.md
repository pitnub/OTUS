### Настроить правила выделения памяти, дискового пространства и использования центрального процессора под сетевые сервисы и ресурсы web-сервера Apache

<pre>
yum install httpd -y
systemctl start httpd
systemctl status httpd
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; disabled; vendor preset: disabled)
   Active: active (running) since Sun 2019-12-15 19:45:24 UTC; 4s ago
     Docs: man:httpd(8)
           man:apachectl(8)
 Main PID: 5141 (httpd)
   Status: "Processing requests..."
   CGroup: /system.slice/httpd.service
           ├─5141 /usr/sbin/httpd -DFOREGROUND
           ├─5142 /usr/sbin/httpd -DFOREGROUND
           ├─5143 /usr/sbin/httpd -DFOREGROUND
           ├─5144 /usr/sbin/httpd -DFOREGROUND
           ├─5145 /usr/sbin/httpd -DFOREGROUND
           └─5146 /usr/sbin/httpd -DFOREGROUND

systemctl set-property httpd CPUShares=512 MemoryLimit=500M BlockIOWeight=500
systemctl status httpd
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; disabled; vendor preset: disabled)
  Drop-In: /etc/systemd/system/httpd.service.d
           └─50-BlockIOWeight.conf, 50-CPUShares.conf, 50-MemoryLimit.conf
   Active: active (running) since Sun 2019-12-15 20:27:06 UTC; 10min ago
     Docs: man:httpd(8)
           man:apachectl(8)
 Main PID: 5325 (httpd)
   Status: "Total requests: 0; Current requests/sec: 0; Current traffic:   0 B/sec"
   Memory: 2.7M (limit: 500.0M)
   CGroup: /system.slice/httpd.service
           ├─5325 /usr/sbin/httpd -DFOREGROUND
           ├─5326 /usr/sbin/httpd -DFOREGROUND
           ├─5327 /usr/sbin/httpd -DFOREGROUND
           ├─5328 /usr/sbin/httpd -DFOREGROUND
           ├─5329 /usr/sbin/httpd -DFOREGROUND
           └─5330 /usr/sbin/httpd -DFOREGROUND

Отмена установленных ограничений:

rm -rf /etc/systemd/system/httpd.service.d/
systemctl daemon-reload
systemctl restart httpd
systemctl status httpd
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; disabled; vendor preset: disabled)
   Active: active (running) since Sun 2019-12-15 20:46:15 UTC; 6s ago
     Docs: man:httpd(8)
           man:apachectl(8)
  Process: 5788 ExecStop=/bin/kill -WINCH ${MAINPID} (code=exited, status=0/SUCCESS)
 Main PID: 5791 (httpd)
   Status: "Processing requests..."
   CGroup: /system.slice/httpd.service
           ├─5791 /usr/sbin/httpd -DFOREGROUND
           ├─5792 /usr/sbin/httpd -DFOREGROUND
           ├─5793 /usr/sbin/httpd -DFOREGROUND
           ├─5794 /usr/sbin/httpd -DFOREGROUND
           ├─5795 /usr/sbin/httpd -DFOREGROUND
           └─5796 /usr/sbin/httpd -DFOREGROUND


Настройка использования дискового пространства Apache для директорий с журналами (/var/log/httpd/) и данными (/var/www/).
Т.к. необходимо настроить разные значения для указанных директорий, то целесообразно использовать квоты на директории.
Квоты на директории (помимо пользовательских и групповых) реализованы на данный момент только в файловой системе xfs и называются project quota.

Добавляем параметры uquota,guota,pquota после параметра defaults (в строке устройства к которому принадлежат наши директории - в нашем случае это корень системы) в файле /etc/fstab.
UUID=8ac075e3-1124-4bb6-bef7-a6811bf8b870 / xfs  defaults,uquota,gquota,pquota 0 0

Т.к. наши директории принадлежат корню, то после перезагрузки мы скорее всего не увидим эти параметры...
Это потому что по умолчанию ядро загружается с опцией noquota для корня системы.
Поэтому добавляем те же параметры для переменной rootflags в строку загрузки ядра в файле /etc/default/grub:
GRUB_CMDLINE_LINUX="no_timer_check console=tty0 console=ttyS0,115200n8 net.ifnames=0 biosdevname=0 elevator=noop crashkernel=auto rootflags=uquota,gquota,pquota"
Формируем новый файл конфигурации grub2 и перегружаемся:
grub2-mkconfig -o /boot/grub2/grub.cfg
reboot

mount | grep xfs
/dev/sda1 on / type xfs (rw,relatime,seclabel,attr2,inode64,usrquota,prjquota,grpquota)

Описание проекта и связывание его с уникальным идентификатором:
echo apachedata:80 >> /etc/projid
echo apachelog:81 >> /etc/projid

Связывание идентификатора проекта с местоположением директории:
echo 80:/var/www >> projects
echo 81:/var/log/httpd >> projects

Инициализация проектов:
# xfs_quota -x -c "project -s apachedata"
Setting up project apachedata (path /var/www)...
Processed 1 (/etc/projects and cmdline) paths for project apachedata with recursion depth infinite (-1).
# xfs_quota -x -c "project -s apachelog"
Setting up project apachelog (path /var/log/httpd)...
Processed 1 (/etc/projects and cmdline) paths for project apachelog with recursion depth infinite (-1).

# xfs_quota -x -c "print"
Filesystem          Pathname
/                   /dev/sda1 (uquota, gquota, pquota)
/var/www            /dev/sda1 (project 80, apachedata)
/var/log/httpd      /dev/sda1 (project 81, apachelog)

# xfs_quota -x -c "report -pbih"
Project quota on / (/dev/sda1)
                        Blocks                            Inodes              
Project ID   Used   Soft   Hard Warn/Grace     Used   Soft   Hard Warn/Grace  
---------- --------------------------------- --------------------------------- 
#0           3.2G      0      0  00 [------]  36.1k      0      0  00 [------]
apachedata      0      0      0  00 [------]      3      0      0  00 [------]
apachelog      8K      0      0  00 [------]      4      0      0  00 [------]


# xfs_quota -x -c "limit -p bsoft=1g bhard=1100m apachedata"
# xfs_quota -x -c "limit -p bsoft=100m bhard=150m apachelog"
# xfs_quota -x -c "report -pbih"
Project quota on / (/dev/sda1)
                        Blocks                            Inodes              
Project ID   Used   Soft   Hard Warn/Grace     Used   Soft   Hard Warn/Grace  
---------- --------------------------------- --------------------------------- 
#0           3.2G      0      0  00 [------]  36.1k      0      0  00 [------]
apachedata      0     1G   1.1G  00 [------]      3      0      0  00 [------]
apachelog      8K   100M   150M  00 [------]      4      0      0  00 [------]

# dd if=/dev/zero of=/var/log/httpd/testfile bs=1024 count=200000
dd: error writing ‘/var/log/httpd/testfile’: No space left on device
153593+0 records in
153592+0 records out
157278208 bytes (157 MB) copied, 0.829169 s, 190 MB/s

# xfs_quota -x -c "report -pbih"
Project quota on / (/dev/sda1)
                        Blocks                            Inodes              
Project ID   Used   Soft   Hard Warn/Grace     Used   Soft   Hard Warn/Grace  
---------- --------------------------------- --------------------------------- 
#0           3.2G      0      0  00 [------]  36.1k      0      0  00 [------]
apachedata      0     1G   1.1G  00 [------]      3      0      0  00 [------]
apachelog    150M   100M   150M  00 [6 days]      5      0      0  00 [------]


</pre>

