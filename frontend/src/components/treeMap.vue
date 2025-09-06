<template>
  <div class="animation-container">
    <h2 class="title">
      <Typewriter 
        text="Hey Levi, give me a roadmap for a Junior Software Engineer"
        :speed="50"
        @typing-complete="startAnimation"
      />
    </h2>
    
    <div ref="canvasContainer" class="canvas-container"></div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue';
import p5 from 'p5';
import Typewriter from './Typewriter.vue';

const canvasContainer = ref(null);
let sketchInstance = null;
function startAnimation() {
  // Safety check to ensure it only runs once
  if (canvasContainer.value && !sketchInstance) {
    sketchInstance = new p5(createSketch, canvasContainer.value);
  }
}

const createSketch = (p) => {
  const stepHeight = 70; // Increased vertical distance
  const branchLength = 60;
  const animSpeed = 1.7;
  const roadmapSteps = [
    { skill: 'Start with Python', direction: 'right' },
    { skill: 'HTML', direction: 'left' },
    { skill: 'CSS', direction: 'right' },
    { skill: 'JavaScript', direction: 'left' },
    { skill: 'Vue.js', direction: 'right' },
    { skill: 'Docker', direction: 'left' },
  ];
  
  let stemHeight = 0;
  let currentStep = 0;
  let branches = [];

  p.setup = () => {
    p.createCanvas(500, 500).parent(canvasContainer.value);
    p.textFont('Satoshi');
  };

  p.draw = () => {
    p.clear();
    const centerX = p.width / 2;
    const totalTreeHeight = (roadmapSteps.length -1) * stepHeight;
    const startY = (p.height / 2) + (totalTreeHeight / 2) - 380;

    // Grow the main stem
    if (currentStep < roadmapSteps.length) {
      const targetHeight = currentStep * stepHeight;
      if (stemHeight < targetHeight) {
        stemHeight += animSpeed;
      } else {
        const step = roadmapSteps[currentStep];
        branches.push(new Branch(centerX, startY + stemHeight, step.direction, step.skill));
        currentStep++;
      }
    }
    
    // Draw the main stem
    p.stroke(192, 201, 238, 150); // Lighter accent color with some transparency
    p.strokeWeight(6);
    p.line(centerX, startY, centerX, startY + stemHeight);

    // Grow and draw all horizontal branches
    for (let branch of branches) {
      branch.growAndShow();
    }
  };

  class Branch {
    constructor(x, y, direction, skill) {
      this.x = x; this.y = y; this.direction = direction; this.skill = skill;
      this.currentLength = 0; this.maxLength = branchLength;
    }
    
    growAndShow() {
      if (this.currentLength < this.maxLength) {
        this.currentLength += animSpeed * 1;
      }
      
      const endX = (this.direction === 'right') ? this.x + this.currentLength : this.x - this.currentLength;
      
      // Draw branch line
      p.stroke(192, 201, 238, 150);
      p.strokeWeight(4);
      p.line(this.x, this.y, endX, this.y);
      
      // Draw node circle
      p.noStroke();
      p.fill(192, 201, 238);
      p.circle(this.x, this.y, 8);

      // --- NEW: Draw the skill box and text when the branch is fully grown ---
      if (this.currentLength >= this.maxLength) {
        p.textSize(16);
        p.textStyle(p.BOLD);
        p.noStroke();

        const textPadding = 15;
        const textW = p.textWidth(this.skill) + textPadding * 2;
        const textH = 40;
        
        let boxX, textX;
        if (this.direction === 'right') {
          boxX = endX + 10;
          p.textAlign(p.LEFT, p.CENTER);
          textX = boxX + textPadding;
        } else {
          boxX = endX - 10 - textW;
          p.textAlign(p.RIGHT, p.CENTER);
          textX = boxX + textW - textPadding;
        }

        // Draw the rounded rectangle (the box)
        p.fill(251, 251, 251, 15); // Use the semi-transparent glass background
        p.rect(boxX, this.y - textH / 2, textW, textH, 4); // 8 is the corner radius

        // Draw the text inside the box
        p.fill(251, 251, 251); // Your main text color
        p.text(this.skill, textX, this.y);
      }
    }
  }
};

onUnmounted(() => {
  // This cleans up the p5 sketch when you navigate away to prevent memory leaks
  if (sketchInstance) {
    sketchInstance.remove();
  }
});
</script>

<style scoped>
.animation-container {
  /* Sizing and Centering */
  width: 100%;
  max-width: 800px;
  height: 700px;
  margin: 2rem auto;
display: flex;
  flex-direction: column; /* Stack items vertically */
  justify-content: flex-start; /* Align items to the top */
  align-items: center;
  gap: 2rem; /* Add space between title and animation */
  padding: 2rem;
  
  /* Glass Effect */
  background: rgba(251, 251, 251, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(251, 251, 251, 0.1);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}
  
.title {
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--text-color);
  opacity: 0.9;
  min-height: 2rem; /* Give the typewriter space */
  text-align: center;
}

.canvas-container {
  width: 500px;
  height: 500px;
}

</style>