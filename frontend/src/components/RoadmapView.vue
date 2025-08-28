<template>
  <div class="roadmap-container">
    <div class="tabs">
      <button class="tab-button active">Summary</button>
      <button class="tab-button">Quantitative Developer</button>
      <button class="tab-button">Cybersecurity Analyst</button>
    </div>
    <div class="roadmap-header">
      <h1 class="roadmap-title">The Big Picture</h1>
      <p class="roadmap-subtitle">A summary roadmap based on the most in-demand skills for your selected roles</p>
    </div>

    <div class="progress-tracker">
      <div class="progress-bar">
        <span class="progress-value">0% DONE</span>
        <span class="progress-count">0 of 37 Done</span>
      </div>
      <a href="#" class="track-link">Track my progress</a>
    </div>

    <div class="tab-content">
      <div class="content-panel">
        
        <div class="analysis-section">
          <h3>Relevant skills in your armory:</h3>
          <div class="skills-pills">
            <span class="pill">Python</span>
            <span class="pill">Git</span>
            <span class="pill">SQL</span>
          </div>
        </div>

        <div class="analysis-section">
          <h3>The Big Picture Roadmap</h3>
          <p class="section-subtitle">Based on all your selected roles, these are the most critical skills to learn, neatly organised for you from easiest to hardest.</p>
          <div class="timeline">
            <div class="timeline-item">
              <div class="skill-node required">Docker</div>
            </div>
            <div class="timeline-item">
              <div class="skill-node">REST APIs</div>
            </div>
            <div class="timeline-item">
              <div class="skill-node required">Cloud (AWS)</div>
            </div>
            <div class="timeline-item">
              <div class="skill-node">CI/CD Pipelines</div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.roadmap-container {
  width: 100%;
  max-width: 900px;
  margin: 2rem auto;
  padding: 2.5rem;
  border: 1px solid rgba(251, 251, 251, 0.1);
  border-radius: 8px;
  background-color: rgba(251, 251, 251, 0.05);
}

/* Tab Navigation */
.tabs {
  display: flex;
  border-bottom: 1px solid rgba(224, 224, 224, 0.2);
}
.tab-button {
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  background-color: transparent;
  border: none;
  color: var(--text-color);
  opacity: 0.6;
  font-weight: 700;
  font-size: 1rem;
  border-bottom: 3px solid transparent;
}
.tab-button.active {
  opacity: 1;
  border-bottom-color: var(--accent-color);
}

/* Roadmap Header */
.roadmap-header {
  padding: 2rem 0;
  text-align: left;
}
.roadmap-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}
.roadmap-subtitle {
  font-size: 1.1rem;
  opacity: 0.7;
  margin: 0;
}

/* Progress Tracker */
.progress-tracker {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.2);
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  margin-bottom: 3rem;
}
.progress-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.progress-value {
  background-color: var(--accent-color);
  color: var(--background-color);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 700;
}
.track-link {
  color: var(--text-color);
  text-decoration: none;
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Content Area */
.tab-content { text-align: left; }
.analysis-section { margin-bottom: 3rem; }
h3 {
  font-size: 1.5rem;
  color: var(--accent-color);
  margin-bottom: 1.5rem;
}
.section-subtitle {
  margin-top: -1rem;
  margin-bottom: 2.5rem;
  opacity: 0.7;
}

/* Skill Pills for Strengths */
.skills-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}
.pill {
  background-color: rgba(197, 176, 205, 0.1); 
  color: var(--accent-color);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 500;
}

/* Roadmap.sh inspired timeline */
.timeline {
  position: relative;
  padding: 1rem 0;
}
.timeline::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  height: 100%;
  background-color: rgba(251, 251, 251, 0.1);
}
.timeline-item {
  position: relative;
  width: 50%;
  padding: 1rem 2rem;
  margin-bottom: 1rem;
}
.timeline-item:nth-child(odd) {
  left: 0;
  text-align: right;
}
.timeline-item:nth-child(even) {
  left: 50%;
  text-align: left;
}
.timeline-item::after {
  content: '';
  position: absolute;
  top: calc(50% - 8px);
  width: 16px;
  height: 16px;
  background-color: var(--background-color);
  border: 2px solid var(--accent-color);
  border-radius: 50%;
  z-index: 1;
}
.timeline-item:nth-child(odd)::after {
  right: -8px;
}
.timeline-item:nth-child(even)::after {
  left: -8px;
}

/* The skill nodes */
.skill-node {
  display: inline-block;
  padding: 0.75rem 1.25rem;
  background-color: rgba(251, 251, 251, 0.05); 
  border: 1px solid rgba(251, 251, 251, 0.1);
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}
.skill-node:hover {
  border-color: var(--accent-color);
  transform: scale(1.05);
}
.skill-node.required {
  background-color: var(--accent-color);
  color: var(--background-color);
  font-weight: 700;
  border-color: var(--accent-color);
}
</style>