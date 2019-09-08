import paho.mqtt.client as mqtt #import the client1
import time
import Adafruit_DHT as DHT #sensor module
import struct #packing module
import RPi.GPIO as GPIO

sensor = DHT.DHT11 #sensor type
DHT11 = 17 #sensor pin
broker_address="test.mosquitto.org" #Mqtt broker address


def getdata(): #this function retrieves, converts, then packs data for transport
    global data
    h, t = DHT.read_retry(sensor, DHT11) #read sensor
    f = t*1.8+32 #converstion
    data = struct.pack('ff', h, f) #packing for transport


def publishdata(): #publishes the data to mqtt broker
    client = mqtt.Client("P1") #create new instance
    client.connect(broker_address) #connect to broker
    client.subscribe("joe/tests") #this should be a specific topic to each sensor
    client.publish("joe/tests",data) #publishes data to broker
    time.sleep(2) #waits for new data
    
def destroy(): #clean exit
   time.sleep(0.01)
    
if __name__ == '__main__':    
    try:
        while True:
            getdata()
            publishdata()            
    except KeyboardInterrupt:
        destroy()
            