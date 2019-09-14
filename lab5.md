### Управление пользователями и группами
#####1. Создайте учетную запись пользователя с именем utime и утилитой /bin/time в качестве стандартной командной оболочки.
   <pre>
   # useradd -c "user for testing" -s /bin/time
   # grep utime /etc/passwd
   utime:x:1001:1001:user for testing:/home/utime:/bin/time
   # grep utime /etc/shadow
   utime:!!:18150:0:99999:7:::
   </pre>  
   
   Что случится, если вы войдете в систему под именем пользователя utime?  
   Будет отображена краткая информация по запуску данной утилиты, т.к. нет обязательного параметра (command).

   <pre>
   # su utime
   Usage: time [-apvV] [-f format] [-o file] [--append] [--verbose]
       [--portability] [--format=format] [--output=file] [--version]
       [--help] command [arg...]
   </pre>
   
####2. Используйте команду passwd -d для деактивации пароля пользователя utime.

<pre>  
# passwd -d utime
Removing password for user utime.
passwd: Success
</pre>

Проверьте наличие строки для пользователя utime в файле /etc/shadow до и после осуществления деактивации.  

<pre>
# grep utime /etc/shadow
utime:!!:18150:0:99999:7:::
# grep utime /etc/shadow
utime::18150:0:99999:7:::
</pre>

Как можно определить, заблокирован или разблокирован пароль пользователя utime? 
По второму полю файла /etc/shadow:  
Если перед хэшем стоит восклицательный знак - то пароль заблокирован.  
Если хэша нет, но присутствуют знаки !! или * - то пользователь не сможет использовать пароль.  
Если пусто - то пароль не требуется.  

Предложите решение на основе утилиты grep(см. выше), а также решение на основе утилиты passwd.

<pre>
# passwd -S utime
utime NP 2019-09-11 0 99999 7 -1 (Empty password.)
</pre>

#### 3. Создайте учетную запись пользователя с именем otus, с указанием на необходимость использования командной оболочки bash и описанием "Owl", а также домашнюю директорию этого пользователя с помощью одной команды. Также сгенерируйте и установите пароль для пользователя otus (использовать 2 метода создания пароля: crypt и openssl).

<pre>
# useradd -c "Owl" -s /bin/bash otus
# passwd otus
Changing password for user otus.
New password: 
Retype new password: 
passwd: all authentication tokens updated successfully.
# grep otus /etc/shadow
otus:$1$IabH1Uvf$18oFIlD5fqsbyCBEvpisD/:18150:0:99999:7:::

# openssl passwd -salt 17 0tu5-0tu5
Warning: truncating password to 8 characters
17rCxc0utdDAk
[root@shield ~]# usermod -p 17rCxc0utdDAk otus
# grep otus /etc/shadow
otus:17rCxc0utdDAk:18150:0:99999:7:::
[root@shield ~]# exit
logout
[vagrant@shield ~]$ su otus
Password: 
[otus@shield vagrant]$

[root@shield ~]# chpasswd -c SHA512
utime:utime4
[root@shield ~]# grep utime /etc/shadow
utime:$6$3kCGMLzVXS/7Oa$weNC6cWxWv9/8TDcGPb2ity0oXb1W4xmDEcGS6A4CyxIhjhzPtGWl1vV4P2hlb4G5NdRH3NDV08haAZFr2omJ.:18152:0:99999:7:::
[root@shield ~]# exit
logout
[vagrant@shield ~]$ su utime
Password: 
[utime@shield vagrant]$ 

</pre>


####4. Заблокируйте учетную запись пользователя otus с помощью утилиты usermod. Проверьте наличие признаков блокировки в файле /etc/shadow до и после осуществления блокировки. Каковы различия между операцией блокировки пользовательской учетной записи и операцией деактивации пароля пользовательской учетной записи, которые мы только что осуществляли с помощью команд usermod -L и passwd -d?

<pre>
# grep otus /etc/shadow
otus:17rCxc0utdDAk:18150:0:99999:7:::
# usermod -L otus
# grep otus /etc/shadow
otus:!17rCxc0utdDAk:18150:0:99999:7:::
</pre>

В случае блокировки учетной записи пользователь не сможет пройти аутентификацию.
В случае деактивации пароля пользователь зайдет в систему без пароля.

####5. Сделайте так, чтобы пользователь otus был обязан изменять пароль через каждые 10 дней. Затем так, чтобы каждый новый пользователь был обязан изменять свой пароль через каждые 30 дней.

<pre>
# chage -M 10 otus
# chage -l otus
Last password change					: Sep 11, 2019
Password expires					: Sep 21, 2019
Password inactive					: never
Account expires						: never
Minimum number of days between password change		: 0
Maximum number of days between password change		: 10
Number of days of warning before password expires	: 7
</pre>

Для устновки 30 дней для всех будущих пользователй необходимо для переменной PASS_MAX_DAYS из файла /etc/login.defs указать 30(вместо 99999).

####6. Воспользуйтесь учетной записью пользователя root для создания резервной копии файла /etc/shadow. Используйте текстовый редактор для копирования хэша пароля из строки пользователя otus в строку пользователя utime. Может ли после этого пользователь utime войти в систему с паролем пользователя otus? 

Это вопрос с подвохом ? :)  
Если двигаться линейно по заданиям - то нет, т.к. при копировании второго поля мы скопируем и знак блокировки :)  
Если же четко скопировать именно хэш - то сможет.

<pre>
# usermod -U otus
# vipw -s
Копируем хэш.
# grep utime /etc/shadow
utime:17rCxc0utdDAk:18150:0:99999:7:::
# exit
logout
[vagrant@shield ~]$ su utime
Password: 
Usage: time [-apvV] [-f format] [-o file] [--append] [--verbose]
       [--portability] [--format=format] [--output=file] [--version]
       [--help] command [arg...]
</pre>

####7. Поработать с программами пакета Shadow: gpasswd, grpck, newgrp, sg.

Что делает каждая из этих команд?  
Прислать примеры и скриншоты выполнения команд.

<pre>
gpasswd - команда делегирования прав на управление группой.
[root@shield ~]# gpasswd -A otus vagrant
[root@shield ~]# su - otus
Last login: Wed Sep 11 12:52:31 UTC 2019 on pts/0
[otus@shield ~]$ id utime
uid=1001(utime) gid=1001(utime) groups=1001(utime)
[otus@shield ~]$ gpasswd -a utime vagrant
Adding user utime to group vagrant
[otus@shield ~]$ id utime
uid=1001(utime) gid=1001(utime) groups=1001(utime),1000(vagrant)
[otus@shield ~]$ gpasswd -d utime vagrant
Removing user utime from group vagrant
[otus@shield ~]$ id utime
uid=1001(utime) gid=1001(utime) groups=1001(utime)
[otus@shield ~]$ exit
logout
[root@shield ~]# gpasswd -A "" vagrant
</pre>

<pre>
newgrp - команда смены основной группы в наследуемой сессии.
[root@shield ~]# id
uid=0(root) gid=0(root) groups=0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
[root@shield ~]# echo $SHLVL
1
[root@shield ~]# newgrp vagrant
[root@shield ~]# id
uid=0(root) gid=1000(vagrant) groups=1000(vagrant),0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
[root@shield ~]# touch a
# ls -la a
-rw-r--r--. 1 root vagrant 0 Sep 11 14:48 a
[root@shield ~]# echo $SHLVL
2
</pre>

<pre>
grpck - команда проверки файлов /etc/group и /etc/gshadow на корректность описания.
[root@shield ~]# grpck 
[root@shield ~]# echo $?
0
0 означает что все в порядке.
</pre>

<pre>
sg - команда для возможности исполнить другую указанную команду с правами другой группы.
# sg vagrant -c "touch b"
[root@shield ~]# ls -la b
-rw-r--r--. 1 root vagrant 0 Sep 11 15:08 b
</pre>
