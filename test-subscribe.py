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
from MQTTSNtestlib import test_subscribe
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


test_subscribe("hello", 0)
