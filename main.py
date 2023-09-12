#!/usr/bin/env python

import asyncio
# from websockets.server import servefrom
import threading
import json
import math
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import time
from queue import Queue


class WebsocketServer:
    def __init__(self, in_queue, out_queue) -> None:
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
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.websocket_thread = threading.Thread(target=self.websocket_worker)
        self.state_thread = threading.Thread(target=self.state_worker)
        self.lock = threading.RLock()
        self.tick_rate = 0.001 # for example application
        self.run()
    
    def run(self):
        self.websocket_thread.start()
        self.state_thread.start()

    def join(self):
        self.state_thread.join()
        self.websocket_thread.join()        
        

    def websocket_worker(self):
#        asyncio.run(self.start_websocket())
        print("Websocket server waiting on messages")
        while True:
            msg = self.in_queue.get()
            self.out_queue.put(self.process_message(msg))
		

    def state_worker(self):
        self.state_update()

    def update_state(self):
        delta = 0.01
        self.state_x = (self.target_x - self.state_x)*delta + self.state_x
        self.state_y = (self.target_y - self.state_y)*delta + self.state_y

    #async def process_message(self, websocket):
    def process_message(self, message):
#        async for message in websocket:
        # print(message)
        msg_in = message
        # msg_in = json.loads(message)
        # print(msg_in)
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
            
            self.tick_in_newest = self.tick
        

        msg_out = {}            

        # self.update_state
        
        msg_out["tick"] = self.tick
        msg_out["state_x"] = self.state_x
        msg_out["state_y"] = self.state_y
        msg_out["target_x"] = self.target_x
        msg_out["target_y"] = self.target_y
        return msg_out
        # await websocket.send(json.dumps(msg_out))
    
    # async def start_websocket(self):
    #     print("Websocket backend waiting")
    #     with self.lock:
    #         for i in range(79,100000):
    #             try:
    #                 async with serve(self.process_message, "0.0.0.0", i):
    #                     self.port = i
    #                     print(f"Starting server messaging using port {self.port}")
    #                     await asyncio.Future()  # run forever
    #             except Exception as e:
    #                 print(e)
    #                 pass
            
    #     print("Websocket server ended")

    def state_update(self):
        try:
            print("Ticking example")
            while True:
                self.tick += 0.1
                self.update_state()
                time.sleep(self.tick_rate)
                # print(f"{self.tick:0.3f}", end="\r")
        except KeyboardInterrupt as e:
            pass

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('client_message')
def message_event(data):
    
    global inbound_queue, outbound_queue
    # while True:
    print(request.remote_addr, "received:", data)
    inbound_queue.put(data)
    msg_out = outbound_queue.get()
    print(request.remote_addr, "sending: ", msg_out)
    socketio.emit("server_message", msg_out)

@socketio.on('client_connected')
def connected_event(data):
    global ws_server
    print(f"{request.remote_addr}\t{data}")
    # socketio.emit("server_message",{'tick':ws_server.tick})


@app.route('/')
def home(name=None):
        global port
        hostname = request.headers.get('Host').split(":")[0]
        print(f"HOST: {hostname}")
        print(f"CLIENT: {request.remote_addr}")
        return render_template('index.html', name=name, hostname=hostname, port=port)

if __name__=="__main__":
    global port, inbound_queue, outbound_queue, ws_server
    port = None
    print("Starting websocket backend")
    inbound_queue = Queue()
    outbound_queue = Queue()
    ws_server = WebsocketServer(inbound_queue, outbound_queue)

    # while port is None:
    #     port = ws_server.port
    # print(f"USING: {port}")
    port=80

    print("Starting")
    # app.run(debug=True, host="0.0.0.0", port=port)
    socketio.run(app, host="0.0.0.0", port=4000)
    
    ws_server.join()
    print("Exit")
