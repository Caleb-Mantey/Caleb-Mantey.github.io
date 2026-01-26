// Fetch and display Medium blog posts
(function() {
  'use strict';

  const MEDIUM_USERNAME = '@manteycaleb';
  const MEDIUM_RSS_URL = `https://medium.com/feed/${MEDIUM_USERNAME}`;
  const RSS_TO_JSON_API = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(MEDIUM_RSS_URL)}`;
  const MAX_POSTS = 3;

  // Format date to readable format
  function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  }

  // Extract reading time from content
  function getReadingTime(content) {
    const text = content.replace(/<[^>]*>/g, '');
    const wordCount = text.split(/\s+/).length;
    const readingTime = Math.ceil(wordCount / 200);
    return `${readingTime} min read`;
  }

  // Get excerpt from content
  function getExcerpt(content, maxLength = 150) {
    const text = content.replace(/<[^>]*>/g, '');
    return text.length > maxLength 
      ? text.substring(0, maxLength) + '...' 
      : text;
  }

  // Get thumbnail from content or use placeholder
  function getThumbnail(item) {
    // Try to get thumbnail from item
    if (item.thumbnail) {
      return item.thumbnail;
    }
    
    // Try to extract first image from content
    const imgMatch = item.content.match(/<img[^>]+src="([^">]+)"/);
    if (imgMatch && imgMatch[1]) {
      return imgMatch[1];
    }
    
    // Use a default placeholder - gray gradient
    return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="800" height="400"%3E%3Crect width="800" height="400" fill="%23f0f0f0"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" fill="%23999"%3EBlog Post%3C/text%3E%3C/svg%3E';
  }

  // Create blog post HTML
  function createBlogPostHTML(item) {
    const thumbnail = getThumbnail(item);
    const excerpt = getExcerpt(item.description || item.content);
    const date = formatDate(item.pubDate);
    const readingTime = getReadingTime(item.content);
    const categories = item.categories && item.categories.length > 0 
      ? item.categories.slice(0, 2).join(', ') 
      : 'Blog';

    return `
      <div class="col-lg-4 col-md-6">
        <div class="blog-post rounded customer-testi m-1">
          <div class="position-relative">
            <img
              src="${thumbnail}"
              class="img-fluid rounded-top"
              alt="${item.title}"
              style="height: 200px; width: 100%; object-fit: cover;"
              onerror="this.src='images/blog/placeholder.png'"
            />
          </div>
          <div class="content pt-4 pb-4 p-3">
            <h5>
              <a
                href="${item.link}"
                target="_blank"
                rel="noopener noreferrer"
                class="title text-dark"
              >
                ${item.title}
              </a>
            </h5>
            <p class="text-light-muted mb-3">
              ${excerpt}
            </p>
            <div class="post-meta d-flex justify-content-between mt-3">
              <ul class="list-unstyled mb-0">
                <li class="list-inline-item me-2 mb-0">
                  <a href="${item.link}" target="_blank" class="text-muted like">
                    <i class="mdi mdi-folder-outline me-1"></i>${categories}
                  </a>
                </li>
                <li class="list-inline-item">
                  <a href="${item.link}" target="_blank" class="text-muted comments">
                    <i class="mdi mdi-clock-outline me-1"></i>${readingTime}
                  </a>
                </li>
              </ul>
              <a
                href="${item.link}"
                target="_blank"
                rel="noopener noreferrer"
                class="text-muted readmore"
              >
                Read More <i class="mdi mdi-chevron-right"></i>
              </a>
            </div>
            <div class="post-meta mt-2">
              <span class="text-muted">
                <i class="mdi mdi-calendar-outline me-1"></i>${date}
              </span>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  // Fetch and display Medium posts
  function fetchMediumPosts() {
    const container = document.getElementById('medium-posts-container');
    
    if (!container) {
      console.error('Medium posts container not found');
      return;
    }

    // Show loading state
    container.innerHTML = `
      <div class="col-12 text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3 text-muted">Loading recent blog posts...</p>
      </div>
    `;

    fetch(RSS_TO_JSON_API)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data.status !== 'ok' || !data.items || data.items.length === 0) {
          throw new Error('No posts found');
        }

        // Get the latest posts
        const posts = data.items.slice(0, MAX_POSTS);
        
        // Clear loading state and add posts
        container.innerHTML = posts.map(post => createBlogPostHTML(post)).join('');
      })
      .catch(error => {
        console.error('Error fetching Medium posts:', error);
        container.innerHTML = `
          <div class="col-12 text-center">
            <div class="alert alert-warning" role="alert">
              <i class="mdi mdi-alert-outline me-2"></i>
              Unable to load blog posts at the moment. Please visit my 
              <a href="https://medium.com/${MEDIUM_USERNAME}" target="_blank" class="alert-link">Medium profile</a> 
              to read my latest articles.
            </div>
          </div>
        `;
      });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fetchMediumPosts);
  } else {
    fetchMediumPosts();
  }
})();
