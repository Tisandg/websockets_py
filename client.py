import websockets
import asyncio

#Server: https://sync-chasing-ball.glitch.me/
print("Starting client...")

# The main function that will handle the connection and comunication
# with the server
async def listen():
  # url = "ws://simple-websocket-server-echo.glitch.me/"
  url = "ws://127.0.0.1:7890/"

  # Connect to the server
  async with websockets.connect(url) as ws:

    # Send a greeting message
    await ws.send("Hello server!")

    #Stay alive forever, listening to incoming message
    while True:
      #What to do
      msg = await ws.recv()
      print(msg)

#Start the connection
asyncio.get_event_loop().run_until_complete(listen())