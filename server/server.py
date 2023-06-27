#!/usr/bin/env python

import asyncio
import websockets
import socket
from base64 import b64decode
import wave
import json
from datetime import datetime
import requests
import json
import os

class Pothole:
    longitude = 0
    latitude = 0
    accel = 0
    strength = ""
    datetime = datetime.timestamp(datetime.now())

    
    def __repr__(self):
        return '<Pothole %r>' % self.id

new_pothole = Pothole()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

hostname = socket.gethostname()
IPAddr = get_ip()
print("Your Computer Name is: " + hostname)
print("Your Computer IP Address is: " + IPAddr)
print(
    "* Enter {0}:5000 in the app.\n* Press the 'Set IP Address' button.\n* Select the sensors to stream.\n* Update the 'update interval' by entering a value in ms.".format(IPAddr))

async def echo(websocket, path):
      

    async for message in websocket: 
        if path == '/accelerometer':
            data = await websocket.recv()
            print(data)
            f = open("accelerometer.txt", "a")
            f.write(data+"\n")
            f.close()
        if path == '/gyroscope':
           
            data = await websocket.recv()
            print(data)
            f = open("gyroscope.txt", "a")
            f.write(data+"\n")
            
            request_url = 'https://api.ipgeolocation.io/ipgeo?ip=147.91.128.87'
            response = requests.get(request_url, params = {'apiKey':'d31ad2767ed3409c8ed922c4a17b1c76'})
            result = response.content.decode()
            # result = result.split("(")[1].strip(")")
            result  = json.loads(result)
            print(result['longitude'])
            print(result['latitude'])
            result = dict({'longitude' : result['longitude'],
                           'latitude' : result['latitude']})
            f = open("location.txt", "a")
            f.write(str(result)+"\n")
            f.close()
        

def getpot():
    return new_pothole

async def main():
    if os.path.exists('gyroscope.txt'):
        os.remove('gyroscope.txt')
    if os.path.exists('location.txt'):
        os.remove('location.txt')
    if os.path.exists('accelerometer.txt'):
        os.remove('accelerometer.txt')
    async with websockets.serve(echo, '0.0.0.0', 5000, max_size=1_000_000_000):
        await asyncio.Future()
        
    
asyncio.run(main())
