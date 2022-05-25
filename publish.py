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
 #sys.path.append('c:/python34/steve/mqttsclient/client')

##

from MQTTSNclient import Callback
from MQTTSNclient import Client
from MQTTSNclient import publish
import MQTTSN
message_q=queue.Queue()

######
def empty_queue(delay=0):
    while not message_q.empty():
      m=message_q.get()
      print(m)
    if delay!=0:
      time.sleep(delay)
########


host="127.0.0.1"
port=60000
m_port=1883 #port gateways advertises on
m_group="225.1.1.1" #IP gateways advertises on

client = Client("linh_pub")#change so only needs name

client.registerCallback(Callback())

print ("threads ",threading.activeCount()) 
print("connecting ",host)
client.connected_flag=False

client.set_will("publish disconnect111", "now", 0, False)
client.connect(host,port,will=False)
client.loop_start()
client.lookfor(MQTTSN.CONNACK)
try:
  if client.waitfor(MQTTSN.CONNACK)==None:
      print("connection failed")
      raise SystemExit("no Connection quitting")
except:
  print("connection failed")
  raise SystemExit("no Connection quitting")


topic1=100

msg="aaaaa"
time.sleep(1)
# print("topic id=",topic1)
# client.publish(topic1,msg)
client.publish(topic1,msg, qos=2, retained=True)
# print("disconnecting")
time.sleep(200) # wait for message to be received and replied with pub_ack
client.disconnect()
# print ("threads ",threading.activeCount()) 
empty_queue(4)
client.loop_stop()



