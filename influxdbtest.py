import paho.mqtt.client as mqtt #mqtt client
import time
import struct #packing module
from influxdb import InfluxDBClient
import datetime

host = "127.0.0.1" # My Ubuntu NUC
port = 8086 # default port
user = "admin" # the user/password created for the pi, with write access
password = "admin" 
dbname = "sensor_data" # the database we created earlier
measurement = "System1"
location = "flower"

clientinf = InfluxDBClient(host, port, user, password, dbname)
broker_address="test.mosquitto.org" #broker address
topic = "home/grow/flower1"

def on_message(client, userdata, message):
    datap = message.payload #message from broker
    datau = struct.unpack('fffff', datap) #unpacking data from sensor
    fr,hr,wtr,phr,ecr = datau #assigning temp and humidty values from data
    f = round(fr,2)
    h = round(hr,2)
    wt = round(wtr,2)
    ph = round(phr,4)
    ec = round(ecr,2)
    iso = time.ctime()
    print('Air Temp = ',f,'*F Humidity = ',h,'%')
    print('PH = ',ph,' EC = ',ec,' Water Temp = ',wt)
    data = [
        {
          "measurement": measurement,
              "tags": {
                  "location": location,
              },
              "time": iso,
              "fields": {
                  "temperature" : f,
                  "humidity": h,
                  "water temperature": wt,
                  "PH": ph,
                  "EC": ec
              }
          }
        ]
        # Send the JSON data to InfluxDB
    clientinf.write_points(data)
    

    
      
client = mqtt.Client("jodeffe") #create new instance        
client.on_message=on_message #run on message function when message recieved
client.connect(broker_address) #connect to broker
client.subscribe(topic)#subscribe to topic
client.loop_forever() #run forever
      
client = mqtt.Client(clientid) #create new instance        
client.on_message=on_message #run on message function when message recieved
client.connect(broker_address) #connect to broker
client.subscribe(topic)#subscribe to topic
client.loop_forever() #run forever