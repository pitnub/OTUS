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
</pre>

