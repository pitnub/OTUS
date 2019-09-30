### Использование атрибутов разграничения доступа - suid, sgid, sticky-bit, umask

####1. Сделать определенный каталог неизменяемым в Linux вместе со всем содержимым.

<pre>
[vagrant@shield ~]$ mkdir test
[vagrant@shield ~]$ lsattr
---------------- ./test
[vagrant@shield ~]$ touch test/t{1,2}
[vagrant@shield ~]$ ls -la test
total 0
drwxrwxr-x. 2 vagrant vagrant  26 Sep 25 16:51 .
drwx------. 4 vagrant vagrant 123 Sep 25 16:49 ..
-rw-rw-r--. 1 vagrant vagrant   0 Sep 25 16:51 t1
-rw-rw-r--. 1 vagrant vagrant   0 Sep 25 16:51 t2
[vagrant@shield ~]$ sudo chattr -R +i test
[vagrant@shield ~]$ lsattr
----i----------- ./test
[vagrant@shield ~]$ lsattr test
----i----------- test/t1
----i----------- test/t2
[vagrant@shield ~]$ rm -rf test
rm: cannot remove ‘test/t1’: Permission denied
rm: cannot remove ‘test/t2’: Permission denied
[vagrant@shield ~]$ rm test/t1
rm: remove write-protected regular empty file ‘test/t1’? y
rm: cannot remove ‘test/t1’: Permission denied
[vagrant@shield ~]$ rm test/t2
rm: remove write-protected regular empty file ‘test/t2’? y
rm: cannot remove ‘test/t2’: Permission denied
</pre>

####2. По аналогии с атрибутом защиты от перезаписи файла, установите атрибут открытия файла лишь в режиме дополнения.

<pre>
[vagrant@shield ~]$ sudo chattr -R -i +a test
[vagrant@shield ~]$ lsattr test
-----a---------- test/t1
-----a---------- test/t2
[vagrant@shield ~]$ echo 123 > test/t1
-bash: test/t1: Operation not permitted
[vagrant@shield ~]$ echo 123 >> test/t1
[vagrant@shield ~]$ cat test/t1
123
</pre>

####3. Защитить нашу систему Linux от создания или модификаций базы данных пользователей. Опишите возможные шаги для этого.

Защитить от модификации можно при помощи атрибута +i для файлов /etc/passwd и /etc/shadow.  
А вот от создания не совсем понятно - они же уже существуют :)

####4. Создайте директорию, которая будет принадлежать группе пользователей, причем каждый пользователь из этой группы должен иметь возможность читать данные из файлов, записывать данные в файлы и создавать новые файлы. Сделайте так, чтобы пользователи могли удалять только собственноручно созданные файлы.

<pre>
[vagrant@shield ~]$ sudo useradd user1
[vagrant@shield ~]$ sudo usermod -a -G users user1
[vagrant@shield ~]$ sudo useradd user2
[vagrant@shield ~]$ sudo usermod -a -G users user2
[vagrant@shield ~]$ cd /opt
[vagrant@shield opt]$ sudo mkdir test2
[vagrant@shield opt]$ sudo chgrp users test2
[vagrant@shield opt]$ sudo chmod 3770 test2
[vagrant@shield opt]$ sudo -i
[root@shield ~]# cd /opt
[root@shield opt]# setfacl -d -m u::rwx,g::rwx,o::---,g:users:rwx test2
[root@shield opt]# getfacl test2
# file: test2
# owner: root
# group: users
# flags: -st
user::rwx
group::rwx
other::---
default:user::rwx
default:group::rwx
default:group:users:rwx
default:mask::rwx
default:other::---
[root@shield opt]# ls -la
total 0
drwxr-xr-x.  3 root root   19 Sep 29 20:01 .
dr-xr-xr-x. 18 root root  255 Aug 25 20:01 ..
drwxrws--T+  2 root users   6 Sep 29 20:18 test2
[root@shield opt]# sudo -u user1 touch /opt/test2/f1
[root@shield opt]# sudo -u user2 touch /opt/test2/f2
[root@shield opt]# ls -la test2
total 0
drwxrws--T+ 2 root  users 26 Sep 29 20:24 .
drwxr-xr-x. 3 root  root  19 Sep 29 20:01 ..
-rw-rw----+ 1 user1 users  0 Sep 29 20:24 f1
-rw-rw----+ 1 user2 users  0 Sep 29 20:24 f2
[root@shield opt]# sudo -u user1 rm -f /opt/test2/f2
rm: cannot remove ‘/opt/test2/f2’: Operation not permitted
[root@shield opt]# sudo -u user2 rm -f /opt/test2/f1
rm: cannot remove ‘/opt/test2/f1’: Operation not permitted
[root@shield opt]# sudo -u user1 rm -f /opt/test2/f1
[root@shield opt]# sudo -u user2 rm -f /opt/test2/f2
</pre>

####5. Установите значение umask 077, использовав символьный формат. Проверьте работоспособность использованной команды. Затем выведите значение umask в восьмеричной и символьной форме.

<pre>
[vagrant@shield ~]$ umask u=rwx,g=,o=
[vagrant@shield ~]$ touch test/t3
[vagrant@shield ~]$ ls -la test/t3
-rw-------. 1 vagrant vagrant 0 Sep 29 20:51 test/t3
[vagrant@shield ~]$ umask
0077
[vagrant@shield ~]$ umask -S
u=rwx,g=,o=
</pre>

####6. В данном уроке была продемонстрирована методика использования утилит chattr и lsattr для управления дополнительными атрибутами файлов, позволяющими предотвратить случайную или преднамеренную модификацию последних. Помните о том, что вы не можете полагаться на утилиту chattr как на инструмент дополнительной защиты системы, так как снятие соответствующих атрибутов с файлов не будет представлять каких-либо сложностей для злоумышленников. Однако есть один надежный способ защититься от этой уязвимости, укажите его.

Не совсем понятна задача... Снятие атрибута "i" позволено руту или пользователям с правами в sudo.
Или мы считаем что злоумышленник имеет права рута ?

####7. Работая с администраторами, которые недавно познакомились с атрибутом SUID, вы заметили сценарий ниже - объясните что он делает и в чем здесь могут быть опасности:
<pre>
% ls change-pass
-rwsr-x--- 1 root helpdesk
37 Feb 26 16:35 change-pass

% cat change-pass
#!/bin/csh -b
set user = $1
passwd $user
</pre>

Данный скрипт дает возможность пользователям группы поддержки менять пароль для указанного пользователя (за счет SUID) в качестве входного параметра.  
Основная опасность в данном случае - использование C-shell в качестве интерпретатора.  
По причине манипуляции с переменными окружения.  
Например, как указано на сайте https://habr.com/ru/post/84635/:  
% env TERM='`cp /bin/sh /tmp/sh;chown root /tmp/sh;chmod 4755/tmp/sh`' change-pass

####8. Если разобрались с предыдущим, то тогда перепишите данный скрипт для безопасного использования. Какие рекомендации вы могли вы дать?

Опять же внимательно изучив статью https://habr.com/ru/post/84635, можно дать следующие рекомендации:  
1. Никогда не используйте C-shell для SUID-сценариев.
2. Необходимо всегда вручную устанавливать переменную окружения PATH и использовать абсолютные пути.
3. Необходимо понимать работу задействованных программ (в данном случае возможна замена пароля рута либо явно либо неявно (запуск без параметра))
4. Не используйте временный файлы или (в случае неизбежной необходимости их применения) не помещайте их в доступные на запись остальным места.
5. Не доверяйте и проверяйте весь пользовательский ввод, исключайте мета-символы.
6. Всегда определяйте IFS вручную.  

Из этих шести рекомендаций приведен модифицированный скрипт:
<pre>
#!/bin/sh
PATH='/bin:/usr/bin'
IFS=' '
user=${1##*[ \\$/;()|\>\<& ]}
[ -z $user ] && echo "Usage: change-pass username" && exit
[ "$user" = root ] && "You can't change root's password!" && exit
/usr/bin/passwd $user

Правда при поиске пользователя и удалении строки со спец-символами надо использовать другую команду (учитывая пример и ожидая имя пользователя в начале)  
user=${1%%[ \\$/;()|\>\<& ]*}

</pre>

Надежной защиты мы все равно не получим при использовании скрипта шелла с SUID...  
Поэтому главная рекомендация: **Не используйте SUID-сценарии**.  
$sudo passwd user

