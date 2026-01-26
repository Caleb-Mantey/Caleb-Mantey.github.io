// Scroll Animation Handler
(function() {
  'use strict';

  // Configuration
  const config = {
    threshold: 0.15, // Percentage of element visible before triggering
    rootMargin: '0px 0px -50px 0px' // Trigger slightly before element is fully visible
  };

  // Create Intersection Observer
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        // Optionally unobserve after animation to improve performance
        // observer.unobserve(entry.target);
      }
    });
  }, config);

  // Function to observe elements
  function observeElements() {
    // Select all sections and elements with animation classes
    const animatedElements = document.querySelectorAll(
      '.fade-in-section, .fade-scale-section, .slide-in-left, .slide-in-right'
    );

    animatedElements.forEach(element => {
      observer.observe(element);
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', observeElements);
  } else {
    observeElements();
  }

  // Re-observe on dynamic content changes (if needed)
  window.addEventListener('load', () => {
    observeElements();
  });
})();
