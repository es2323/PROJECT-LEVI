// frontend/src/data/mockRoadmapData.js
// frontend/src/data/mockRoadmapData.js

export const mockData = {
  "summary_roadmap": {
    "top_skills": [
      { 
        "skill": "Cloud Platforms (AWS/GCP)",
        "explanation": "Proficiency in a major cloud provider is a universal requirement for most modern tech roles, enabling scalable deployment and management of applications.",
        "recommended_resources": [
          { "type": "Video", "title": "AWS Fundamentals: Going Cloud-Native", "url": "#", "is_premium": false },
          { "type": "Course", "title": "Google Cloud Digital Leader Training", "url": "#", "is_premium": true }
        ]
      },
      { 
        "skill": "JavaScript Frameworks (Vue.js)",
        "explanation": "Essential for building modern, interactive web applications. Vue.js is a popular and approachable choice.",
        "recommended_resources": [
           { "type": "Documentation", "title": "Vue.js - The Official Guide", "url": "https://vuejs.org/guide/introduction.html", "is_premium": false }
        ]
      }
    ]
  },
  "individual_roadmaps": [
    {
      "job_title": "AI / Machine Learning Engineer",
      "skill_gaps_roadmap": [
        {
          "skill": "Cloud Platforms (AWS/GCP)",
          "explanation": "Modern AI/ML models are trained and deployed on the cloud. Proficiency in a major cloud provider is essential for managing data, training jobs, and deploying endpoints.",
          "recommended_resources": [
            { "type": "Video", "title": "AWS Certified Machine Learning Specialty 2024 - Full Course", "url": "https://www.youtube.com/watch?v=jw_H_k_6B2Q", "is_premium": false },
            { "type": "Course", "title": "Machine Learning on Google Cloud Specialization", "url": "https://www.coursera.org/specializations/machine-learning-google-cloud", "is_premium": true }
          ]
        },
        {
          "skill": "Advanced Python Libraries",
          "explanation": "Beyond basic scripts, ML Engineers use specialized libraries for data manipulation, deep learning, and model serving.",
          "recommended_resources": [
            { "type": "Article", "title": "Official PyTorch Tutorials", "url": "https://pytorch.org/tutorials/", "is_premium": false }
          ]
        }
      ]
    },
    {
      "job_title": "Frontend Developer",
      "skill_gaps_roadmap": [
        {
          "skill": "JavaScript Frameworks (Vue.js)",
          "explanation": "Mastering a modern JS framework is the most critical skill for a frontend developer. It allows you to build complex, reactive user interfaces.",
          "recommended_resources": [
            { "type": "Documentation", "title": "Vue.js - The Official Guide", "url": "https://vuejs.org/guide/introduction.html", "is_premium": false },
            { "type": "Project Idea", "title": "Build a To-Do App with a backend to practice API calls.", "url": "#", "is_premium": false }
          ]
        }
      ]
    }
  ]
};