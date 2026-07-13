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

// Config mapping of repositories to their raw README files and features section headers
const readmeConfig = {
  'leantype': {
    url: 'https://raw.githubusercontent.com/LeanBitLab/LeanType/main/README.md',
    header: "## What's New in LeanType"
  },
  'ltvlauncher': {
    url: 'https://raw.githubusercontent.com/LeanBitLab/LtvLauncher/master/README.md',
    header: "## Key Features & Enhancements"
  },
  'lwidget': {
    url: 'https://raw.githubusercontent.com/LeanBitLab/Lwidget/main/README.md',
    header: "## Features"
  },
  'leantype-handwriting-plugin': {
    url: 'https://raw.githubusercontent.com/LeanBitLab/Leantype-Handwriting-Plugin/main/README.md',
    header: "## How it works"
  },
  'adaptive-brightness-linux': {
    url: 'https://raw.githubusercontent.com/LeanBitLab/adaptive-brightness-linux/master/README.md',
    header: "## 🚀 Key Features"
  }
};

// Static features backup database to serve as fallbacks in case of rate limits or offline state
const fallbackFeatures = {
  'leantype': [
    '<strong>🤖 Multi-Provider AI</strong> - Proofread using Gemini, Groq, or OpenAI-compatible providers.',
    '<strong>🛡️ Offline AI (GGUF)</strong> - Private, on-device translation using local GGUF models powered by llama.cpp.',
    '<strong>🌐 AI Translation</strong> - Translate selected text directly using your chosen AI provider.',
    '<strong>🧠 Custom AI Keys</strong> - Assign custom prompts, personas, and themed capsules to 10 customizable keys.',
    '<strong>🧭 Text Editing Mode</strong> - Gboard-style panel with precise DPAD navigation and editing utilities.',
    '<strong>✍️ Handwriting Input</strong> - Support handwriting recognition canvas using dynamic plugin imports.',
    '<strong>👆 Gesture Typing</strong> - Built-in gesture engine removing dependency on proprietary Google binaries.',
    '<strong>🖱️ Touchpad Mode</strong> - Swipe spacebar up to toggle touchpad with custom sensitivity controls.',
    '<strong>📝 Text Expander</strong> - Built-in expansion tool supporting custom shortcuts and template variables.',
    '<strong>🪟 Floating Keyboard</strong> - Detach the keyboard into a draggable window for seamless multitasking.',
    '<strong>⌨️ Dual Toolbar / Split Suggestions</strong> - Option to split suggestions and toolbar for easier access.',
    '<strong>📥 Dynamic Downloader</strong> - Standard version dynamically downloads layout/emoji dictionaries on demand.',
    '<strong>🔍 Clipboard Search & Undo</strong> - Search through clipboard history and undo accidental item deletions.',
    '<strong>📸 Screenshot Suggestion & Clipboard</strong> - Suggests recently taken screenshots for quick suggestion strip sharing.',
    '<strong>🔎 Emoji Search</strong> - Search for emojis by name.',
    '<strong>🚫 Blocked Words Blacklist</strong> - Prevent unwanted words from being suggested with regex pattern support.',
    '<strong>✉️ Auto-Read OTP</strong> - Automatically reads OTP codes from SMS notifications for quick entry.',
    '<strong>💾 Selective Backup & Restore</strong> - Backup and restore settings and AI configurations selectively.',
    '<strong>⌨️ Direct Switch IME</strong> - Map custom keycode to any toolbar key to switch directly to another input method.',
    '<strong>🎨 Custom Layouts</strong> - Save up to five custom layout profiles with persistent slot tracking.',
    '<strong>🔒 Privacy Choices</strong> - Choose Standard, Offline (no network), or Offline Lite (minimalist) versions.',
    '<strong>🎨 Modern UI</strong> - "Squircle" key backgrounds, refined icons, and polished aesthetics.',
    '<strong>🕵️ Clear Incognito Mode</strong> - Distinct "Hat & Glasses" icon for clear visibility.',
    '<strong>🔄 Google Dictionary Import</strong> - Easily import your personal dictionary words.',
    '<strong>⚙️ Enhanced Customization</strong> - Force auto-capitalization toggle, reorganized settings, and more.'
  ],
  'ltvlauncher': [
    '<strong>📊 Data Usage Widget</strong> - Track WiFi, Ethernet, and Mobile consumption directly from status bar.',
    '<strong>🛡️ Inbuilt OLED Screensaver</strong> - Minimal screensaver with 30s clock position shifting to prevent burn-in.',
    '<strong>🔌 Easy WiFi Access</strong> - Network indicator doubles as a shortcut to system WiFi settings.',
    '<strong>⏱️ Quick Presets</strong> - Select Time/Date formats and Category names from a list without a keyboard.',
    '<strong>☀️ Time-Based Wallpaper</strong> - Automatically switches between custom day and night backgrounds.',
    '<strong>🌑 Pitch Black Wallpaper</strong> - Added a true black gradient background option.',
    '<strong>🔳 Focus Indicator</strong> - New double-border design ensures perfect visibility on any background.',
    '<strong>🧭 Smart Navigation</strong> - Fixed "bounce back" issues and optimized focus traversal.',
    '<strong>⚙️ Refined Settings</strong> - Reorganized menus with a new "Miscellaneous" section.',
    '<strong>🎨 Accent Color Support</strong> - Personalize the UI with multiple color presets.',
    '<strong>👕 Themes</strong> - Switch between distinct styles (Default, Premium, Classic, Capsule).',
    '<strong>🎭 Focus Customization</strong> - Toggle focus outline and transition animations.',
    '<strong>💥 Edge Bump Animation</strong> - Visual feedback when reaching the edge of a row.'
  ],
  'lwidget': [
    '<strong>📱 Unified Android Widget</strong> - Track time, calendar events, tasks, battery, and mobile data usage.',
    '<strong>🎨 Material 3 Principles</strong> - Modern components built with dynamic system coloring support.',
    '<strong>🌿 100% Free & FOSS</strong> - Bloat-free, resource-respecting, and completely open source with absolute privacy.'
  ],
  'leantype-handwriting-plugin': [
    '<strong>Dynamic Plugin loader</strong> - APK isolates Google ML Kit Digital Ink Recognition to comply with FOSS guidelines.',
    '<strong>DexClassLoader Engine</strong> - Core keyboard loads the handwriting APK dynamically only when imported by the user.'
  ],
  'adaptive-brightness-linux': [
    '<strong>📈 Interactive Spline Curve</strong> - Draggable spline nodes to adjust 24-hour target levels in real time.',
    '<strong>☀️ Circular Brightness Dial</strong> - Clean visual dial indicating current brightness and manual offsets.',
    '<strong>⚙️ System Control Center</strong> - Enable/disable daemon, adjust now, restart timer, and clear overrides.',
    '<strong>⏸️ Advanced Pause Controls</strong> - Temporarily pause auto adjustments for 1h, 3h, 8h, or indefinitely.',
    '<strong>🎨 Visual Profile Editor</strong> - Add, edit, or delete dynamic time blocks and target levels.',
    '<strong>💾 Force Learn Profiles</strong> - Instantly save manual override offsets into active time block memory.',
    '<strong>🔄 Restore Defaults</strong> - Instantly resets curves to factory-calibrated defaults.'
  ]
};

// Memory cache to prevent duplicate fetch requests
const featuresCache = {};

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

// Filter projects by category tab
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
      card.offsetHeight; 
      card.classList.add('filtered-in');
    } else {
      card.classList.remove('filtered-in');
      card.style.display = 'none';
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

// Fixed header scrolled styles toggler
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

// Helper to extract feature bullets under a specific heading inside README markdown text
function extractFeatures(markdownText, repoName) {
  const config = readmeConfig[repoName];
  if (!config) return null;

  const targetHeader = config.header;
  const headerIdx = markdownText.indexOf(targetHeader);
  if (headerIdx === -1) return null;

  const contentStart = headerIdx + targetHeader.length;
  let contentEnd = markdownText.length;
  const nextHeaderRegex = /\n##[#]?\s+/g;
  nextHeaderRegex.lastIndex = contentStart;
  
  const nextHeaderMatch = nextHeaderRegex.exec(markdownText);
  if (nextHeaderMatch) {
    contentEnd = nextHeaderMatch.index;
  }

  const sectionContent = markdownText.substring(contentStart, contentEnd).trim();
  const lines = sectionContent.split('\n');
  const items = [];

  lines.forEach(line => {
    const trimmed = line.trim();
    if (trimmed.startsWith('-') || trimmed.startsWith('*')) {
      let bullet = trimmed.substring(1).trim();
      // Replace bold markdown formatting
      bullet = bullet.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
      // Replace italics markdown formatting
      bullet = bullet.replace(/\*([^*]+)\*/g, '<em>$1</em>');
      // Replace markdown links with secure HTML links
      bullet = bullet.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
      items.push(bullet);
    } else if (repoName === 'leantype-handwriting-plugin' && trimmed.length > 0) {
      let para = trimmed;
      para = para.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
      para = para.replace(/\*([^*]+)\*/g, '<em>$1</em>');
      para = para.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
      items.push(para);
    }
  });

  return items.length > 0 ? items : null;
}

// Lazy create the inline scrollable features list overlay container inside a card
function createFeaturesOverlay(card, repoName) {
  const overlay = document.createElement('div');
  overlay.className = 'features-preview-overlay';
  overlay.innerHTML = `
    <button class="screenshot-close-btn" aria-label="Close Features">&times;</button>
    <button class="screenshot-expand-btn" aria-label="Expand Features View">&#x2922;</button>
    
    <button class="features-scroll-btn features-scroll-up" aria-label="Scroll Up">&#x25B2;</button>
    <div class="features-title">Features</div>
    <div class="features-viewport">
      <div class="screenshot-spinner" style="position: static; margin: 30px auto;"></div>
      <ul class="features-list"></ul>
    </div>
    <button class="features-scroll-btn features-scroll-down" aria-label="Scroll Down">&#x25BC;</button>
  `;
  card.appendChild(overlay);

  initFeaturesNav(overlay, repoName);
  return overlay;
}

// Fetch features list and bind the scroll up/down buttons
async function initFeaturesNav(overlay, repoName) {
  const closeBtn = overlay.querySelector('.screenshot-close-btn');
  const expandBtn = overlay.querySelector('.screenshot-expand-btn');
  const viewport = overlay.querySelector('.features-viewport');
  const listEl = overlay.querySelector('.features-list');
  const spinnerEl = overlay.querySelector('.screenshot-spinner');
  
  const scrollUpBtn = overlay.querySelector('.features-scroll-up');
  const scrollDownBtn = overlay.querySelector('.features-scroll-down');

  // Close overlay handler
  closeBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    overlay.classList.remove('active');
  });

  // Expand features fullscreen handler
  expandBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const lightbox = document.getElementById('features-lightbox');
    const lightboxList = lightbox.querySelector('.features-lightbox-list');
    if (lightbox && lightboxList) {
      lightboxList.innerHTML = listEl.innerHTML;
      lightbox.classList.add('active');
    }
  });

  // Scroll controls (up & down) click triggers
  scrollUpBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    viewport.scrollBy({ top: -80, behavior: 'smooth' });
  });

  scrollDownBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    viewport.scrollBy({ top: 80, behavior: 'smooth' });
  });

  // Block clicks propagating to card content
  overlay.addEventListener('click', (e) => {
    e.stopPropagation();
  });

  const renderFeatures = (features) => {
    if (spinnerEl) spinnerEl.remove();
    listEl.innerHTML = '';
    features.forEach(feat => {
      const li = document.createElement('li');
      li.innerHTML = feat;
      listEl.appendChild(li);
    });
  };

  // Serve cache if already fetched
  if (featuresCache[repoName]) {
    renderFeatures(featuresCache[repoName]);
    return;
  }

  const config = readmeConfig[repoName];
  if (!config) {
    renderFeatures(fallbackFeatures[repoName] || ['No features list available.']);
    return;
  }

  try {
    const response = await fetch(config.url);
    if (!response.ok) throw new Error('Network error');
    const text = await response.text();
    const extracted = extractFeatures(text, repoName);
    if (extracted) {
      featuresCache[repoName] = extracted;
      renderFeatures(extracted);
    } else {
      throw new Error('Parsing failed');
    }
  } catch (err) {
    console.warn(`Failed to fetch features for ${repoName}, loading fallback data:`, err);
    featuresCache[repoName] = fallbackFeatures[repoName];
    renderFeatures(fallbackFeatures[repoName]);
  }
}

// Dismiss all open card overlays (screenshots and features)
function closeAllOverlays() {
  const activeOverlays = document.querySelectorAll('.screenshot-preview-overlay.active, .features-preview-overlay.active');
  activeOverlays.forEach(overlay => {
    overlay.classList.remove('active');
  });
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
      
      // Close other active card overlays first
      closeAllOverlays();
      
      let overlay = card.querySelector('.screenshot-preview-overlay');
      if (!overlay) {
        overlay = createScreenshotOverlay(card, repoName);
      }
      
      overlay.offsetHeight;
      overlay.classList.add('active');
    });
  });

  // Set up features buttons click listeners
  const featuresButtons = document.querySelectorAll('.btn-features');
  featuresButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();

      const repoName = btn.getAttribute('data-repo');
      const card = btn.closest('.project-card');
      if (!card) return;

      // Close other active card overlays first
      closeAllOverlays();

      let overlay = card.querySelector('.features-preview-overlay');
      if (!overlay) {
        overlay = createFeaturesOverlay(card, repoName);
      }

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
      e.stopPropagation();
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

  // Fullscreen Features Lightbox close and scroll listeners
  const featuresLightbox = document.getElementById('features-lightbox');
  if (featuresLightbox) {
    const closeFeatures = () => {
      featuresLightbox.classList.remove('active');
    };
    featuresLightbox.querySelector('.features-lightbox-close').addEventListener('click', closeFeatures);
    featuresLightbox.addEventListener('click', closeFeatures);
    
    const lightboxContent = featuresLightbox.querySelector('.features-lightbox-content');
    lightboxContent.addEventListener('click', (e) => {
      e.stopPropagation();
    });

    // Lightbox Scroll Up / Down clicks
    const upBtn = featuresLightbox.querySelector('.features-lightbox-scroll-up');
    if (upBtn) {
      upBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        lightboxContent.scrollBy({ top: -150, behavior: 'smooth' });
      });
    }

    const downBtn = featuresLightbox.querySelector('.features-lightbox-scroll-down');
    if (downBtn) {
      downBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        lightboxContent.scrollBy({ top: 150, behavior: 'smooth' });
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
    
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileToggle.classList.remove('active');
        navMenu.classList.remove('active');
      });
    });
  }
});
