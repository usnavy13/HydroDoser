import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt #mqtt client
import time
import struct #packing module

phup=17
phdown=27
a=22
b=5
cal=6
early=13
mid=19
guard=26

ph=6
chan_list = [phup,phdown,a,b,cal,early,mid,guard]

GPIO.setmode(GPIO.BCM)
GPIO.setup(phup, GPIO.OUT)
GPIO.output(phup,GPIO.LOW)
client = mqtt.Client("jfhgr54oe") #create new instance
broker_address="test.mosquitto.org" #broker address
topic = "home/grow/flower1"

def on_message(client, userdata, message):
    data = message.payload #message from broker
    datau = struct.unpack('fffff', data) #unpacking data from sensor
    fr,hr,wtr,phr,ecr = datau #assigning temp and humidty values from data
    global ph
    f = round(fr,2)
    h = round(hr,2)
    wt = round(wtr,2)
    ph = round(phr,1)
    ec = round(ecr,2)
    print('Air Temp = ',f,'*F Humidity = ',h,'%')
    print('PH = ',ph,' EC = ',ec,' Water Temp = ',wt)
    #client.loop_stop()    
    #time.sleep(10)

def main():    
    client.on_message=on_message #run on message function when message recieved
    client.connect(broker_address) #connect to broker
    client.subscribe(topic)#subscribe to topic   
    client.loop_start() #run forever

if __name__ == '__main__':
    main()
    while True:
        if ph >= 6.5:
            GPIO.output(phup,GPIO.HIGH)
            time.sleep(2)
            GPIO.output(phup,GPIO.LOW)
            time.sleep(20)


        
