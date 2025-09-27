<template>
  <footer class="footer-container">
    <div class="footer-content">
      
      <div class="footer-links">
        <button @click="emit('open-manifesto')" class="footer-link-button">Manifesto</button>        <a href="#help">FAQs</a>
        <a href="mailto:your.email@example.com">Contact Us</a>
        <a href="#" target="_blank" rel="noopener noreferrer">GitHub</a>
      </div>

      <div class="footer-bottom">
        <div class="copyright">
          © 2025 Project Levi.
        </div>
        <div class="social-links">
          <a href="#" target="_blank" rel="noopener noreferrer" aria-label="Twitter">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"></path></svg>
          </a>
          <a href="#" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M20.5 2h-17A1.5 1.5 0 002 3.5v17A1.5 1.5 0 003.5 22h17a1.5 1.5 0 001.5-1.5v-17A1.5 1.5 0 0020.5 2zM8 19H5v-9h3zM6.5 8.25A1.75 1.75 0 118.25 6.5 1.75 1.75 0 016.5 8.25zM19 19h-3v-4.75c0-1.4-1.2-2.5-2.5-2.5S11 12.85 11 14.25V19h-3v-9h3v1.38c.6-.98 1.9-1.63 3-1.63 2.2 0 4 1.8 4 4z"></path></svg>
          </a>
          <a href="#" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 2c2.717 0 3.056.01 4.122.06 1.065.05 1.79.217 2.428.465.66.254 1.216.598 1.772 1.153a4.908 4.908 0 011.153 1.772c.247.637.415 1.363.465 2.428.047 1.066.06 1.405.06 4.122 0 2.717-.01 3.056-.06 4.122-.05 1.065-.218 1.79-.465 2.428a4.883 4.883 0 01-1.153 1.772 4.915 4.915 0 01-1.772 1.153c-.637.247-1.363.415-2.428.465-1.066.047-1.405.06-4.122.06-2.717 0-3.056-.01-4.122-.06-1.065-.05-1.79-.218-2.428-.465a4.89 4.89 0 01-1.772-1.153 4.904 4.904 0 01-1.153-1.772c-.248-.637-.415-1.363-.465-2.428C2.013 15.056 2 14.717 2 12c0-2.717.01-3.056.06-4.122.05-1.066.217-1.79.465-2.428a4.88 4.88 0 011.153-1.772A4.897 4.897 0 015.45 2.525c.638-.248 1.362-.415 2.428-.465C8.944 2.013 9.283 2 12 2zm0 5a5 5 0 100 10 5 5 0 000-10zm6.5-.25a1.25 1.25 0 00-2.5 0 1.25 1.25 0 002.5 0z"></path></svg>
          </a>
        </div>
      </div>

    </div>
  </footer>
</template>

<script setup>
const emit = defineEmits(['open-manifesto']);
</script>

<style scoped>
.footer-container {
  width: 100%;
  padding: 3rem 2rem 2rem 2rem; /* Added more top padding */
  border-top: 1px solid rgba(251, 251, 251, 0.1);
  margin-top: 4rem;
}
.footer-content {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
}
.footer-links {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
}
.footer-links a {
  color: var(--text-color);
  opacity: 0.8;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.2s;
}
.footer-links a:hover {
  opacity: 1;
  text-decoration: underline;
}
.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(251, 251, 251, 0.1);
}
.copyright {
  font-size: 0.9rem;
  opacity: 0.7;
}
.social-links {
  display: flex;
  gap: 1.5rem;
}
.social-links a {
  color: var(--text-color);
  opacity: 0.7;
  transition: opacity 0.2s, transform 0.2s;
}
.social-links a:hover {
  opacity: 1;
  transform: scale(1.1);
}
.footer-link-button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-color);
  opacity: 0.8;
  text-decoration: none;
  font-weight: 500;
  font-size: 1rem; /* Match the <a> tag font size */
  font-family: 'Satoshi', sans-serif;
  transition: opacity 0.2s;
  padding: 0;
}
.footer-link-button:hover {
  opacity: 1;
  text-decoration: underline;
}
</style>