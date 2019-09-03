import paho.mqtt.client as mqtt #mqtt client
import time
import RPi.GPIO as GPIO
import struct #packing module
import configparser #Reads config file


led = 23 #led pin number
broker_address="test.mosquitto.org" #broker address
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)
config = configparser.RawConfigParser() #configparser setup

#function that runs when an mqtt message is recieved
def on_message(client, userdata, message):
    data = message.payload #message from broker
    datau = struct.unpack('ff', data) #unpacking data from sensor
    h, t = datau #assigning temp and humidty values from data
    config.read('test.txt') #read config file
    thresh = int(config.get('setup', 'thresh')) #sets threshold for activation
    if 96 > h > thresh: #checks if sensor value is over the threshold
       GPIO.output(led,GPIO.HIGH)
    else:
       GPIO.output(led,GPIO.LOW)

      
client = mqtt.Client("joe") #create new instance        
client.on_message=on_message #run on message function when message recieved
client.connect(broker_address) #connect to broker
client.subscribe("joe/tests")#subscribe to topic
client.loop_forever() #run forever