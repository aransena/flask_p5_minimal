let r, g, b;
let w, h;
let x, y, radius;
let counter;
let message;
let port;
let hostname;
let tick;
let ws_url;
let target_x;
let target_y;
let state_x;
let state_y;


function messageReceived(msg) {
  // Callback function that receives data from remote websocket server
  message = msg;
  let new_tick = message['tick'];
  if(new_tick > tick){
    tick = new_tick;
    state_x = message['state_x']*w;
    state_y = message['state_y']*h;
    target_x = message['target_x']*w;
    target_y = message['target_y']*h;
  }
}

function setup() {
  
  message = null;
  tick = 0.0;
  port = document.getElementsByName('userscript')[0].getAttribute('port_value');
  
  hostname = document.getElementsByName('userscript')[0].getAttribute('host_name');
  ws_url = "ws://"+hostname+":"+port;
  console.log(port);
  connectWebsocket(ws_url);
  sendMessage({
    "msg": "Setup success"
  });
  counter = 0;
  frameRate(120);
  h = windowHeight;
  w = windowWidth;
  state_x = w/2;
  state_y = h/2;
  target_x = w/2;
  target_y = h/2;
  
  createCanvas(w, h);
  r = random(255);
  g = random(255);
  b = random(255);

  console.log("Setup")
}

function draw() {
  background(127);

  stroke(r, g, b);
  fill(r, g, b, 127);
  let lambda = 0.01;
  
  counter += 0.1; // Demo local value to send to remote websocket server
  
  // Send data back to remote websocket server
  try {
    
    sendMessage({
      "data": counter,
      "msg": "Counter value",
      "tick": tick,
    });
  } catch (error) {
    connectWebsocket(ws_url);
  }
  
  // Simple example for this code
  try {
    // console.log(state_x);
    ellipse(
      state_x, 
      state_y,
      30+sin(tick/100.)*10,
      30+sin(tick/100.)*10
    );
    
  } catch (error) {
    
  }

  // Check for window resize  
  let w_new = windowWidth
  let h_new = windowHeight
  if(w_new != w || h_new != h){
    w = w_new;
    h = h_new;
    resizeCanvas(w, h);
  }
    
}



function mousePressed() {
  target_x = mouseX;
  target_y = mouseY;
  // Send data back to remote websocket server
  try {
    sendMessage({
      "data": counter,
      "msg": "Counter value",
      "tick": tick,
      "state_x": state_x/w,
      "state_y": state_y/h,
      "target_x": target_x/w,
      "target_y": target_y/h
    });
  } catch (error) {
    connectWebsocket(ws_url);
  }

}