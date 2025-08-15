<template>
  <nav class="navbar">
    <div class="nav-left">
    <div class="nav-logo">
      <a href="#landing">LEVI</a>
    </div>
    <div class="nav-links">
      <a href="#upload">How It Works</a>
      <a href="#about">About</a>
      <a href="#contact">Contact</a>
      </div>
    </div>
    <div class="nav-cta">
      <a href="#upload" class="cta-button">Get Started</a>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  /* Positioning */
  position: sticky;
  top: 0;
  width: 100%;
  z-index: 100;

  /* Layout */
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  
  /* Styling */
  background-color: var(--background-color);
  border-bottom: 3px solid rgba(224, 224, 224, 0.1); /* Subtle border */
}
.nav-left {
  display: flex;
  align-items: center;
  gap: 2rem; /* Adds space between the logo and the links */
}

.nav-logo a, .nav-links a {
  color: var(--text-color);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 700;
  padding: 0.5rem;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: var(--accent-color);
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.cta-button {
  background-color: #ffffff;
  color: #000;
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 700;
  text-decoration: none;
  transition: opacity 0.2s;
}

.cta-button:hover {
  opacity: 0.8;
}
</style>