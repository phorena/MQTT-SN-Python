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

import time
from os import path
import ssl
from socket import socket, AF_INET, SOCK_DGRAM
from logging import basicConfig, DEBUG
basicConfig(level=DEBUG)  # set now for dtls import code
from dtls import do_patch

do_patch()

cert_path = path.join(path.abspath(path.dirname(__file__)), "certs")
s = ssl.wrap_socket(socket(AF_INET, SOCK_DGRAM), cert_reqs=ssl.CERT_NONE, ca_certs=path.join(cert_path, "ca-cert.pem"))
s.connect(('127.0.0.1', 61003))

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



client.set_dtls_socket(s)
print(s.getpeername())
print(s.getsockname())




client.message_arrived_flag=False
client.registerCallback(MyCallback())

print ("threads ",threading.activeCount()) 
print("connecting ",host)
client.connected_flag=False

client.connect(host,port)

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
print("topic for topic1 is", topic1)
print("connected now subscribing")
while True:
  topic1_id,rc = client.subscribe(topic1, 0)
  if rc==None:
    print("subscribe failed")
    raise SystemExit("Subscription failed quitting")
  if rc==0:
    print("subscribed ok to ",topic1)
    print("topic1_id",topic1_id)
    break

topic1=3345

msg_cnt = 1

# print("disconnecting")
try:
  while True:
    # client.publish(topic1, msg, qos=2, retained=False)
    msg_cnt += 1
    msg="aaaaa" + str(msg_cnt)
    client.publish(topic1, msg, qos=1, retained=True)
    time.sleep(3)
    pass

except KeyboardInterrupt:
    print ("You hit control-c")


print ("threads ",threading.activeCount()) 

print("disconnecting")
client.disconnect()

client.loop_stop()
