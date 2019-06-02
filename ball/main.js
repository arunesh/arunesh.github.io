// setup canvas

var canvas = document.querySelector('canvas');
var ctx = canvas.getContext('2d');

var h1text = document.querySelector('h1');

var width = canvas.width = window.innerWidth;
var height = canvas.height = window.innerHeight;
var currTimeSec = Date.now();
var balls = [];

// function to generate random number

function random(min,max) {
  var num = Math.floor(Math.random()*(max-min)) + min;
  return num;
}

function Ball(x, y, velX, velY, color, size) {
    this.x = x;
    this.y = y;
    this.velX = velX;
    this.velY = velY;
    this.color = color;
    this.size = size;
}

Ball.prototype.draw = function (ctx) {
    ctx.beginPath();
    ctx.fillStyle = this.color;
    ctx.arc(this.x, this.y, this.size, 0, 2 * Math.PI);
    ctx.fill();
}

function loop(timestamp) {
    currTimeSec = Date.now();
   h1text.innerHTML =  "Bouncing Balls: " + currTimeSec.toString(); 
   var randomBall = new Ball(
            random(0, width),
            random(0, height), 0, 0, 
            'rgba(' + random(0, 255) + ', ' + random(0, 255) + ', ' + random(0, 255) + ', 0.2 )',
            random(5, 200));
   randomBall.draw(ctx);
   window.requestAnimationFrame(loop);
}

window.requestAnimationFrame(loop);
