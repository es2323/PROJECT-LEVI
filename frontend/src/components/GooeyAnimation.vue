<template>
  <svg xmlns="http://www.w3.org/2000/svg" version="1.1" class="svg-filter">
    <defs>
      <filter id="goo">
        <feGaussianBlur in="SourceGraphic" stdDeviation="6.8" result="blur" />
        <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 19 -9" result="goo" />
        <feComposite in="SourceGraphic" in2="goo" operator="atop"/>
      </filter>
    </defs>
  </svg>

  <div class="burger-ctr" :class="{ 'active': isActive }">
    <div class="head"></div>
    <div class="bar top"></div>
    <div class="bar center"></div>
    <div class="bar bottom"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isActive = ref(false);
let animationInterval = null;

// onMounted starts the animation loop when the component is on the page
onMounted(() => {
  // This interval will toggle the 'active' class every 2 seconds, creating an infinite loop
  animationInterval = setInterval(() => {
    isActive.value = !isActive.value;
  }, 1500);
});

// onUnmounted cleans up the loop when the component is removed to prevent memory leaks
onUnmounted(() => {
  clearInterval(animationInterval);
});
</script>

<style scoped>
/* This hides the SVG filter so it doesn't take up space */
.svg-filter {
  position: absolute;
  width: 0;
  height: 0;
}

.burger-ctr {
  width: 100px;
  height: 100px;
  position: relative;
  box-sizing: border-box;
transform: scale(1.3);
}

.bar, .head {
  /* CHANGED: Uses your theme's accent color */
  background: var(--accent-color);
  position: relative;
}

.bar {
  height: 15px;
  margin-bottom: 15px;
  border-radius: 10px;
  transition: .3s all ease;
}

.bar.bottom {
  margin-bottom: 0;
}

.head {
  position: relative;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  top: 50%;
  margin-top: -10px;
  left: 50%;
  margin-left: -10px;
  transform: scale(0);
}

/* --- Active State Animation --- */
.burger-ctr.active {
  filter: url("#goo");
}

.burger-ctr.active .head {
  top: 0;
  margin-top: 0;
  transform: scale(1);
  transition: .4s all ease .3s;
}

.burger-ctr.active .bar.center {
  transform: scale(0);
}

.burger-ctr.active .bar.top {
  transform: translateY(30px) rotate(45deg);
}

.burger-ctr.active .bar.bottom {
  transform: translateY(-30px) rotate(-45deg);
}
</style>