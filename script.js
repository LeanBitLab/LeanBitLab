// Mapping from GitHub repository name (lowercase) to DOM ID suffix
const repoMap = {
  'adaptive-brightness-linux': 'adaptive-brightness-linux',
  'leantype': 'leantype',
  'leantype-handwriting-plugin': 'leantype-handwriting-plugin',
  'ltvlauncher': 'ltvlauncher',
  'lwidget': 'lwidget'
};

// Database mapping of repositories to their screenshot files and raw URL paths
const repoScreenshots = {
  'leantype': {
    baseUrl: 'https://raw.githubusercontent.com/LeanBitLab/LeanType/main/docs/images/',
    files: ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
  },
  'ltvlauncher': {
    baseUrl: 'https://raw.githubusercontent.com/LeanBitLab/LtvLauncher/master/docs/images/',
    files: ['screenshot_1.png', 'screenshot_2.png', 'screenshot_3.png', 'screenshot_4.png']
  },
  'lwidget': {
    baseUrl: 'https://raw.githubusercontent.com/LeanBitLab/Lwidget/main/docs/images/',
    files: ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png']
  },
  'adaptive-brightness-linux': {
    baseUrl: 'https://raw.githubusercontent.com/LeanBitLab/adaptive-brightness-linux/master/docs/screenshots/',
    files: ['1.png', '2.png']
  }
};

// Global variables to track the active gallery context for the fullscreen lightbox
let activeCardPrevBtn = null;
let activeCardNextBtn = null;
let activeCardImgEl = null;

// Format large numbers (e.g., 32848 -> 32.8k)
function formatNumber(num) {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k';
  }
  return num.toString();
}

// Animate count-up of stats using requestAnimationFrame
function animateStat(el, targetVal) {
  let startTimestamp = null;
  const duration = 1200; // 1.2 seconds animation
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const easeProgress = 1 - Math.pow(1 - progress, 3); // easeOutCubic
    const current = Math.floor(easeProgress * targetVal);
    el.textContent = formatNumber(current);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}

// Fetch live statistics from GitHub API
async function fetchGithubStats() {
  try {
    const reposResponse = await fetch('https://api.github.com/users/LeanBitLab/repos?per_page=100');
    if (!reposResponse.ok) throw new Error('Failed to fetch repositories list');
    
    const repos = await reposResponse.json();
    
    for (const repo of repos) {
      if (repo.fork) continue;
      
      const repoNameLower = repo.name.toLowerCase();
      const domId = repoMap[repoNameLower];
      
      if (domId) {
        // Update Stars with animation
        const starsEl = document.getElementById(`stars-${domId}`);
        if (starsEl) {
          animateStat(starsEl, repo.stargazers_count);
        }
        
        // Fetch Releases for Downloads
        try {
          const releasesResponse = await fetch(`https://api.github.com/repos/LeanBitLab/${repo.name}/releases`);
          if (releasesResponse.ok) {
            const releases = await releasesResponse.json();
            let downloadsCount = 0;
            
            for (const release of releases) {
              if (release.assets) {
                for (const asset of release.assets) {
                  downloadsCount += asset.download_count || 0;
                }
              }
            }
            
            const downloadsEl = document.getElementById(`downloads-${domId}`);
            if (downloadsEl) {
              animateStat(downloadsEl, downloadsCount);
            }
          }
        } catch (err) {
          console.error(`Error fetching releases for ${repo.name}:`, err);
        }
      }
    }
  } catch (error) {
    console.error('Error fetching live GitHub stats:', error);
  }
}

// Filter projects by category tab with smooth transitions
function filterProjects(category) {
  const cards = document.querySelectorAll('.project-card');
  const buttons = document.querySelectorAll('.tab-btn');
  
  buttons.forEach(btn => {
    if (btn.getAttribute('data-filter') === category) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  cards.forEach(card => {
    const cardCategory = card.getAttribute('data-category');
    const matches = (category === 'all' || cardCategory === category);
    
    if (matches) {
      card.classList.remove('filtered-out');
      card.style.display = 'block';
      // Trigger reflow to ensure display change has taken effect
      card.offsetHeight; 
      card.classList.add('filtered-in');
    } else {
      card.classList.remove('filtered-in');
      card.style.display = 'none'; // Instant layout collapse on filtered-out
    }
  });
}

// Initialize cursor spotlight effect
function initSpotlightEffect() {
  const cards = document.querySelectorAll('.project-card, .media-card');
  cards.forEach(card => {
    let tick = false;
    card.addEventListener('mousemove', (e) => {
      if (!tick) {
        window.requestAnimationFrame(() => {
          const rect = card.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          card.style.setProperty('--mouse-x', `${x}px`);
          card.style.setProperty('--mouse-y', `${y}px`);
          tick = false;
        });
        tick = true;
      }
    }, { passive: true });
  });
}

// Fixed header scrolled styles toggler (passive scroll listener)
function initHeaderScroll() {
  const header = document.querySelector('header');
  if (header) {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }
}

// IntersectionObserver fallback for scroll reveal animations
function initScrollRevealFallback() {
  if (!CSS.supports('(animation-timeline: view()) and (animation-range: entry)')) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('scroll-visible');
          }
        });
      },
      { 
        root: null,
        threshold: 0.1 
      }
    );

    const animatedElements = document.querySelectorAll(
      '.projects-grid > *, .media-card, .phil-card, .section-header'
    );
    
    animatedElements.forEach(el => {
      el.classList.add('scroll-hidden');
      observer.observe(el);
    });
  }
}

// Lazy create the inline screenshot gallery overlay container inside a card
function createScreenshotOverlay(card, repoName) {
  const overlay = document.createElement('div');
  overlay.className = 'screenshot-preview-overlay';
  overlay.innerHTML = `
    <button class="screenshot-close-btn" aria-label="Close Preview">&times;</button>
    <button class="screenshot-expand-btn" aria-label="Larger View">&#x2922;</button>
    <div class="screenshot-spinner"></div>
    <div class="screenshot-img-wrapper">
      <button class="screenshot-nav-btn screenshot-nav-prev" aria-label="Previous image">&lsaquo;</button>
      <img class="screenshot-img" alt="${repoName} screenshot" style="opacity: 0;">
      <button class="screenshot-nav-btn screenshot-nav-next" aria-label="Next image">&rsaquo;</button>
    </div>
    <div class="screenshot-indicators"></div>
  `;
  card.appendChild(overlay);
  
  initOverlayNav(overlay, repoName);
  return overlay;
}

// Set up gallery navigation logic for the screenshot overlay
function initOverlayNav(overlay, repoName) {
  const repoData = repoScreenshots[repoName];
  if (!repoData) return;
  
  let currentIndex = 0;
  const imgEl = overlay.querySelector('.screenshot-img');
  const spinnerEl = overlay.querySelector('.screenshot-spinner');
  const indicatorsContainer = overlay.querySelector('.screenshot-indicators');
  
  // Build dot indicators
  repoData.files.forEach((_, idx) => {
    const dot = document.createElement('div');
    dot.className = 'screenshot-indicator-dot' + (idx === 0 ? ' active' : '');
    indicatorsContainer.appendChild(dot);
  });
  
  const updateImage = (index) => {
    currentIndex = index;
    spinnerEl.style.display = 'block';
    imgEl.style.opacity = '0';
    
    // Update dots
    const dots = indicatorsContainer.querySelectorAll('.screenshot-indicator-dot');
    dots.forEach((dot, idx) => {
      if (idx === currentIndex) {
        dot.classList.add('active');
      } else {
        dot.classList.remove('active');
      }
    });
    
    // Set raw image source from GitHub CDN
    const filename = repoData.files[currentIndex];
    imgEl.src = repoData.baseUrl + filename;
  };
  
  // Fade in image when loaded and hide spinner
  imgEl.addEventListener('load', () => {
    spinnerEl.style.display = 'none';
    imgEl.style.opacity = '1';
    
    // If fullscreen lightbox is open, synchronize its image source as well
    const lightbox = document.getElementById('screenshot-lightbox');
    if (lightbox && lightbox.classList.contains('active') && activeCardImgEl === imgEl) {
      const lightboxImg = lightbox.querySelector('.screenshot-lightbox-img');
      if (lightboxImg) {
        lightboxImg.src = imgEl.src;
      }
    }
  });
  
  // Prev navigation
  overlay.querySelector('.screenshot-nav-prev').addEventListener('click', (e) => {
    e.stopPropagation();
    let prevIdx = currentIndex - 1;
    if (prevIdx < 0) prevIdx = repoData.files.length - 1;
    updateImage(prevIdx);
  });
  
  // Next navigation
  overlay.querySelector('.screenshot-nav-next').addEventListener('click', (e) => {
    e.stopPropagation();
    let nextIdx = (currentIndex + 1) % repoData.files.length;
    updateImage(nextIdx);
  });
  
  // Close overlay
  overlay.querySelector('.screenshot-close-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    overlay.classList.remove('active');
  });

  // Expand (Larger View) handler
  overlay.querySelector('.screenshot-expand-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    const lightbox = document.getElementById('screenshot-lightbox');
    const lightboxImg = lightbox.querySelector('.screenshot-lightbox-img');
    if (lightbox && lightboxImg) {
      // Store references to this card's controllers for fullscreen navigation
      activeCardPrevBtn = overlay.querySelector('.screenshot-nav-prev');
      activeCardNextBtn = overlay.querySelector('.screenshot-nav-next');
      activeCardImgEl = imgEl;
      
      lightboxImg.src = imgEl.src;
      lightbox.classList.add('active');
    }
  });
  
  // Prevent click propagation within the overlay to keep the repository link safe
  overlay.addEventListener('click', (e) => {
    e.stopPropagation();
  });
  
  // Display initial image
  updateImage(0);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  fetchGithubStats();
  initSpotlightEffect();
  initHeaderScroll();
  initScrollRevealFallback();
  
  // Set up tab button listeners
  const tabButtons = document.querySelectorAll('.tab-btn');
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const category = btn.getAttribute('data-filter');
      filterProjects(category);
    });
  });

  // Set up screenshot buttons click listeners
  const screenshotButtons = document.querySelectorAll('.btn-screenshot');
  screenshotButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      
      const repoName = btn.getAttribute('data-repo');
      const card = btn.closest('.project-card');
      if (!card) return;
      
      let overlay = card.querySelector('.screenshot-preview-overlay');
      if (!overlay) {
        overlay = createScreenshotOverlay(card, repoName);
      }
      
      // Trigger browser reflow and show overlay
      overlay.offsetHeight;
      overlay.classList.add('active');
    });
  });

  // Fullscreen Lightbox setup and close listeners
  const lightbox = document.getElementById('screenshot-lightbox');
  if (lightbox) {
    const closeLightbox = () => {
      lightbox.classList.remove('active');
      activeCardPrevBtn = null;
      activeCardNextBtn = null;
      activeCardImgEl = null;
    };
    
    lightbox.querySelector('.screenshot-lightbox-close').addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', closeLightbox);
    lightbox.querySelector('.screenshot-lightbox-img').addEventListener('click', (e) => {
      e.stopPropagation(); // Prevent closing when clicking the image content
    });

    // Lightbox navigation bindings (synchronizes with card indices)
    const prevLightboxBtn = lightbox.querySelector('.screenshot-lightbox-nav-prev');
    if (prevLightboxBtn) {
      prevLightboxBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (activeCardPrevBtn) {
          activeCardPrevBtn.click();
        }
      });
    }

    const nextLightboxBtn = lightbox.querySelector('.screenshot-lightbox-nav-next');
    if (nextLightboxBtn) {
      nextLightboxBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (activeCardNextBtn) {
          activeCardNextBtn.click();
        }
      });
    }
  }

  // Mobile navigation drawer toggle
  const mobileToggle = document.getElementById('mobile-toggle');
  const navMenu = document.getElementById('nav-menu');
  
  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      mobileToggle.classList.toggle('active');
      navMenu.classList.toggle('active');
    });
    
    // Close menu when a link is clicked
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileToggle.classList.remove('active');
        navMenu.classList.remove('active');
      });
    });
  }
});
