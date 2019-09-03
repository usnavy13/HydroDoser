import paho.mqtt.client as mqtt #import the client1
import time
import Adafruit_DHT as DHT
import struct
import RPi.GPIO as GPIO

sensor = DHT.DHT11
DHT11 = 17
broker_address="test.mosquitto.org"

def getdata():
    global data
    h, t = DHT.read_retry(sensor, DHT11)
    f = t*1.8+32
    data = struct.pack('ff', h, f)


def publishdata():
    client = mqtt.Client("P1") #create new instance
    client.connect(broker_address) #connect to broker
    client.subscribe("joe/tests")
    client.publish("joe/tests",data)
    time.sleep(2)
    
def destroy():
   time.sleep(0.01)
    
if __name__ == '__main__':    
    try:
        while True:
            getdata()
            publishdata()            
    except KeyboardInterrupt:
        destroy()
            