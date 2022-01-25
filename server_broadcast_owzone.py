import websockets
import asyncio

PORT = 7890
print("Server starting")
print("Listening on port "+str(PORT))

connected = set()

async def echo(websocket, path):
  print("A client just connected")
  connected.add(websocket)

  try:
    async for message in websocket:
      print("Message received: "+message)

      # Send message to others clients
      for conn in connected:
        if conn != websocket:
          await conn.send(message)

  except websockets.exceptions.ConnectionClosed as e:
    print("A client just disconnected")

  finally:
    connected.remove(websocket)

start_server = websockets.serve(echo, "localhost", PORT, ping_interval=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()