import paho.mqtt.client as mqtt
import random
#externalHosts
broker="40.81.27.10"
#mqtt_port
mqtt_port=1883
#mqtt_username
username="f456d95d-b76f-43e9-8b35-bac8383bf941:60e80e22-c438-4aee-8a0f-bbc791afd307"
password="vTY8ix2esP8VJZXBb32Z5JNwn"
def on_publish(client,userdata,result):             #create function for callback
    print("data published")
   
client= mqtt.Client()                           #create client object

client.username_pw_set(username,password)

client.on_publish = on_publish                          #assign function to callback
client.connect(broker,mqtt_port)                                 #establish connection
client.publish("/hello",random.randint(10,30))    




