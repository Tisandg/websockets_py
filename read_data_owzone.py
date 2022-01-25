import pandas as pd
import time
import json
import threading
import asyncio
import websockets

data_line = ""
current_index = 0
json_data = ""


def read_file(path):

  global json_data
  # Read csv
  df = pd.read_csv(path)

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

def start_sending_data():
  while 1:
    line = update_data()
    print(line)
    time.sleep(3)


def start_delivery():
    t = threading.Thread(target=start_sending_data)
    t.start()


def get_data():
    return data_line, current_index


async def main():
  async with websockets.connect('ws://127.0.0.1:7890') as websocket:
    while 1:
      try:
        while 1:
          line = update_data()
          print(line)
          await websocket.send(str(line))
          print('data updated')
          time.sleep(3)  # wait and then do it again

      except Exception as e:
          print(e)

read_file('data/owzone.csv')
asyncio.get_event_loop().run_until_complete(main())
