<template>
  <div class="roadmap-container" v-if="roadmapData">
    <div class="tabs">
      <button 
        @click="activeTab = 'summary'" 
        :class="{ 'active': activeTab === 'summary' }"
        class="tab-button"
      >
        Summary
      </button>
      <button 
        v-for="roadmap in roadmapData.individual_roadmaps" 
        :key="roadmap.job_title"
        @click="activeTab = roadmap.job_title"
        :class="{ 'active': activeTab === roadmap.job_title }"
        class="tab-button"
      >
        {{ roadmap.job_title }}
      </button>
    </div>

    <div class="tab-content">
      
      <div v-if="activeTab === 'summary'" class="content-panel">
        <div class="roadmap-header">
          <h1 class="roadmap-title">{{ roadmapData.summary_roadmap.title }}</h1>
          <p class="roadmap-subtitle">{{ roadmapData.summary_roadmap.description }}</p>
        </div>
        <div class="analysis-section">
          <h3>Top Demanded Skills Pathway</h3>
          <div class="timeline">
            <div v-for="item in roadmapData.summary_roadmap.top_skills" :key="item.skill" class="timeline-item">
              <div class="skill-node required" @click="selectSkill(item)">
                {{ item.skill }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-for="roadmap in roadmapData.individual_roadmaps" :key="roadmap.job_title">
        <div v-if="activeTab === roadmap.job_title" class="content-panel">
          <div class="roadmap-header">
            <h1 class="roadmap-title">{{ roadmap.job_title }} Roadmap</h1>
            <p class="roadmap-subtitle">Your personalized pathway to becoming a {{ roadmap.job_title }}.</p>
          </div>
          <div class="analysis-section">
            <h3>Skill Gaps to Address</h3>
            <div class="timeline">
              <div v-for="gap in roadmap.skill_gaps_roadmap" :key="gap.skill" class="timeline-item">
                <div class="skill-node required" @click="selectSkill(gap)">
                  {{ gap.skill }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Transition name="slide">
      <div v-if="selectedSkill" class="details-panel-overlay" @click.self="closePanel">
        <div class="details-panel">
          <button @click="closePanel" class="close-button">×</button>
          <h2>{{ selectedSkill.skill }}</h2>
          <p class="explanation">{{ selectedSkill.explanation }}</p>
          
          <div class="resources">
            <h3>Recommended Resources</h3>
            <ul>
              <li v-for="resource in selectedSkill.recommended_resources" :key="resource.title">
                <a :href="resource.url" target="_blank" rel="noopener noreferrer">
                  <span class="resource-type">{{ resource.type }}</span>
                  <span class="resource-title">{{ resource.title }}</span>
                  <span v-if="resource.is_premium" class="premium-tag">Premium</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed  } from 'vue';

const props = defineProps({
  roadmapData: Object
});

// State to manage which tab is currently active
const activeTab = ref('summary');
const selectedSkill = ref(null);

function selectSkill(skill) {
  selectedSkill.value = skill;
}

function closePanel() {
  selectedSkill.value = null;
}
</script>

<style scoped>
/* Your existing styles will work perfectly with this new dynamic structure */
.roadmap-container {
  width: 100%;
  max-width: 900px;
  margin: 2rem auto;
  padding: 2.5rem;
  border: 1px solid rgba(251, 251, 251, 0.1);
  border-radius: 16px;
  background-color: rgba(251, 251, 251, 0.05);
}
.tabs {
  display: flex;
  border-bottom: 1px solid rgba(251, 251, 251, 0.1);
  margin-bottom: 1rem;
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
.tab-content { text-align: left; }
.analysis-section { margin-bottom: 3rem; }
h3 {
  font-size: 1.5rem;
  color: var(--accent-color);
  margin-bottom: 1.5rem;
}
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
.timeline-item:nth-child(odd):after {
  right: -8px;
}
.timeline-item:nth-child(even):after {
  left: -8px;
}
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

/* Details Panel & Animation */
.details-panel-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: flex-end;
}
.details-panel {
  width: 100%;
  max-width: 450px;
  height: 100%;
  background-color: var(--background-color);
  box-shadow: -5px 0 15px rgba(0,0,0,0.2);
  padding: 2rem;
  overflow-y: auto;
  position: relative;
}
.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 2rem;
  color: var(--text-color);
  opacity: 0.5;
  cursor: pointer;
}
.close-button:hover { opacity: 1; }
.details-panel h2 { font-size: 2rem; color: var(--accent-color); margin-top: 2rem; }
.explanation { line-height: 1.6; opacity: 0.9; }
.resources h3 { font-size: 1.2rem; border-top: 1px solid rgba(251, 251, 251, 0.1); padding-top: 1.5rem; margin-top: 2rem; }
.resources ul { list-style: none; padding: 0; }
.resources li a {
  display: block;
  padding: 1rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  background-color: rgba(251, 251, 251, 0.05);
  text-decoration: none;
  color: var(--text-color);
  transition: background-color 0.2s;
}
.resources li a:hover { background-color: rgba(251, 251, 251, 0.1); }
.resource-type { display: block; font-size: 0.8rem; font-weight: 700; color: var(--accent-color); margin-bottom: 0.25rem; }
.premium-tag { float: right; background-color: var(--accent-color); color: var(--background-color); font-size: 0.7rem; padding: 0.15rem 0.4rem; border-radius: 4px; font-weight: 700; }

.slide-enter-active,
.slide-leave-active {
  transition: all 0.4s ease;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateX(100px);
}
</style>