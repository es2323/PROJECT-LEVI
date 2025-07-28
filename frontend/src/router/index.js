// frontend/src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import CVUploader from '../components/CVUploader.vue';
import Questionnaire from '../components/Questionnaire.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: CVUploader // The CVUploader is the default home page
  },
  {
    path: '/questionnaire',
    name: 'Questionnaire',
    component: Questionnaire // The questionnaire is on its own page
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;