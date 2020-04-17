import pymysql
import pymysql.cursors
import time
import os
from datetime import datetime

class agent:
 def __init__(self,id,name,ext,queue="0",status="offline",duration="0",breaks="",callsanswered=0):
  self.ext=ext
  self.canswered = []
  self.name=name
  self.id=id
  self.queue=queue
  self.status=status
  self.duration=duration
  self.breaks=breaks
 def __repr__(self):
  return "([id={},name={},extension={},queue={},status={},duration={},answered: {}])".format(self.id,self.name,self.ext,self.queue,self.status,self.duration,self.canswered)
 def __str__(self):
  return "([id={},name={},extension={},queue={},status={},duration={},answered: {}])".format(self.id,self.name,self.ext,self.queue,self.status,self.duration,self.canswered)

class queue:
 def __init__(self,id,name,agents,avgwdur=0,avgcdur=0,waitingcalls=0,activecalls=0,abadonedcalls=0,callsanswered=0):
  self.canswered = callsanswered
  self.id=id
  self.name=name
  self.agents=agents
  self.avgwdur=avgwdur
  self.avgcdur=avgcdur
  self.waitingcalls=waitingcalls
  self.activecalls=activecalls
  self.abadonedcalls=abadonedcalls
 def __repr__(self):
  return "({},{},{},{},{})".format(self.id,self.name,self.agents,self.avgwdur,self.avgcdur,self.waitingcalls,self.activecalls,self.abadonedcalls)
 def __str__(self):
  return "(id={},name={},agents={}, avg waiting duration={}, average call duration ={}, waitingcalls={}, activecalls={}, abadonedcalls={})".format(self.id,self.name,self.agents,self.avgwdur,self.avgcdur,self.waitingcalls,self.activecalls,self.abadonedcalls)
  
# file.writelines(cont)
 #file.close()

def query(sql):
 connection = pymysql.connect(host='127.0.0.1',user='root',passwd='aacom0222',db='call_center',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
 with connection.cursor() as cursor:
  try:
   cursor.execute(sql)
   db = cursor.fetchall()
  except pymysql.ProgrammingError:
   pass
  except pymysql.Error:
   pass
  except pymysql.Warning:
   pass
  except Warning:
   pass
  
 return(db)
        
def prithtm(agentcalls,breaks,agentlist,abadonedcalls,waitingcalls,calldur,waitingdur,long,longactive,stats,asteriskonline):
 cont='''<?php
function _moduleContent(&$smarty, $module_name)
{
$content=' '''
 output='''<html><head><meta http-equiv="refresh" content="2"><center><h1> Sparrow Callcenter </h1></center>''' # the page will refresh every second
 #output='''<html><head><center><h1> Sparrow Callcenter </h1></center>''' # the page will refresh every second
 now = datetime.now()
 now = str(now.strftime("%d/%m/%y - %H:%M:%S"))
 output+='''<H2><center>{}</center></H2>'''.format(now)
 output+='''</head><style type="text/css">
table.floatedTable {
            float:left;
        }
table.inlineTable {
            display: inline-block;
        }
table.blueTable {
  border: 1px solid #1C6EA4;
  background-color: #EEEEEE;
  text-align: left;
  border-collapse: collapse;
}
table.blueTable td, table.blueTable th {
  border: 1px solid #AAAAAA;
  padding: 2px 10px;
}
table.blueTable tbody td {
  font-size: 20px;
}
table.blueTable tr:nth-child(even) {
  background: #E4F0F5;
}
table.blueTable thead {
  background: #1C6EA4;
  background: -moz-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
  background: -webkit-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
  background: linear-gradient(to bottom, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
  border-bottom: 2px solid #444444;
}
table.blueTable thead th {
  font-size: 15px;
  font-weight: bold;
  color: #FFFFFF;
  border-left: 2px solid #D0E4F5;
}
table.blueTable thead th:first-child {
  border-left: none;
}

table.blueTable tfoot {
  font-size: 14px;
  font-weight: bold;
  color: #FFFFFF;
  background: #D0E4F5;
  background: -moz-linear-gradient(top, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);
  background: -webkit-linear-gradient(top, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);
  background: linear-gradient(to bottom, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);
  border-top: 2px solid #444444;
}
table.blueTable tfoot td {
  font-size: 14px;
}
table.blueTable tfoot .links {
  text-align: right;
}
table.blueTable tfoot .links a{
  display: inline-block;
  background: #1C6EA4;
  color: #FFFFFF;
  padding: 1px 5px;
  border-radius: 5px;
}
</style><body><br><br>'''
 
 quelist=[]
 for q in qlist:
  quelist.append(queue(q,namelist[q],qlist[q]))
 
#waiting duration + call duration avg by queue table
 output+='<center><table border=1 class="inlineTable" align="center"> <tbody>'
 output+='<TH>Queue</TH><TH>Average Waiting Duration (sec)</TH><TH>Average Call Duration (min)</TH>'
 if calldur:
  for i in calldur: 
   try:  
    for j in quelist:
      if j.id==i["Queue"]:
       j.avgcdur=i["Average"]
   except IndexError:
    pass
 
 if waitingdur:
  for i in waitingdur:
   try:
    for j in quelist:
      if j.id==i["Queue"]:
       j.avgwdur=i["Waiting"]
   except IndexError:
    pass
   except KeyError:
    pass

 for j in quelist:
  output+='<TR><TD>{}</TD><TD>{}</TD><TD>{}</TD></TR>'.format(j.name,j.avgwdur,j.avgcdur)
 output+='<TR></TR></table></center><BR>'
 
#abadoned calls and active calls by queue table
 if waitingcalls:
  try:
   for i in waitingcalls:
    for j in quelist:
     if j.id==i["Queue"]:
      j.waitingcalls=i["Waiting"]
  except IndexError:
   pass	 
   
 if abadonedcalls:
  try:
   for i in abadonedcalls:
    for j in quelist:
     if j.id==i[1]:
      j.abadonedcalls=i[0]
  except IndexError:
   pass

 if agentcalls:
  for i in agentcalls:
   try: 
    for j in quelist:
     if j.id==i[1]:
      j.activecalls=i[0]
   except IndexError:	
    pass

 output+='<center><table border=1 class="inlineTable" align="center"> <tbody>'
 output+='<TH>Queue</TH><TH>Active Calls</TH><TH>Waiting Calls</TH><TH> Abadoned Calls</TH>'
 for j in quelist:
  output+='<TR><TD>{}</TD><TD>{}</TD><TD>{}</TD><TD>{}</TD></TR>'.format(j.name,j.activecalls,j.waitingcalls,j.abadonedcalls)
 output+='</table></center>'

#long waiting call warning (>30)
 if long:
  try:
   output+='Caller Waiting too long:<BR>'
   output+='<center><table><th>Queue Num</th><th>Waiting Time</th>'
   for i in long:
    output+='<TR><TD><font color="red">{}</TD><TD><font color="red"><blink>{}</blink></TD></TR>'.format(i["Queue"],i["Duration"])
  except IndexError:
   pass
 output+='</table></center>'

#long activeg call warning (>300)
 if longactive:
  try:
   output+='Call lasts too long:<BR>'
   output+='<center><table><th>Queue Num</th><th>Agent Name</th><th>Call Time</th>'	
   for j in longactive:
    output+='<TR><TD><font color="red">{}</TD><TD><font color="red"><blink>{}</blink><TD>{}</TD></TD></TR>'.format(j["Queue"],j["name"],j["Duration"])
  except IndexError:
   pass
 output+='</table></center><br>'

#status table by queue
		
 if stats:
  for g in stats:
   for k in agentlist:
    if g["id"]==k.id:
     k.canswered.append({g["Queue"],g["count(status)"]})
 for i in quelist:
  if i.id==3:
   output+='<center>'
   output+='<table border=1 class="inlineTable">'
   output+='<TH>Agent Name</TH><TH>Duration / Last Online</TH>'
   output+="<TR><TH>Queue:{}</TH><TD>{}</TD></TR>".format(i.id,i.name)
  else:
   output+='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
   output+='<table border=1 class="inlineTable">'
   output+='<TH>Agent Name</TH><TH>Duration / Last Online</TH>'
   output+="<TR><TH>Queue:{}</TH><TD>{}</TD></TR>".format(i.id,i.name)
  for j in agentlist:
   if j.id in i.agents:
    for v in asteriskonline: 
     for q,z in v.items():
      if q == i.id:
       if j.ext in z:
        if j.status=="online":
         output+='<TR><TD><font color="#53AB4D">{}</TD><TD><font color="#53AB4D">{}</TD></TR>'.format(j.name,j.duration)
        elif j.status == "active":
         output+='<TR><TD><font color="blue">{}</TD><TD><font color="blue">{}</TD></TR>'.format(j.name,j.duration)
        elif j.status == "break":
         output+='<TR><TD><font color="#e6b800">{}</TD><TD><font color="#e6b800">{}</TD></TR>'.format(j.name,j.duration)
  output+=' </table>' 
 output+=' <br>'
 output+=' <br>' 
 output+='</center>'
  
 #breaks table
 output+='<center><table border=1 class="inlineTable" align="center"> <tbody>'
 output+='<TH>agent id</TH><TH>Break type</TH><TH>Duration</TH>'
 if breaks:
  for row in breaks:
    output+='<TR><TD>{}</TD><TD>{}</TD><TD>{}</TD>'.format(row["aname"],row["Break"],row["Duration"])
  output+=' </table></center> </tbody>'
 else: 
  output+=' <TR><TD>No</TD><TD>Breaks</TD><TD>Yet</TD></TR>'
  #output +='</body></html>'
  cont+=output
 cont+=''' ';
 return $content;
 }
 ?>'''
 file = open("/var/www/html/modules/callcenter_doron/index.php", "w")
 file.writelines(cont)
 file.close()

def main():
    asteriskonline=[]
    for q in qlist:
     stream = os.popen('asterisk -x "queue show {}"'.format(q))
     output = stream.readlines()
     for i in range(len(output)):
      if i > 0 and i < (len(output)-1):
       words=output[i+1].split(" ")
       for j in words:
        sttt="0"       
        j=j.strip("(")
        j=j.strip(")")
        if "SIP/" in j:
         d={q:j}
         for a in asteriskonline:
          if d == a:
           sttt="1"
         if sttt=="0":
          asteriskonline.append({q:j})

#agent stats
    sql='''select count(status),agent.id ,id_queue_call_entry as Queue from call_entry inner join agent agent on agent.id = id_agent and DATE(datetime_init) = CURDATE()and status like "termi%" group by agent.name,Queue;'''
    stats=query(sql)	
#long active call	
    max2=59
    sql='''select agent.name ,id_queue_call_entry as Queue, timediff(now(),datetime_init) as Duration from call_entry inner join agent agent on agent.id = id_agent where (timediff(now(),datetime_init)>{})and  DATE(datetime_init) = CURDATE()and status like "activ%";'''.format(max2)
    longactive=query(sql)

    max=30
    sql='''select id_agent as Agent,id_queue_call_entry as Queue, TIMEDIFF(now(), datetime_entry_queue) as Duration from call_entry where (TIMEDIFF(now(),datetime_entry_queue)>{}) and status like "en-cola";'''.format(max)
    longwaiting=query(sql)
	
#avg waiting duration by queue
    sql='''select id_queue_call_entry as Queue, truncate(avg(duration_wait),1) as Waiting from call_entry where duration_wait is not NULL and DATE(datetime_entry_queue) = CURDATE() group by id_queue_call_entry;'''	
    waitingdur=query(sql)
		
#avg call duration by queue
    sql='''select id_queue_call_entry as Queue,truncate((sum(duration)/count(duration))/60,1) as Average from call_entry where status like "terminada" and DATE(datetime_init) = CURDATE() and DATE(datetime_end) = CURDATE() group by id_queue_call_entry;'''
    calldur=query(sql)	

#waiting calls by queue
    sql='''select id_queue_call_entry as Queue, count(*) as Waiting from call_entry where status like "en-cola" group by id_queue_call_entry;'''
    waiting=query(sql)
#agent break report for table
    sql='''select a.id_agent as ID, ag.name as aname, b.name as Break, datetime_init as Start, datetime_end as End, duration as Duration 
		   from audit a inner join break b on a.id_break = b.id inner join agent ag on a.id_agent = ag.id where DATE(datetime_init) = curdate() and date(datetime_end) = curdate();'''
    breaks=query(sql)

    agentcalls=[]	
#current active calls by queues for table
    sql = '''select id_queue_call_entry as Queue, count(*) as Calls from call_entry where status like "activa" and DATE(datetime_init) = CURDATE() and DATE(datetime_end) is null group by id_queue_call_entry;'''
    db=query(sql)
    for row in db:
     agentcalls.append((str(row["Calls"]),row["Queue"]))

#current abadoned calls by queues for table
    sql = '''select id_queue_call_entry as Queue, count(*) as Missed from call_entry where status like "abandonada" and DATE(datetime_end) = CURDATE() group by id_queue_call_entry;'''
    db=query(sql)
    abadonedcalls=[]
    for row in db:
     abadonedcalls.append((str(row["Missed"]),row["Queue"]))
	 

#active calls per agent for status
    sql='''select entry.id_queue_call_entry as Queue, entry.id_agent as ID, agent.name as Name, TIMEDIFF(now(), datetime_init) as Duration 
		   from call_entry entry inner join agent agent on agent.id = entry.id_agent where status like "activa" and date(datetime_init) = curdate() and date(datetime_end) is null;'''
    activeagents=query(sql)
	#all agents for status
    sql=''' select name,id from agent;'''
    allagents=query(sql)

    sql='''select id_queue_call_entry as Queue,duration_wait as Waiting from call_entry where DATE(datetime_entry_queue) = CURDATE() and (duration_wait > 60);'''
    highwait=query(sql)

	#online not active agent & not in break for status
    sql='''select ag.id, ag.name,ag.number, ad.id_break as brk, ad.datetime_init as Started, TIMEDIFF(NOW(), ad.datetime_init) as Duration,ad.datetime_end as ended from audit ad inner join agent ag on ad.id_agent = ag.id where ad.datetime_init is not null and ad.datetime_end is null and DATE(ad.datetime_init) = CURDATE();'''
    onlineagents=query(sql)
    agentlist=[]
    bbk=""
	#inserting to lists
    
    if onlineagents:    
     for x in onlineagents:
      nn="SIP/"+str(x["number"])
      for v in asteriskonline:
       for key,value in v.items():
        if nn in value:
         stt="0"
         sssst="0"
         if not x["brk"]:
          for y in activeagents:
           if x["id"] == y["ID"]:
            agentlist.append(agent(x["id"],x["name"],x["number"],"","active",x["Duration"],""))
            stt="1"
          if stt !="1":
           for cc in agentlist:
            if cc.id == x["id"]:
             sssst="1"
           if sssst != "1":
            agentlist.append(agent(x["id"],x["name"],x["number"],"","online",x["Duration"],""))
         else: 	 
          agentlist.pop()
          agentlist.append(agent(x["id"],x["name"],x["number"],"","break",x["Duration"],"2"))
      '''for x in allagents:
        stt="0"
        for y in onlineagents:
         if x["id"] == y["id"]:
          stt="1"'''
    prithtm(agentcalls,breaks,agentlist,abadonedcalls,waiting,calldur,waitingdur,longwaiting,longactive,stats,asteriskonline) # send for html table 
	
#print 'Content-type:text/html\n'
print("The data will be updated at /var/www/html/1.htm every 1 second")
########################################################################################### 
qlist={3:[8,10,11,12,13,14,15],4:[8,10,11,12,13,14,15],5:[8,10,11,12,13,14,15]} #static agents by queues	
namelist={3:"IP",4:"CORAL",5:"Test"}
########################################################################################### 
while True:
 main() 
 time.sleep(1)
 # the data will be updated every second
