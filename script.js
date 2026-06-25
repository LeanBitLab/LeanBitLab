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
        // Update Stars
        const starsEl = document.getElementById(`stars-${domId}`);
        if (starsEl) {
          starsEl.textContent = formatNumber(repo.stargazers_count);
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
              downloadsEl.textContent = formatNumber(downloadsCount);
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

// Filter projects by category tab
function filterProjects(category) {
  const cards = document.querySelectorAll('.project-card');
  const buttons = document.querySelectorAll('.tab-btn');
  
  buttons.forEach(btn => {
    if (btn.outerHTML.includes(`'${category}'`)) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  cards.forEach(card => {
    const cardCategory = card.getAttribute('data-category');
    if (category === 'all' || cardCategory === category) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

// Shrink header on scroll
window.addEventListener('scroll', () => {
  const header = document.querySelector('header');
  if (window.scrollY > 50) {
    header.style.background = 'rgba(8, 12, 16, 0.95)';
    header.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.3)';
  } else {
    header.style.background = 'rgba(8, 12, 16, 0.7)';
    header.style.boxShadow = 'none';
  }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  fetchGithubStats();
  
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
