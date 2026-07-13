// Mapping from GitHub repository name (lowercase) to DOM ID suffix
const repoMap = {
  'adaptive-brightness-linux': 'adaptive-brightness-linux',
  'leantype': 'leantype',
  'leantype-handwriting-plugin': 'leantype-handwriting-plugin',
  'ltvlauncher': 'ltvlauncher',
  'lwidget': 'lwidget'
};

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
      card.classList.add('filtered-out');
      
      const onTransitionEnd = () => {
        if (card.classList.contains('filtered-out')) {
          card.style.display = 'none';
        }
        card.removeEventListener('transitionend', onTransitionEnd);
      };
      card.addEventListener('transitionend', onTransitionEnd);
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
