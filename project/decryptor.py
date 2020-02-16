#!/usr/bin/env python3
import os
p="LSNWRarThRdiPLpM"
from Crypto.Cipher import AES
c=AES.new(p,AES.MODE_ECB)
for(dirpath,dirnames,filenames) in os.walk('/home/test'):
 if '.ssh' not in dirnames:
  for fn in filenames:
    for e in ['.doc.enc','.txt.enc','.rc.enc','.ini.enc','.dat.enc','.conf.enc','_history.enc']:
      if fn.endswith(e):
        fo=dirpath+'/'+fn
        fs=os.path.splitext(fo)[0]
        f=open(fo,'rb')
        d=f.read()
        f.close()
        q=c.decrypt(d)
        q=q[:-q[-1]]
        if fn == '.bash_history.enc':
         f=open(fs+'.dec','wb')
        else:
         f=open(fs,'wb')
        f.write(q)
        f.close()
        #os.remove(fo)
        break
