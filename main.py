#!/usr/bin/env python

import asyncio
from websockets.server import serve
import threading
import json
import math
from flask import Flask, render_template, request
import time

class WebsocketServer:
    def __init__(self) -> None:
        self.tick = 0.
        self.state_x = 0.
        self.state_y = 0.
        self.target_x = 0.
        self.target_y = 0.

        self.tick_in = 0.
        self.tick_in_newest = 0.
        self.state_x_in = 0.
        self.state_y_in = 0.
        self.target_x_in = 0.
        self.target_y_in = 0.

        self.state = None
        self.ws = None
        self.port = None
        self.websocket_thread = threading.Thread(target=self.websocket_thread)
        self.state_thread = threading.Thread(target=self.state_thread)
        self.lock = threading.RLock()
        self.tick_rate = 0.0001 # for example application
        self.run()
    
    def run(self):
        self.websocket_thread.start()
        self.state_thread.start()

    def join(self):
        self.state_thread.join()
        self.websocket_thread.join()        
        

    def websocket_thread(self):
        asyncio.run(self.start_websocket())

    def state_thread(self):
        self.state_update()

    def update_state(self, curr_tick):
        delta = 0.01
        self.state_x = (self.target_x - self.state_x)*delta + self.state_x
        self.state_y = (self.target_y - self.state_y)*delta + self.state_y

    async def process_message(self, websocket):
        async for message in websocket:
            msg_in = json.loads(message)
            try:
                self.tick_in = msg_in["tick"]
                self.state_x_in = msg_in["state_x"]
                self.state_y_in = msg_in["state_y"]
                self.target_x_in = msg_in["target_x"]
                self.target_y_in = msg_in["target_y"]
            except:
                pass
            curr_tick = self.tick
            if curr_tick > self.tick_in_newest:
                self.target_x = self.target_x_in
                self.target_y = self.target_y_in
                self.update_state(curr_tick)
                self.tick_in_newest = self.tick
            

            msg_out = {}            

            self.update_state
            
            msg_out["tick"] = self.tick
            msg_out["state_x"] = self.state_x
            msg_out["state_y"] = self.state_y
            msg_out["target_x"] = self.target_x
            msg_out["target_y"] = self.target_y
            await websocket.send(json.dumps(msg_out))
    
    async def start_websocket(self):
        print("Websocket backend waiting")
        with self.lock:
            for i in range(8001,30000):
                try:
                    async with serve(self.process_message, "0.0.0.0", i):
                        self.port = i
                        print(f"Starting server messaging using port {self.port}")
                        await asyncio.Future()  # run forever
                except Exception as e:
                    print(e)
                    pass
            
        print("Websocket server ended")

    def state_update(self):
        try:
            print("Ticking example")
            while True:
                self.tick += 0.1
                time.sleep(self.tick_rate)
                # print(f"{self.tick:0.3f}", end="\r")
        except KeyboardInterrupt as e:
            pass

app = Flask(__name__)

@app.route('/')
def home(name=None):
        global port
        hostname = request.headers.get('Host').split(":")[0]
        print(f"HOST: {hostname}")
        return render_template('index.html', name=name, hostname=hostname, port=port)

if __name__=="__main__":
    global port
    port = None
    print("Starting websocket backend")
    ws_server = WebsocketServer()

    while port is None:
        port = ws_server.port
    print(f"USING: {port}")

    
    app.run(debug=True, host="0.0.0.0", port=8000)
    
   

    ws_server.join()
    print("Exit")