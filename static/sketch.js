let r, g, b;
let w, h;
let x, y, radius;
let counter;
let message;
function messageReceived(msg) {
  message = msg;
  console.log("Received: " + msg.data);
}

function setup() {
  message = null;

  connectWebsocket("ws://127.0.0.1:8765");
  sendMessage({
    "msg": "Setup success"
  });
  counter = 0;
  frameRate(120);
  h = windowHeight
  w = windowWidth
  createCanvas(w, h);
  r = random(255);
  g = random(255);
  b = random(255);

  console.log("Setup")
}

function draw() {
  try {
    sendMessage({
      "data": counter,
      "msg": "Counter value"
    });
  } catch (error) {
    connectWebsocket("ws://127.0.0.1:8765");
  }
  
  counter += 0.01;
  background(127);
  if(message == null){
  strokeWeight(2);
  }
  else{
  strokeWeight(2);
  }
  stroke(r, g, b);
  fill(r, g, b, 127);
  radius = 100;//200+100*sin(frameCount/30)
  x = w/2;
  if(message != null){
    x = message["data"]%w
    y = h/2 + sin(message["data"]*0.01)*radius;
  }
  else{
    x = w/2;
    y = h/2;
  }
  
  ellipse(x, y, radius, radius);
  let w_new = windowWidth
  let h_new = windowHeight
  if(w_new != w || h_new != h){
    w = w_new;
    h = h_new;
    resizeCanvas(w, h);
  }

}

function mousePressed() {
  let d = dist(mouseX, mouseY, x, y);
  if (d < radius) {
    r = random(255);
    g = random(255);
    b = random(255);
  }
}