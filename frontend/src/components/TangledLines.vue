<template>
  <div class="main-wrapper">
    <div class="sphere-wrapper">
      <div v-for="p in 12" :key="`plane-${p}`" :class="`plane plane-${p}`">
        <div v-for="s in 36" :key="`spoke-${s}`" :class="`spoke spoke-${s}`">
          <div class="dot"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// This is a pure CSS animation, so no script logic is needed.
</script>

<style scoped>
/* Main Keyframes */
@keyframes rotate3d {
  from { transform: rotate3d(1, 1, 1, 0deg); }
  to { transform: rotate3d(1, 1, 1, 360deg); }
}

@keyframes pulsate {
  0% { transform: rotateX(90deg) scale(0.3) translateZ(10px); opacity: 0.5; }
  100% { transform: rotateX(90deg) scale(1) translateZ(0px); opacity: 1; }
}

/* Layout and 3D Setup */
.main-wrapper {
  display: flex;
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: center;
  transform-style: preserve-3d;
  perspective: 600px;
}

.sphere-wrapper {
  transform-style: preserve-3d;
  width: 200px;
  height: 200px;
  position: relative;
  animation: rotate3d 25s linear infinite;
}

.plane, .spoke {
  position: absolute;
  transform-style: preserve-3d;
  top: 0; right: 0; bottom: 0; left: 0;
}

.spoke {
  transform-origin: 0 0;
  left: 50%;
  top: 50%;
  height: 110px; /* half of sphere-wrapper width */
  width: 0px;
}

.dot {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  left: -3px;
  top: 100%;
  transform: rotateX(90deg);
  background-color: var(--accent-color); /* Default color */
}

/* Generated positions for planes (12 planes) */
.plane-1 { transform: rotateY(15deg); }
.plane-2 { transform: rotateY(30deg); }
.plane-3 { transform: rotateY(45deg); }
.plane-4 { transform: rotateY(60deg); }
.plane-5 { transform: rotateY(75deg); }
.plane-6 { transform: rotateY(90deg); }
.plane-7 { transform: rotateY(105deg); }
.plane-8 { transform: rotateY(120deg); }
.plane-9 { transform: rotateY(135deg); }
.plane-10 { transform: rotateY(150deg); }
.plane-11 { transform: rotateY(165deg); }
.plane-12 { transform: rotateY(180deg); }

/* Generated positions for spokes (36 spokes) */
.spoke-1 { transform: rotateZ(10deg); } .spoke-2 { transform: rotateZ(20deg); } .spoke-3 { transform: rotateZ(30deg); } .spoke-4 { transform: rotateZ(40deg); } .spoke-5 { transform: rotateZ(50deg); } .spoke-6 { transform: rotateZ(60deg); } .spoke-7 { transform: rotateZ(70deg); } .spoke-8 { transform: rotateZ(80deg); } .spoke-9 { transform: rotateZ(90deg); } .spoke-10 { transform: rotateZ(100deg); } .spoke-11 { transform: rotateZ(110deg); } .spoke-12 { transform: rotateZ(120deg); } .spoke-13 { transform: rotateZ(130deg); } .spoke-14 { transform: rotateZ(140deg); } .spoke-15 { transform: rotateZ(150deg); } .spoke-16 { transform: rotateZ(160deg); } .spoke-17 { transform: rotateZ(170deg); } .spoke-18 { transform: rotateZ(180deg); } .spoke-19 { transform: rotateZ(190deg); } .spoke-20 { transform: rotateZ(200deg); } .spoke-21 { transform: rotateZ(210deg); } .spoke-22 { transform: rotateZ(220deg); } .spoke-23 { transform: rotateZ(230deg); } .spoke-24 { transform: rotateZ(240deg); } .spoke-25 { transform: rotateZ(250deg); } .spoke-26 { transform: rotateZ(260deg); } .spoke-27 { transform: rotateZ(270deg); } .spoke-28 { transform: rotateZ(280deg); } .spoke-29 { transform: rotateZ(290deg); } .spoke-30 { transform: rotateZ(300deg); } .spoke-31 { transform: rotateZ(310deg); } .spoke-32 { transform: rotateZ(320deg); } .spoke-33 { transform: rotateZ(330deg); } .spoke-34 { transform: rotateZ(340deg); } .spoke-35 { transform: rotateZ(350deg); } .spoke-36 { transform: rotateZ(360deg); }

/* Animate dots with your theme colors */
.spoke .dot {
  animation: pulsate 0.7s infinite alternate both;
}

/* Alternate colors using your palette */
.spoke:nth-child(even) .dot {
  background-color: var(--text-color);
}
.spoke:nth-child(odd) .dot {
  background-color: var(--accent-color);
}

/* Stagger animation delays for a nice effect */
.spoke:nth-child(1) .dot, .spoke:nth-child(36) .dot { animation-delay: 0.05s; }
.spoke:nth-child(2) .dot, .spoke:nth-child(35) .dot { animation-delay: 0.1s; }
.spoke:nth-child(3) .dot, .spoke:nth-child(34) .dot { animation-delay: 0.15s; }
.spoke:nth-child(4) .dot, .spoke:nth-child(33) .dot { animation-delay: 0.2s; }
.spoke:nth-child(5) .dot, .spoke:nth-child(32) .dot { animation-delay: 0.25s; }
.spoke:nth-child(6) .dot, .spoke:nth-child(31) .dot { animation-delay: 0.3s; }
.spoke:nth-child(7) .dot, .spoke:nth-child(30) .dot { animation-delay: 0.35s; }
.spoke:nth-child(8) .dot, .spoke:nth-child(29) .dot { animation-delay: 0.4s; }
.spoke:nth-child(9) .dot, .spoke:nth-child(28) .dot { animation-delay: 0.45s; }
.spoke:nth-child(10) .dot, .spoke:nth-child(27) .dot { animation-delay: 0.5s; }
.spoke:nth-child(11) .dot, .spoke:nth-child(26) .dot { animation-delay: 0.55s; }
.spoke:nth-child(12) .dot, .spoke:nth-child(25) .dot { animation-delay: 0.6s; }
.spoke:nth-child(13) .dot, .spoke:nth-child(24) .dot { animation-delay: 0.65s; }
.spoke:nth-child(14) .dot, .spoke:nth-child(23) .dot { animation-delay: 0.7s; }
.spoke:nth-child(15) .dot, .spoke:nth-child(22) .dot { animation-delay: 0.75s; }
.spoke:nth-child(16) .dot, .spoke:nth-child(21) .dot { animation-delay: 0.8s; }
.spoke:nth-child(17) .dot, .spoke:nth-child(20) .dot { animation-delay: 0.85s; }
.spoke:nth-child(18) .dot, .spoke:nth-child(19) .dot { animation-delay: 0.9s; }
</style>