let sample = 0;

const updateVisualizerData = (audioSample) => {
  sample = audioSample;
}

const main = () => {
  const canvas = document.getElementById("visualizer");
  const ctx = canvas.getContext("2d");
  const width = 350;
  const height = 200;
  canvas.width = width; 
  canvas.height = height; 
  
  let audioData = new Array(width).fill(0);

  const drawWave = () => {
    ctx.clearRect(0, 0, width, height);
    ctx.beginPath();
    ctx.moveTo(0, height / 2 + audioData[0] * height / 2);
    for (let i = 1; i < audioData.length; i++) {
      const x = i;
      const y = height / 2 + audioData[i] * height / 2;
      ctx.lineTo(x, y);
    }
    ctx.strokeStyle = '#d6d6d6';
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  const update = () => {
    audioData.shift();
    audioData.push(sample);
    drawWave();
    requestAnimationFrame(update); // Request the next frame
    document.getElementById("gain_value").innerHTML = document.getElementById("gain_knob").value*2 + '%';
  }

  // Start the animation loop
  update();
}

window.addEventListener('load', () => {
  main();
});
