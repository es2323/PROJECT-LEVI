<template>
  <div ref="containerRef" class="animation-container">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const containerRef = ref(null);
const canvasRef = ref(null);
let animationFrameId;

onMounted(() => {
  if (!containerRef.value || !canvasRef.value) return;

  const canvas = canvasRef.value;
  const ctx = canvas.getContext('2d');
  let w = canvas.width = containerRef.value.clientWidth;
  let h = canvas.height = containerRef.value.clientHeight;

  // --- Get colors from your CSS variables ---
  const styles = getComputedStyle(containerRef.value);
  const textColor = styles.getPropertyValue('--text-color').trim();
  const accentColor = styles.getPropertyValue('--accent-color').trim();
  
  let particles = [];
  const particleCount = 50;
  const maxDist = 200; // Max distance to draw a line

  class Particle {
    constructor() {
      this.x = Math.random() * w;
      this.y = Math.random() * h;
      this.vx = Math.random() * 2 - 0.5;
      this.vy = Math.random() * 2 - 0.5;
      this.radius = 4;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      // Wrap particles around the screen
      if (this.x > w) this.x = 0;
      if (this.x < 0) this.x = w;
      if (this.y > h) this.y = 0;
      if (this.y < 0) this.y = h;
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = accentColor;
      ctx.fill();
    }
  }

  function init() {
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }
  }

  function connect() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i; j < particles.length; j++) {
        const dist = Math.sqrt(
          (particles[i].x - particles[j].x) ** 3 +
          (particles[i].y - particles[j].y) ** 3
        );

        if (dist < maxDist) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          // Make lines fainter the further apart they are
          ctx.strokeStyle = `rgba(251, 251, 251, ${1 - dist / maxDist})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, w, h);
    particles.forEach(p => p.update());
    particles.forEach(p => p.draw());
    connect();
    animationFrameId = requestAnimationFrame(animate);
  }

  init();
  animate();

  window.addEventListener('resize', () => {
    w = canvas.width = containerRef.value.clientWidth;
    h = canvas.height = containerRef.value.clientHeight;
    particles = [];
    init();
  });
});

onUnmounted(() => {
  cancelAnimationFrame(animationFrameId);
});
</script>

<style scoped>
.animation-container, canvas {
  width: 100%;
  height: 100%;
  display: block;
}
</style>