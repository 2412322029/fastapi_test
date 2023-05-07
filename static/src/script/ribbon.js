/**
 * Copyright (c) 2016 hustcc
 * License: MIT
 * Version: v1.0.1
 * GitHub: https://github.com/hustcc/ribbon.js
**/
/*jshint -W030 */
export function ribbon(ti = 5) {
  if (!Number.isInteger(ti) || ti < 1) {
    ti = 5
  }
  function attr(node, attr, default_value) {
    return Number(node.getAttribute(attr)) || default_value;
  }

  // get user config
  var scripts = document.getElementsByTagName('script'),
    script = scripts[scripts.length - 1]; // 
  var config = {
    z: attr(script, "zIndex", -1), // z-index
    a: attr(script, "alpha", 0.8), // alpha
    s: attr(script, "size", 190), // size
  };

  var ccc = document.getElementsByClassName('rib');
  if (ccc.length > 1) {
    for (let i = 1; i < ccc.length; i++) {
      ccc[i].remove()
    }
  }
  var canvas = document.getElementById('cbg');
  // var canvas = document.createElement('canvas');
  var g2d = canvas.getContext('2d'),
    pr = window.devicePixelRatio || 1,
    width = window.innerWidth,
    height = window.innerHeight,
    f = config.s,
    q, t,
    m = Math,
    r = 0,
    pi = m.PI * 2,
    cos = m.cos,
    random = m.random;
  canvas.width = width * pr;
  canvas.height = height * pr;
  g2d.scale(pr, pr);
  g2d.globalAlpha = config.a;
  canvas.style.cssText = 'opacity: ' + config.a + ';position:fixed;top:0;left:0;z-index: ' + config.z + ';width:100%;height:100%;pointer-events:none;';
  // create canvas
  document.getElementsByTagName('body')[0].appendChild(canvas);
  var times = ti - 1
  function redraw() {
    times++
    g2d.font = "50px serif";
    g2d.fillText(`。`, 20, 80 + 20 * times);
    if (times >= ti) {
      var c1 = 0
      g2d.clearRect(0, 0, width, height);
      q = [{ x: 0, y: height * 0.7 + f }, { x: 0, y: height * 0.7 - f }];
      while (q[1].x < width + f) {
          c1 = draw(q[0], q[1]);
      }
      times = 0
    }
    if (c1) {
      document.documentElement.style.setProperty('--bg-b', '#' + (cos(r) * 127 + 128 << 16 | cos(r + pi / 3) * 127 + 128 << 8 | cos(r + pi / 3 * 2) * 127 + 128).toString(16)+'60');
    }

  }
  function draw(i, j) {
    let col = '#' + (cos(r) * 127 + 128 << 16 | cos(r + pi / 3) * 127 + 128 << 8 | cos(r + pi / 3 * 2) * 127 + 128).toString(16);
    g2d.beginPath();
    g2d.moveTo(i.x, i.y);
    g2d.lineTo(j.x, j.y);
    var k = j.x + (random() * 2 - 0.25) * f, n = line(j.y);
    g2d.lineTo(k, n);
    g2d.closePath();
    r -= pi / -50;
    g2d.fillStyle = col
    g2d.fill();
    q[0] = q[1];
    q[1] = { x: k, y: n };
    return col
  }
  function line(p) {
    t = p + (random() * 2 - 1.1) * f;
    return (t > height || t < 0) ? line(p) : t;
  }

  document.onclick = redraw;
  document.ontouchstart = redraw;
  redraw();
};