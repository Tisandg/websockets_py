from logging import exception
import websockets
import asyncio
import pandas as pd
import time
import json

#Server: https://sync-chasing-ball.glitch.me/
print("Starting client...")

data_line = ""
current_index = 0

# Read csv
df = pd.read_csv('data/owzone.csv')

# Convert to json
txt_json = df.to_json(orient='records')
json_data = json.loads(txt_json)
print("Archivo leido")

def update_data():
  global data_line, json_data, current_index
  data_line = json_data[current_index]

  print(current_index)

  if(current_index < len(json_data)-1):
      current_index = current_index + 1
  else:
      current_index = 0

  return data_line

# The main function that will handle the connection and comunication
# with the server
async def listen():
  # url = "ws://simple-websocket-server-echo.glitch.me/"
  url = "ws://127.0.0.1:7890/"

  # Connect to the server
  async with websockets.connect(url, ping_interval=None) as ws:

    # Send a greeting message
    await ws.send("Hello server! I'm the client generator of data")
    
    #Stay alive forever, sending the information from csv
    while True:
      line = update_data()
      print("Line to send: "+ str(line))
      await ws.send(str(line))
      time.sleep(3)

#Start the connection
asyncio.get_event_loop().run_until_complete(listen())