import sys
file=open("/var/spool/asterisk/name.txt","wb")
for i in sys.stdin:
 print("name",i)
 file.write(i)
file.close()    


