# MQTT to HTTP sender

This is very simple MQTT (broker) to HTTP (webserver) bridge, aka. value sender. Script is waiting on background for MQTT Pub messages. If message is received, payload (value) is send as HTTP GET request to webserver.

Code is easy to read. Ready for demonizing.
