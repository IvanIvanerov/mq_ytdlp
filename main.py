import paho.mqtt.client as mqtt
import json
import sys
import base64
from yt_dlp import YoutubeDL

MQ_TOPIC = sys.argv[2]
MQ_SERVER = sys.argv[1]
MQ_PORT = 1883
ydl_opts = {
        'format': 'best[height=1080][ext=mp4]/best[height<=1080][ext=mp4]/best',
        'outtmpl': sys.argv[3]+'/%(uploader)s/%(title)s.%(ext)s',
        'cachedir': False,
        'logtostderr': True
        }

def on_connect(mqttc, mosq, obj,rc):
    print("Connected with result code:"+str(rc))
    mqttc.subscribe(MQ_TOPIC,0)

def on_message(mosq,obj,msg):
    print(msg.payload.decode('utf-8'))
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(msg.payload.decode('utf-8'))
    mosq.publish('pong', 'ack', 0)
  
def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc,obj,level,buf):
    print("message:" + str(buf))
    print("userdata:" + str(obj))

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    client.connect(MQ_SERVER,MQ_PORT, 60)

    client.loop_forever()
