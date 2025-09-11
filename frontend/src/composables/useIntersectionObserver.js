// frontend/src/composables/useIntersectionObserver.js
import { ref, onMounted, onUnmounted } from 'vue';

export function useIntersectionObserver(elementRef) {
  const isVisible = ref(false);
  
  const observer = new IntersectionObserver(([entry]) => {
    // This will trigger only once when the element becomes visible
    if (entry.isIntersecting) {
      isVisible.value = true;
      // Once it's visible, we don't need to watch it anymore
      if (elementRef.value) {
        observer.unobserve(elementRef.value);
      }
    }
  });

  onMounted(() => {
    // Start observing the element when the component mounts
    if (elementRef.value) {
      observer.observe(elementRef.value);
    }
  });

  onUnmounted(() => {
    // Clean up the observer when the component is unmounted
    observer.disconnect();
  });

  return { isVisible };
}