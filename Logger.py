import paho.mqtt.client as mqtt #mqtt client
import time
import struct #packing module
from datetime import datetime
import csv


broker_address="test.mosquitto.org" #broker address
topic = "home/grow/flower1"
clientid = '8jofjn9!!'

def on_message(client, userdata, message):
    data = message.payload #message from broker
    datau = struct.unpack('fffff', data) #unpacking data from sensor
    fr,hr,wtr,phr,ecr = datau #assigning temp and humidty values from data
    f = round(fr,2)
    h = round(hr,2)
    wt = round(wtr,2)
    ph = round(phr,4)
    ec = round(ecr,2)
    row = datetime.now().strftime('%d/%m/%Y %H:%M:%S'),f,h,wt,ph,ec
    with open('Sensorlog.csv', 'a') as f: #writes a new row in the sensor log
        w = csv.writer(f)
        w.writerow(row)
    #print('Air Temp = ',f,'*F Humidity = ',h,'%')
    #print('PH = ',ph,' EC = ',ec,' Water Temp = ',wt)
    
    

    
      
client = mqtt.Client(clientid) #create new instance        
client.on_message=on_message #run on message function when message recieved
client.connect(broker_address) #connect to broker
client.subscribe(topic)#subscribe to topic
client.loop_forever() #run forever