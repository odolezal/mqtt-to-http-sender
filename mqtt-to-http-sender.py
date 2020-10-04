################################
# MQTT to HTTP sender
# Based on:
# http://wiki.tmep.cz/doku.php?id=zarizeni:raspberry_pi
# https://techtutorialsx.com/2017/04/23/python-subscribing-to-mqtt-topic/
# https://stackoverflow.com/questions/41624697/mqtt-python-subscribe-to-multiple-topics-and-write-payloads-on-raspberry-lcd
# https://mntolia.com/mqtt-python-with-paho-mqtt-client/
#
# Little bit a code by:
# https://github.com/odolezal
#############################

import time
import paho.mqtt.client as paho
import httplib2

# MQTT broker setting
broker_url = "localhost"
broker_port = 1883
broker_timeout = 30
broker_username = "user"
broker_password = "password"

def on_connect(mqttc, userdata, flags, rc):
  if rc == 0:
   print("Connected With Result Code: {}".format(rc))
  else:
   print("Error! Not connected to broker.")

def on_disconnect(mqttc, userdata, rc):
   print("Client Got Disconnected")

# MQTT handler
mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.username_pw_set(username=broker_username, password=broker_password)
mqttc.connect(broker_url, broker_port, broker_timeout)

print("MQTT to HTTP sender")

# Topic 1 - device1/topic1
def on_message_topic1(mosq, obj, msg):
    print "Topic: " + msg.topic
    print "Message payload: " + msg.payload

    # HTTP request
    url = "http://somesubdomain1.example1.com/?"
    guid = "someGUID1"
    requesturl = url + guid + "=" + msg.payload
    print("Request URL: " + requesturl)
    resp, content = httplib2.Http().request(requesturl)
    if resp.status == 200:
     print("OK. Sended to server.")
    else:
     print("Error! Connection to webserver failed!")
    print(" ")

# Topic 2 - device2/topic2
def on_message_topic2(mosq, obj, msg):
    print "Topic: " + msg.topic
    print "Message payload: " + msg.payload
    print " "

    # HTTP request
    url = "http://somesubdomain2.example2.com/?"
    guid = "someGUID2"
    requesturl = url + guid + "=" + msg.payload
    print("Request URL: " + requesturl)
    resp, content = httplib2.Http().request(requesturl)
    if resp.status == 200:
     print("OK. Sended to server.")
    else:
     print("Error! Connection to webserver failed!")
    print(" ")
	
# Topic 3 - device3/topic3
# etc...

# Topic for other undefined/unhandled messages
def on_message(mosq, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

mqttc.on_message = on_message

# Subscribe to "parent" topic. Use "#" for root on broker (subscribe to all topics).
mqttc.subscribe("#")

# Add message callbacks that will only trigger on a specific subscription match
mqttc.message_callback_add('device1/topic1', on_message_topic1)
mqttc.message_callback_add('device2/topic2', on_message_topic2)

# Run endless loop
mqttc.loop_forever()