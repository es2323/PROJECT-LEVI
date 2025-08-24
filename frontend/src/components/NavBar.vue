<template>
  <nav class="navbar">
    <div class="nav-left">
      <div class="nav-logo">
        <a href="#landing">LEVI</a>
      </div>
      <div class="nav-links"> 
      <a href="#samplemap">Sample Roadmap</a>
      <a href="#upload">The Proccess</a>
      <a href="#about">Why Levi?</a>
      <a href="#faqs">FAQs</a>
      </div>
      </div>
    
    <div class="nav-cta">
      <a href="#upload" class="cta-button">Get Started for Free</a>
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
  padding: 1rem 2.5rem;  
  /* Styling */
  background-color: rgba(251, 251, 251, 0.05);
  border-bottom: 0.5px solid var(--accent-color);
  
    /* The blur effect */
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  
  /* A subtle border to define the edge of the glass */
  border: 1px solid rgba(251, 251, 251, 0.1);
  
  /* A slightly larger radius looks better with glass */
  border-radius: 0px; 
  
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 3rem; /* Adds space between the logo and the links */
}

.nav-logo a, .nav-links a {
  color: var(--text-color);
  text-decoration: none;
  font-size: 1rem;
  font-weight: 600;
  padding: 0.8rem;
  transition: color 0.2s;
  opacity: 0.8;

}

.nav-links a:hover {
  color: var(--accent-color);
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.cta-button {
  background-color: #FBFBFB;
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