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

Ball.prototype.updatePosition = function () {
    this.x = this.x + this.velX 
    this.y = this.y + this.velY 
    if (this.x <= this.size) {
       this.velX = - this.velX;
    } else if (this.x + this.size > width) {
       this.velX = - this.velX;
    }
    if (this.y <= this.size) {
       this.velY = - this.velY;
    } else if (this.y + this.size > height) {
       this.velY = - this.velY;
    }
}

function generateBalls() {
    var i = 0;
    for (i = 0; i < 50; i ++) {
        var randomBall = new Ball(
	random(0, width),
	random(0, height), random(0, 10), random(0, 20), 
	'rgba(' + random(0, 255) + ', ' + random(0, 255) + ', ' + random(0, 255) + ', 0.2 )',
	random(5, 50));
        balls.push(randomBall);
    }
}

function loop(timestamp) {
    currTimeSec = Date.now();
   h1text.innerHTML =  "Bouncing Balls: " + currTimeSec.toString(); 
   var i = 0;
   ctx.clearRect(0, 0, width, height);
   for (i = 0; i < balls.length; i ++) {
       balls[i].updatePosition();
       balls[i].draw(ctx);
   }
   window.requestAnimationFrame(loop);
}

generateBalls();
window.requestAnimationFrame(loop);
