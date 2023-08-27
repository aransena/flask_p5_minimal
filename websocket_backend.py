#!/usr/bin/env python

import asyncio
from websockets.server import serve
import threading
import json
import math

class WebsocketServer:
    def __init__(self) -> None:
        self.tick = 0
        self.state = None
        self.ws = None
        self.websocket_thread = threading.Thread(target=self.websocket_thread)
        self.state_thread = threading.Thread(target=self.state_thread)
    
    def run(self):
        self.websocket_thread.start()
        self.state_thread.start()
        self.websocket_thread.join()
        self.state_thread.join()
        

    def websocket_thread(self):
        asyncio.run(self.start_websocket())

    def state_thread(self):
        self.state_update()

    async def process_message(self, websocket):
        async for message in websocket:
            msg_in = json.loads(message)
            print(f"Received: {msg_in}")
            msg_out = {}
            msg_out["data"] = self.tick
            await websocket.send(json.dumps(msg_out))
    
    async def start_websocket(self):
        print("Websocket backend waiting")
        async with serve(self.process_message, "0.0.0.0", 8765):
            print("Starting server messaging")
            await asyncio.Future()  # run forever
        print("Websocket server ended")

    def state_update(self):
        try:
            print("Ticking example")
            while True:
                self.tick += 0.001
                print(f"{self.tick:0.3f}", end="\r")
        except KeyboardInterrupt as e:
            pass

if __name__=="__main__":
    print("Starting websocket backend")
    ws_server = WebsocketServer()
    ws_server.run()
    print("Exit")