let r, g, b;
let w, h;
let x, y, radius;

function setup() {

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
  background(127);
  strokeWeight(2);
  stroke(r, g, b);
  fill(r, g, b, 127);
  radius = 200+100*sin(frameCount/30)
  x = w/2;
  y = h/2;
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