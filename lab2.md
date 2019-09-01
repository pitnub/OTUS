### Задание 1: Получение информации от dns серверов

#### Получение IP-адреса для доменного имени opu.ua
##### vagrant@sword:~$ host opu.ua
opu.ua has address 91.194.79.77  

##### vagrant@sword:~$ nslookup opu.ua
Non-authoritative answer:  
Name:	opu.ua  
Address: 91.194.79.77

##### vagrant@sword:~$ dig opu.ua
;; ANSWER SECTION:  
opu.ua.			486	IN	A	91.194.79.77  

#### Получение информации о DNS-серверах домена opu.ua
##### vagrant@sword:~$ dig -t ns opu.ua
;; ANSWER SECTION:  
opu.ua.			17027	IN	NS	ns1.opu.ua.  
opu.ua.			17027	IN	NS	ns2.opu.ua.  

#### Таблица запросов с текущим и доверенным NS-серверами
| dig/NS | default | @ns1.opu.ua |
| --- | --- | --- |
| NS | NS ns1.opu.ua<br>NS ns2.opu.ua | NS ns1.opu.ua<br>NS ns2.opu.ua<br>NS ns1.secondary.net.ua<br>NS ns2.secondary.net.ua |
| ANY | NS ns1.opu.ua<br>NS ns2.opu.ua | SOA ns1.opu.ua. hostmaster.opu.ua. 2015042189 3600 1800 604800 86400<br>opu.ua. 86400	IN	NS	ns2.secondary.net.ua<br>NS	ns1.opu.ua<br>NS ns1.secondary.net.ua<br>NS	ns2.opu.ua<br>A	91.194.79.77<br>MX 1 aspmx.l.google.com<br>MX 10 alt4.aspmx.l.google.com<br>MX 5 alt2.aspmx.l.google.com<br>MX 5 alt1.aspmx.l.google.com<br>MX 10 alt3.aspmx.l.google.com<br>TXT "MS=ms22769637"<br>TXT	"google-site-verification=2Hrp82qq9NeOs1GUPu12_My2zfxIL80jquzz0I9JaDI"<br>TXT "google-site-verification=gV-KF-d4bIFsJetXVLImF27Z_Qr2NeU5Ko10JeMviyc"<br>TXT	"google-site-verification=gpIQ4WW6aEC61Aw_83i9pQb5KH8F8tMUTmCsn5CiwuM"<br>;; ADDITIONAL SECTION:<br>ns1.opu.ua.	86400 IN A 195.22.132.2<br>ns2.opu.ua. 86400 IN	A 195.22.132.22 |
| AXFR | communications error to 10.0.2.3#53: end of file | Transfer failed |
| TXT | TXT "google-site-verification=gV-KF-d4bIFsJetXVLImF27Z_Qr2NeU5Ko10JeMviyc"<br>TXT	"MS=ms22769637"<br>TXT	"google-site-verification=2Hrp82qq9NeOs1GUPu12_My2zfxIL80jquzz0I9JaDI"<br>TXT "google-site-verification=gpIQ4WW6aEC61Aw_83i9pQb5KH8F8tMUTmCsn5CiwuM" | TXT "google-site-verification=gV-KF-d4bIFsJetXVLImF27Z_Qr2NeU5Ko10JeMviyc"<br>TXT	"MS=ms22769637"<br>TXT	"google-site-verification=2Hrp82qq9NeOs1GUPu12_My2zfxIL80jquzz0I9JaDI"<br>TXT "google-site-verification=gpIQ4WW6aEC61Aw_83i9pQb5KH8F8tMUTmCsn5CiwuM" |
| PTR | ANSWER: 0 | ;; AUTHORITY SECTION:<br>opu.ua. 86400	IN	SOA	ns1.opu.ua. hostmaster.opu.ua. 2015042189 3600 1800 604800 86400 |

Q: Что такое записи ANY,TXT,AXFR,PTR,А ?  
A: Все записи,специальная информация,получение всей зоны,запись IP-host,запись host-IP.

Q: Что такое запись SOA ?  
A: Служебная информация о зоне.  

Q: Что такое NS ?  
A: Запись о серверах доменных имен.

Q: Какие DNS сервера бывают ? (вендор)  
A: bind, microsoft DNS, google dns.

Q: С каким dns сервером взаимодействовали вы ?  
A: Bind, microsoft DNS, google dns.

Q: Что такое атака zone transfer и чем она не безопасна как в локальных так и во внешних сетях ?  
A: Получение всей информации о зоне. Является источником информации для проведения атак.

### Задание 2: Поиск информации у регистратора по заданному домену

| | Информация о домене opu.ua | Информация о домене ptsecurity.com |
| -- | -- | -- |
| Владелец | ODESSA NATIONAL POLYTECHNIC UNIVERSITY | Positive Technologies, CJSC |
| Почтовые адреса | noc@opu.ua | domreg@ptsecurity.ru |
| Физические адреса | UA 65044 ODESSA Shevchenko ave. 1 | RU 109439 Moscow 23A Schelkovskoe schosse |	
| IP адреса | 195.22.132.2, 195.22.132.22 | |
| Телефоны | +380.487348340 | +7.4957440144 |		
| ДНС сервера | ns1.opu.ua, ns2.opu.ua | ns1.p23.dynect.net, ns2.p23.dynect.net, ns3.p23.dynect.net, ns4.p23.dynect.net |		
| DNSSEC | | unsigned |

### Задание 3: Использование поисковых движков

| Данные/Поисковик | 2ip.ru | 
| -- | -- |
| Информация об IP адресе или домене | 91.194.79.77<br>vps-md7831.tenet.ua<br>Odessa, Ukraine
| IP интернет ресурса | 91.194.79.77 - opu.ua |
| Система управления сайтом (CMS) | найдены признаки использования Drupal |
| Хостинг сайта | Украина, Белгород-Днестровский |
| Информация о сайте | Одеський національний політехнічний університет<br>Apache/2.2.15 (CentOS)<br>Let's Encrypt to 2019-09-25 |
| Сайты на одном IP | Домены не найдены |
| Все домены одного владельца | нет возможности проверить домен .ua |
| DNS параметры домена | ANY: opu.ua.	83691	IN	A	91.194.79.77 |
| Поиск доменного имени | занят |
| Определение IP адреса по Е-mail | нет возможности проверить |
| Информация об AS (автономных системах) принадлежащих искомой цели и адреса блоков, которые им соответствуют | AS:AS6876<br>91.194.78.0/23 |

### Задание 4: Поиск информации о суб-доменах по заданному домену

| Найденные суб-домены |
| -- |
| old.opu.ua |
| catalog.library.opu.ua |
| ac.opu.ua |
| immm.opu.ua |
| hsf.opu.ua |
| www.ac.opu.ua |
| fs.opu.ua |
| pratsi.opu.ua |
| dspace.opu.ua |
| career.opu.ua |
| beiti.opu.ua |
| pei.opu.ua |
| www.dei.opu.ua |
| fspirki.opu.ua |
| hait.opu.ua |
| summerschool.opu.ua |
| etks.opu.ua |
| library.opu.ua |
| if.opu.ua |
| ugi.opu.ua |
| oadk.opu.ua |
| staffer.opu.ua |
| acm.opu.ua |
| www.irt.opu.ua |
| usec.opu.ua |
| mbei.opu.ua |
| mrot.opu.ua |
| el.opu.ua |
| economics.opu.ua |
| ics.opu.ua |
| ui.opu.ua |
| cisn.opu.ua |
| itdmi.opu.ua |
| fspi.opu.ua |
| upec.opu.ua |
| ctf.opu.ua |
| syssoftdep.opu.ua |
| usi.opu.ua |
| imi.opu.ua |
| irt.opu.ua |
| eltecs.opu.ua |
| upi.opu.ua |
| emd.opu.ua |
| zpo.opu.ua |
| aspirant.opu.ua |
| mip.opu.ua |
| ccs.opu.ua |
| cs.opu.ua |
| eei.opu.ua |
| dei.opu.ua |
| www.ceet.opu.ua |
| edu.opu.ua |

Q: Какую информацию вы получили на выходе ?  
A: Список под-доменов основного домена opu.ua.

Q: Где можно применить эту информацию ?  
A: В анализе инфраструктуры организации.

### Задание 5: Поиск информации у DNS серверов по заданному домену

#### $dnsrecon -d opu.ua
| Тип записи | Доменное имя | IP адрес/data |
| -- | -- | -- |
| SOA | ns1.opu.ua | 195.22.132.2 |
| NS | ns1.opu.ua | 195.22.132.2 |
| NS | ns2.opu.ua | 195.22.132.22 |
| MX | alt4.aspmx.l.google.com | 74.125.28.27 |
| MX | alt3.aspmx.l.google.com | 74.125.204.27 |
| MX | aspmx.l.google.com | 74.125.133.27 |
| MX | alt1.aspmx.l.google.com | 108.177.14.26 |
| MX | alt2.aspmx.l.google.com | 172.217.194.26 |
| MX | alt4.aspmx.l.google.com | 2607:f8b0:400e:c04::1b |
| MX | alt3.aspmx.l.google.com | 2404:6800:4008:c04::1a |
| MX | aspmx.l.google.com | 2a00:1450:400c:c0c::1b |
| MX | alt1.aspmx.l.google.com | 2a00:1450:4010:c0f::1b |
| MX | alt2.aspmx.l.google.com | 2404:6800:4003:c04::1a |
| A | opu.ua | 91.194.79.77 |
| TXT | opu.ua | google-site-verification=gpIQ4WW6aEC61Aw_83i9pQb5KH8F8tMUTmCsn5CiwuM |
| TXT | opu.ua | google-site-verification=2Hrp82qq9NeOs1GUPu12_My2zfxIL80jquzz0I9JaDI |
| TXT | opu.ua | google-site-verification=gV-KF-d4bIFsJetXVLImF27Z_Qr2NeU5Ko10JeMviyc |
| TXT | opu.ua | MS=ms22769637 |

Bind Version for 195.22.132.22 9.10.3-P4-Debian

#### $dnsenum opu.ua
| Имя | Запись | IP |
| -- | -- | -- |
| opu.ua. | A | 91.194.79.77 |
| ns2.opu.ua. | A | 195.22.132.22 |
| ns1.opu.ua. | A | 195.22.132.2 |
| alt4.aspmx.l.google.com. | A | 74.125.28.26 |
| alt3.aspmx.l.google.com. | A | 74.125.204.26 |
| aspmx.l.google.com. | A | 74.125.206.26 |
| alt1.aspmx.l.google.com. | A | 108.177.14.27 |
| alt2.aspmx.l.google.com. | A | 172.217.194.27 |

#### $dnsmap opu.ua
| Имя | IP |
| -- | -- |
| ac.opu.ua | 195.138.69.237 |
| cs.opu.ua | 91.194.79.34 |
| dc.opu.ua | 91.194.79.34 |
| dl.opu.ua | 195.22.133.117 |
| ei.opu.ua | 91.194.79.34 |
| el.opu.ua | 195.22.133.117 |
| email.opu.ua | 195.22.132.15 |
| fs.opu.ua | 185.53.160.206 |
| groups.opu.ua | 2a00:1450:4017:801::2013 |
| groups.opu.ua | 172.217.17.211 |
| if.opu.ua | 91.194.79.34 |
| library.opu.ua | 91.194.79.34 |
| m.opu.ua | 195.22.133.16 |
| mail.opu.ua | 2a00:1450:4017:801::2013 |
| mail.opu.ua | 172.217.17.211 |
| mi.opu.ua | 91.194.79.34 |
| nc.opu.ua | 195.22.133.34 |
| net.opu.ua | 91.194.79.34 |
| ns1.opu.ua | 195.22.132.2 |
| ns2.opu.ua | 195.22.132.22 |
| pop3.opu.ua | 195.22.132.15 |
| sa.opu.ua | 91.194.79.34 |
| smtp.opu.ua | 195.22.132.15 |
| staging.opu.ua | 91.194.79.34 |
| ui.opu.ua | 91.194.79.34 |
| www.opu.ua | 91.194.79.77 |

Q: Какую еще информацию вы почерпнули из вывода команды ?  
A: Адреса серверов организации, кроме того определили вендора и версию ДНС-сервера (Bind 9.10.3-P4-Debian)

Q: Где можно применить эту информацию ?  
A: Дополнительные цели для анализа.

#### $dnsrecon -d opu.ua -t brt -D /usr/share/wordlists/dnscan/subdomains-10000.txt
Q: Какие дополнительные результаты принес нам этот словарь ?  
A: Примерно в 5 раз больше записей.

### Задание 6: Рассмотрите дополнительные утилиты для сбора информации
Приведенные утилиты собирают примерно ту же информацию что уже собрана.

### Задание 7: История DNS имён
#### IP history results for opu.ua.
| IP Address | Location	IP Address | Owner | Last seen on this IP |
| -- | -- | -- | -- |
| 91.194.79.77 | Ukraine | Odessa, Ukraine | 2019-06-24 |
| 91.194.79.34 | Ukraine | Odessa, Ukraine | 2019-06-17 |
| 143.95.249.223 | Los Angeles - United States | Athenix Inc. | 2017-10-03 |
| 195.138.69.237 | Odesa - Ukraine | TeNeT Networking Centre | 2016-08-25 |
| 143.95.249.223 | Los Angeles - United States | Athenix Inc. | 2016-07-15 |

### Задание 8: Поиск сертификатов
В последнее время используются для серверов домена opu.ua только "C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3".

### Задание 9: Поиск информации о почтовых ящиках по заданному домену
$ theharvester -d opu.ua -b all
К сожалению нулевой результат...

### Задание 10: Агрегированный поиск информации
#### $dmitry opu.ua

Собранная информация идентична уже собранной, за исключением:  
Gathered E-Mail information for opu.ua: aait@opu.ua  
Gathered TCP Port information for 91.194.79.77  

| Port | State |
| -- | -- |
| 21/tcp | open |
| 80/tcp | open |

