// Dark mode toggle script
import '../styles/light/base.css';
import '../styles/light/components.css';
import '../styles/light/filters.css';
import '../styles/light/modal.css';
import '../styles/dark/base.css';
import '../styles/dark/components.css';
import '../styles/dark/filters.css';
import '../styles/dark/modal.css';

// Function to load CSS file
function loadCSS(filename) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = filename;
    document.head.appendChild(link);
  }
  
  // Function to remove CSS file
  function removeCSS(filename) {
    const links = document.getElementsByTagName('link');
    for (let i = links.length - 1; i >= 0; i--) {
      if (links[i].href.includes(filename)) {
        links[i].parentNode.removeChild(links[i]);
      }
    }
  }
  
  // Function to toggle dark mode
  function toggleDarkMode() {
    const isDarkMode = !window.isDarkMode;
    window.isDarkMode = isDarkMode;
    
    // Save the dark mode state to localStorage
    localStorage.setItem('isDarkMode', isDarkMode);
    
    // Toggle CSS files
    if (isDarkMode) {
      removeCSS('styles/light/');
      loadCSS('styles/dark/base.css');
      loadCSS('styles/dark/components.css');
      loadCSS('styles/dark/filters.css');
      loadCSS('styles/dark/modal.css');
    } else {
      removeCSS('styles/dark/');
      loadCSS('styles/light/base.css');
      loadCSS('styles/light/components.css');
      loadCSS('styles/light/filters.css');
      loadCSS('styles/light/modal.css');
    }
    
    // Update button text
    const darkModeToggle = document.getElementById('darkModeToggle');
    darkModeToggle.textContent = isDarkMode ? '☀' : '☽';
    
    // Reload the page to refresh images
    location.reload();
  }
  
  // Function to initialize dark mode state
  function initDarkMode() {
    const savedDarkMode = localStorage.getItem('isDarkMode');
    window.isDarkMode = savedDarkMode === 'true';
    
    // Apply initial state
    if (window.isDarkMode) {
      removeCSS('styles/light/');
      loadCSS('styles/dark/base.css');
      loadCSS('styles/dark/components.css');
      loadCSS('styles/dark/filters.css');
      loadCSS('styles/dark/modal.css');
      document.getElementById('darkModeToggle').textContent = '☀';
    } else {
      removeCSS('styles/dark/');
      loadCSS('styles/light/base.css');
      loadCSS('styles/light/components.css');
      loadCSS('styles/light/filters.css');
      loadCSS('styles/light/modal.css');
      document.getElementById('darkModeToggle').textContent = '☽';
    }
  }
  
  // Add event listener to the dark mode toggle button
  document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('darkModeToggle');
    darkModeToggle.addEventListener('click', toggleDarkMode);
    
    // Initialize dark mode state
    initDarkMode();
  });