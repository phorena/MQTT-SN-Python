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
def test_subscribe(topic, qos=0, wait1=1, wait2=2):
  mystring = f"""
  %%%%%%%%%%%%%%%%%%%%%%%%
  test_subscribe
  1. Connect
  2. Wait for ConnAck
  3. Run loop_start()
  4. Wait {wait1} sec
  5. Subscribe
      a. qos: {qos}
  6. Wait {wait2} sec
  %%%%%%%%%%%%%%%%%%%%%%%%"""
  print(mystring)

  parameters = {
    "qos": qos,
    "wait1": wait1,
    "wait2": wait2,
  }
  print(parameters)
  client = Client("linh")#change so only needs name
  client.message_arrived_flag=False
  client.registerCallback(MyCallback())
  client.connected_flag=False
  client.set_will("sub0", "disconnect now", 0, False)

  client.connect(host,port,duration=30, cleansession=True, will=False)
  client.lookfor(MQTTSN.CONNACK)
  try:
    if client.waitfor(MQTTSN.CONNACK)==None:
        print("connection failed")
        raise SystemExit("no Connection quitting")
  except:
    print("connection failed")
    raise SystemExit("no Connection quitting")

  client.loop_start() #start loop
  time.sleep(wait1)
  print ("threads ",threading.activeCount()) 
  while True:
    topic1_id,rc = client.subscribe(topic, qos)
    if rc==None:
      print("subscribe failed")
      raise SystemExit("Subscription failed quitting")
    if rc==0:
      print("topic1_id",topic1_id)
      break
  try:
    while True:
      time.sleep(1)
      empty_queue(0)
      pass
  except KeyboardInterrupt:
      print ("You hit control-c")

def test_connect(cleansession, will, duration, wait1=5, wait2=2):
  mystring = f"""
  %%%%%%%%%%%%%%%%%%%%%%%%
  test_connect
  1. Connect with: 
      a. cleansession: {cleansession}
      b. will: {will}
      c. duration: {duration}
  2. Wait for ConnAck
  3. Run loop_start()
  4. Wait {wait1} sec
  5. Disconnect()
  6. Wait {wait2} sec
  %%%%%%%%%%%%%%%%%%%%%%%%"""
  print(mystring)

  parameters = {
    "duration": duration,
    "wait1": wait1,
    "wait2": wait2,

  }
  print(parameters)
  client = Client("linh")#change so only needs name
  client.message_arrived_flag=False
  client.registerCallback(MyCallback())
  client.connected_flag=False
  client.set_will("sub0", "disconnect now", 0, False)

  client.connect(host,port,duration, cleansession, will)
  client.lookfor(MQTTSN.CONNACK)
  try:
    if client.waitfor(MQTTSN.CONNACK)==None:
        print("connection failed")
        raise SystemExit("no Connection quitting")
  except:
    print("connection failed")
    raise SystemExit("no Connection quitting")

  client.loop_start() #start loop
  time.sleep(wait1)

  client.disconnect()

  time.sleep(wait2)
  client.loop_stop() #stop loop
  assert client.connected_flag == False
  time.sleep(disconnect_time)
  return client
  

#if __name__ == "__main__":
host="127.0.0.1"
port=60000
#m_port=1885 #port gateways advertises on
#m_group="225.0.18.83" #IP gateways advertises on

# test_subscribe("hello", 0)
# 
# test_connect(cleansession=True, will=False, duration=10)
# test_connect(cleansession=True, will=True, duration=10)
# test_connect(cleansession=False, will=True, duration=10)
# test_connect(cleansession=False, will=False, duration=10)
# 
# # Connection timeout because wait1=15 while duration=10
# test_connect(cleansession=True, will=False, duration=10, wait1=15)
