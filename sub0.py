#! c:\python34\python3
#!/usr/bin/env python
##demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
##Free to use for any purpose
##If you like and use this code you can
##buy me a drink here https://www.paypal.me/StepenCope
import signal
import queue
import struct
import threading
import time
import sys
# sys.path.append('c:/python34/steve/mqttsclient/client')
print(sys.version_info)

from MQTTSNclient import Callback
from MQTTSNclient import Client
from MQTTSNclient import publish
import MQTTSN
message_q=queue.Queue()

class MyCallback(Callback):
  def on_message(self,client,TopicId,TopicName, payload, qos, retained, msgid):
    m= "d-p-Arrived" +" topic  " +str(TopicId)+ "message " +\
       str(payload) +"  qos= " +str(qos) +" ret= " +str(retained)\
       +"  msgid= " + str(msgid)
    #print("got the message ",payload)
    message_q.put(payload)
    return True

######
def empty_queue(delay=0):
    while not message_q.empty():
      m=message_q.get()
      print("Received message  ",m)
    if delay!=0:
      time.sleep(delay)
########

#if __name__ == "__main__":
host="127.0.0.1"
port=60000
#m_port=1885 #port gateways advertises on
#m_group="225.0.18.83" #IP gateways advertises on

client = Client("linh")#change so only needs name
client.message_arrived_flag=False
client.registerCallback(MyCallback())

print ("threads ",threading.activeCount()) 
print("connecting ",host)
client.connected_flag=False
client.set_will("disconnect sub0", "now", 0, False)
client.connect(host,port,duration=64, will=False)

client.lookfor(MQTTSN.CONNACK)
try:
  if client.waitfor(MQTTSN.CONNACK)==None:
      print("connection failed")
      raise SystemExit("no Connection quitting")
except:
  print("connection failed")
  raise SystemExit("no Connection quitting")
  
client.loop_start() #start loop
print ("threads ",threading.activeCount()) 
topic1="mqttsn-test"
topic1="abc"
topic0=0
topic1=100
print("topic for topic1 is", topic1)
print("connected now subscribing")
while True:
  topic0_id,rc = client.subscribe(topic0,0)
  if rc==None:
    print("subscribe failed")
    raise SystemExit("Subscription failed quitting")
  if rc==0:
    print("subscribed ok to ",topic0)
    print("topic0_id",topic0_id)

  topic1_id,rc = client.subscribe(topic1,0)
  if rc==None:
    print("subscribe failed")
    raise SystemExit("Subscription failed quitting")
  if rc==0:
    print("subscribed ok to ",topic1)
    print("topic1_id",topic1_id)
    break

try:
  while True:
    time.sleep(1)
    empty_queue(0)
    pass
except KeyboardInterrupt:
    print ("You hit control-c")


print ("threads ",threading.activeCount()) 

print("disconnecting")
client.disconnect()

client.loop_stop()
