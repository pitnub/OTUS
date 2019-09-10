### Задание 1. polkit
В виртуалке centos подключается диск.  
Необходимо создать policykit правила, разрешающих пользователю otus монтировать диски.

<pre>
yum install udisks2 -y
parted /dev/sdb mklabel msdos mkpart primary ext4 1MiB 10MiB
mkfs.ext4 /dev/sdb1
polkit.addRule(function(action, subject) {
    if (action.id.match("org.freedesktop.udisks2.filesystem-mount-system") && subject.user == "otus") {
      return polkit.Result.YES;
  }
});
udisksctl mount --block-device /dev/sdb1
udisksctl unmount --block-device /dev/sdb1
</pre>

### Задание 2. pam.d
Доделать пример начатый в лекции, запретить с помощью time_conf логиниться пользователю otus2 через ssh.

Ограничение доступа по ssh по неделе и времени:  
добавим строку  
account required pam_time.so  
в файл􏰀 /etc/pam.d/sshd  
в /etc/security/time.conf добавим регламентное время (Четверг с 14:00 до 18:00)  
sshd;*;otus2;Th1400-1800  
<pre>
# cp /home/vagrant/.ssh/autorized_keys /home/otus2/.ssh
# chown otus2:otus2 /home/otus2/.ssh/authorized_keys
$ ssh -i .vagrant/machines/centos/virtualbox/private_key otus2@127.0.0.1 -p2222
</pre>

### Задание 3. chroot
Настроить chroot при подключении через ssh пользователю otus3.

<pre>
CHROOT over ssh
# mkdir -p /secure/jail
# ls -l /dev/{null,zero,stdin,stdout,stderr,random,tty}
crw-rw-rw-. 1 root root 1, 3 Sep  5 09:33 /dev/null
crw-rw-rw-. 1 root root 1, 8 Sep  5 09:33 /dev/random
lrwxrwxrwx. 1 root root   15 Sep  5 09:33 /dev/stderr -> /proc/self/fd/2
lrwxrwxrwx. 1 root root   15 Sep  5 09:33 /dev/stdin -> /proc/self/fd/0
lrwxrwxrwx. 1 root root   15 Sep  5 09:33 /dev/stdout -> /proc/self/fd/1
crw-rw-rw-. 1 root tty  5, 0 Sep  5 11:30 /dev/tty
crw-rw-rw-. 1 root root 1, 5 Sep  5 09:33 /dev/zero
# mkdir -p /secure/jail/dev
# cd /secure/jail/dev
# mknod -m 666 null c 1 3
# mknod -m 666 random c 1 8
# mknod -m 666 tty c 5 0
# mknod -m 666 zero c 1 5
# mkdir -p /secure/jail/bin
# cp /bin/bash /secure/jail/bin/
# ldd /bin/bash
	linux-vdso.so.1 =>  (0x00007ffc51983000)
	libtinfo.so.5 => /lib64/libtinfo.so.5 (0x00007f3890d56000)
	libdl.so.2 => /lib64/libdl.so.2 (0x00007f3890b52000)
	libc.so.6 => /lib64/libc.so.6 (0x00007f3890785000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f3890f80000)
# mkdir -p /secure/jail/lib64
# cd /secure/jail/lib64
# cp /lib64/{libtinfo.so.5,libdl.so.2,libc.so.6,ld-linux-x86-64.so.2} .
# ldd /bin/ls
	linux-vdso.so.1 =>  (0x00007ffc1675b000)
	libselinux.so.1 => /lib64/libselinux.so.1 (0x00007f849118a000)
	libcap.so.2 => /lib64/libcap.so.2 (0x00007f8490f85000)
	libacl.so.1 => /lib64/libacl.so.1 (0x00007f8490d7c000)
	libc.so.6 => /lib64/libc.so.6 (0x00007f84909af000)
	libpcre.so.1 => /lib64/libpcre.so.1 (0x00007f849074d000)
	libdl.so.2 => /lib64/libdl.so.2 (0x00007f8490549000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f84913b1000)
	libattr.so.1 => /lib64/libattr.so.1 (0x00007f8490344000)
	libpthread.so.0 => /lib64/libpthread.so.0 (0x00007f8490128000)
# cp /lib64/{libselinux.so.1,libcap.so.2,libacl.so.1,libpcre.so.1,libattr.so.1,libpthread.so.0} .
# cp /bin/ls /secure/jail/bin/
# cp /bin/date /secure/jail/bin/
# cp /bin/mkdir /secure/jail/bin/
# mkdir -p /secure/jail/etc
# passwd otus3
# cp -f /etc/{passwd,group} /secure/jail/etc/
# mkdir -p /secure/jail/home/otus3
# chown -R otus3:otus3 /secure/jail/home/otus3
# chmod -R 0700 /secure/jail/home/otus3
# vi /etc/ssh/sshd_config
  Match User otus3
  ChrootDirectory /secure/jail
# systemctl restart sshd
# mkdir -p /home/otus3/.ssh
# cp /home/vagrant/.ssh/authorized_keys /home/otus3/.ssh/
# chown otus3:otus3 /home/otus3/.ssh/authorized_keys 
host# ssh -i .vagrant/machines/centos/virtualbox/private_key otus3@127.0.0.1 -p2222
-bash-4.2$ export PATH=$PATH:/bin
-bash-4.2$ cd /
-bash-4.2$ ls
bin  dev  etc  home  lib64
-bash-4.2$ ls -la
total 0
drwxr-xr-x. 7 0 0  64 Sep  6 16:04 .
drwxr-xr-x. 7 0 0  64 Sep  6 16:04 ..
drwxr-xr-x. 2 0 0  53 Sep  6 16:08 bin
drwxr-xr-x. 2 0 0  55 Sep  6 14:57 dev
drwxr-xr-x. 2 0 0  33 Sep  6 15:53 etc
drwxr-xr-x. 3 0 0  19 Sep  6 16:04 home
drwxr-xr-x. 2 0 0 214 Sep  6 15:12 lib64
-bash-4.2$ date
Fri Sep  6 16:18:40 UTC 2019
-bash-4.2$ exit
</pre>

### AppArmor

#### Установка docker
<pre>
sudo apt-get update
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
lsb_release -cs
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo docker run hello-world
</pre>

#### Подключение профиля
<pre>
$ sudo apparmor_status
$ sudo -i
# cd /etc/apparmor.d/containers/
# touch docker-nginx
# vi docker-nginx
#include <tunables/global>


profile docker-nginx flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  network inet tcp,
  network inet udp,
  network inet icmp,

  deny network raw,

  deny network packet,

  file,
  umount,

  deny /bin/** wl,
  deny /boot/** wl,
  deny /dev/** wl,
  deny /etc/** wl,
  deny /home/** wl,
  deny /lib/** wl,
  deny /lib64/** wl,
  deny /media/** wl,
  deny /mnt/** wl,
  deny /opt/** wl,
  deny /proc/** wl,
  deny /root/** wl,
  deny /sbin/** wl,
  deny /srv/** wl,
  deny /tmp/** wl,
  deny /sys/** wl,
  deny /usr/** wl,

  audit /** w,

  /var/run/nginx.pid w,

  /usr/sbin/nginx ix,

  deny /bin/dash mrwklx,
  deny /bin/sh mrwklx,
  deny /usr/bin/top mrwklx,


  capability chown,
  capability dac_override,
  capability setuid,
  capability setgid,
  capability net_bind_service,

  deny @{PROC}/* w,   # deny write for all files directly in /proc (not in a subdir)
  # deny write to files not in /proc/<number>/** or /proc/sys/**
  deny @{PROC}/{[^1-9],[^1-9][^0-9],[^1-9s][^0-9y][^0-9s],[^1-9][^0-9][^0-9][^0-9]*}/** w,
  deny @{PROC}/sys/[^k]** w,  # deny /proc/sys except /proc/sys/k* (effectively /proc/sys/kernel)
  deny @{PROC}/sys/kernel/{?,??,[^s][^h][^m]**} w,  # deny everything except shm* in /proc/sys/kernel/
  deny @{PROC}/sysrq-trigger rwklx,
  deny @{PROC}/mem rwklx,
  deny @{PROC}/kmem rwklx,
  deny @{PROC}/kcore rwklx,

  deny mount,

  deny /sys/[^f]*/** wklx,
  deny /sys/f[^s]*/** wklx,
  deny /sys/fs/[^c]*/** wklx,
  deny /sys/fs/c[^g]*/** wklx,
  deny /sys/fs/cg[^r]*/** wklx,
  deny /sys/firmware/** rwklx,
  deny /sys/kernel/security/** rwklx,
}

# exit
$ sudo apparmor_parser -r -W /etc/apparmor.d/containers/docker-nginx
$ sudo apparmor_status
$ sudo docker run --security-opt "apparmor=docker-nginx" -p 80:80 -d --name apparmor-nginx nginx
$ sudo docker container ls
$ ss -ltn | grep 80
$ curl http://127.0.0.1
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>

$ sudo docker container exec -it apparmor-nginx bash
root@2752445ce45e:/# uname -a
Linux 2752445ce45e 4.15.0-60-generic #67-Ubuntu SMP Thu Aug 22 16:55:30 UTC 2019 x86_64 GNU/Linux
root@2752445ce45e:/# sh
bash: /bin/sh: Permission denied
root@2752445ce45e:/# touch ~/thing
touch: cannot touch '/root/thing': Permission denied
root@2752445ce45e:/# dash
bash: /bin/dash: Permission denied
root@2752445ce45e:/# exit
$ sudo docker stop apparmor-nginx
</pre>
