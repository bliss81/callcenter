import os
import sys
file=open("/var/spool/asterisk/name.txt","r")
name1=file.readlines()
file.close()

#doron
print("sys",sys.argv)
ext=sys.argv[8]
ext1=ext.split("/")
ext=ext1[1]
print("ext",ext)

name=ext
for line in name1:
 lines=line.split("|")
 for i in lines:
  if ext in i:
   words=i.split(";")
   name=words[3]

print("new name",name)
file=open("/var/spool/asterisk/name.txt","w")
file.write(name)
file.close()
opp=""
argvnew=sys.argv


if "AA" in argvnew:
 argvnew = [w.replace("AA","'") for w in argvnew]
org=argvnew
org = [w for w in argvnew]

if "remove" in argvnew:
 argvnew2=argvnew[11]
 print("rrr",argvnew2)
 argvnew2=argvnew2[0:-2]
 argvnew2=argvnew2 + " penalty 0 as " + name + "'"
 argvtmp = argvnew
 argvtmp[11]=argvnew2
 
if "add" in argvnew:
 argvnew2=argvnew[11]
 print("rrr",argvnew2)
 argvnew2=argvnew2[0:-2]
 argvnew2=argvnew2 + " penalty 0 as " + name + "'"
 argvnew[11]=argvnew2
 org=argvnew
 org = [w for w in argvnew]
 
if "add" in argvnew:
 opp = [w.replace("add","remove") for w in argvnew]
 opp = [w.replace("to","from") for w in opp]
 opp[11]="'"
 print("new opp",opp)
elif "remove" in argvnew:
 opp = [w.replace("remove","add") for w in argvtmp]
 opp = [w.replace("from","to") for w in opp]
stopp=""
storg=""
j=0
for i in opp:
 j+=1
 if j > 1:
  if j<len(org):
   stopp+=i
   stopp+=" "
  else:
   stopp+=i
   stopp+="\n"
j=0
for i in org:
 j+=1
 if j > 1:
  if j<len(org):
   storg+=i
   storg+=" "
  else:
   storg+=i
   storg+="\n"
print("storg",storg)

file=open("/var/spool/cron/asterisk","r")
cron=file.readlines()
file.close()

if stopp in cron:
 print ("need to replace in file")
 stcron=""
 newcron = [w.replace(stopp,storg) for w in cron]
 print("new file: ",newcron)
 file=open("/var/spool/cron/asterisk","wb")
 for i in newcron:
  stcron += i
 file.writelines(newcron)
 file.close()
elif storg in cron:
 print ("noting to do")
else:
 print("append to file")
 file=open("/var/spool/cron/asterisk","wb")
 stcron=""
 for i in cron:
  stcron += i
 stcron+="\n"+storg
 file.write(stcron)
 file.close()
stream = os.popen('service crond restart')
output = stream.readlines()
print(output)
