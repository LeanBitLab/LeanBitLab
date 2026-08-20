// Mapping from GitHub repository name (lowercase) to DOM ID suffix
const repoMap = {
  'adaptive-brightness-linux': 'adaptive-brightness-linux',
  'leantype': 'leantype',
  'leantype-handwriting-plugin': 'leantype-handwriting-plugin',
  'leantype-translation-plugin': 'leantype-translation-plugin',
  'leantype-voice-plugin': 'leantype-voice-plugin',
  'ltvlauncher': 'ltvlauncher',
  'lwidget': 'lwidget',
  'rdtube': 'rdtube'
};

// Database mapping of repositories to their screenshot files and raw URL paths
const repoScreenshots = {
  'leantype': {
    baseUrl: 'https://raw.githubusercontent.com/LeanBitLab/LeanType/main/docs/images/',
    files: ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
  },
  'ltvlauncher': {
    baseUrl: 'https://raw.githubusercontent.com/leanbitlab-org/LtvLauncher/master/docs/images/',
    files: ['screenshot_1.png', 'screenshot_2.png', 'screenshot_3.png', 'screenshot_4.png']
  },
  'lwidget': {
    baseUrl: 'https://raw.githubusercontent.com/LeanBitLab/Lwidget/main/docs/images/',
    files: ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png']
  },
  'adaptive-brightness-linux': {
    baseUrl: 'https://raw.githubusercontent.com/LeanBitLab/adaptive-brightness-linux/master/docs/screenshots/',
    files: ['1.png', '2.png']
  },
  'rdtube': {
    baseUrl: 'https://raw.githubusercontent.com/LeanBitLab/RdTube/main/docs/images/',
    files: ['R1.png', 'R2.png', 'R3.png', 'R4.png', 'R5.png']
  }
};

// Config mapping of repositories to their raw README files and features section headers
const readmeConfig = {
  'leantype': {
    url: 'https://raw.githubusercontent.com/LeanBitLab/LeanType/main/README.md',
    header: "## What's New in LeanType"
  },
  'ltvlauncher': {
    url: 'https://raw.githubusercontent.com/leanbitlab-org/LtvLauncher/master/README.md',
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
  'leantype-translation-plugin': {
    url: 'https://raw.githubusercontent.com/LeanBitLab/Leantype-Translation-Plugin/main/README.md',
    header: "## How it works"
  },
  'leantype-voice-plugin': {
    url: 'https://raw.githubusercontent.com/LeanBitLab/LeanType-Voice-Plugin/master/README.md',
    header: "## Architecture"
  },
  'adaptive-brightness-linux': {
    url: 'https://raw.githubusercontent.com/LeanBitLab/adaptive-brightness-linux/master/README.md',
    header: "## 🚀 Key Features"
  },
  'rdtube': {
    url: 'https://raw.githubusercontent.com/LeanBitLab/RdTube/main/README.md',
    header: "## Features"
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
  'leantype-translation-plugin': [
    '<strong>🌐 Direct Integration</strong> - Translation plugin enabling Google Translate directly within the LeanType keyboard.',
    '<strong>Dynamic Plugin Loader</strong> - Core keyboard loads translation APK dynamically when enabled by the user.'
  ],
  'leantype-voice-plugin': [
    '<strong>🎙️ Offline Whisper Engine</strong> - Native whisper.cpp integration with ARM64 NEON optimizations.',
    '<strong>⚡ AIDL IPC Interface</strong> - Standardized IVoiceEngine contract with real-time audio streaming.',
    '<strong>📦 Async Model Management</strong> - Non-blocking background model imports and on-demand unloading.',
    '<strong>🔒 100% Private</strong> - Zero network permissions required; all voice processing stays strictly on-device.'
  ],
  'adaptive-brightness-linux': [
    '<strong>📈 Interactive Spline Curve</strong> - Draggable spline nodes to adjust 24-hour target levels in real time.',
    '<strong>☀️ Circular Brightness Dial</strong> - Clean visual dial indicating current brightness and manual offsets.',
    '<strong>⚙️ System Control Center</strong> - Enable/disable daemon, adjust now, restart timer, and clear overrides.',
    '<strong>⏸️ Advanced Pause Controls</strong> - Temporarily pause auto adjustments for 1h, 3h, 8h, or indefinitely.',
    '<strong>🎨 Visual Profile Editor</strong> - Add, edit, or delete dynamic time blocks and target levels.',
    '<strong>💾 Force Learn Profiles</strong> - Instantly save manual override offsets into active time block memory.',
    '<strong>🔄 Restore Defaults</strong> - Instantly resets curves to factory-calibrated defaults.'
  ],
  'rdtube': [
    '<strong>🔑 No API Key Required</strong> - Works instantly right after installation with zero setup or API client registration.',
    '<strong>👤 No Account Required</strong> - 100% anonymous browsing out of the box with zero sign-in or Reddit credentials required.',
    '<strong>📱 Single-Column & Vertical Pager Feeds</strong> - Smooth vertical video scrolling with instant background prefetching.',
    '<strong>🎬 Media3 ExoPlayer Engine</strong> - Integrated video player supporting dynamic playback speed, quality selector, and automatic lifecycle pause.',
    '<strong>🔁 Auto-Play & Auto-Rotate</strong> - Toggle continuous auto-next video playback and sensor orientation lock.',
    '<strong>⬇️ Video Downloads</strong> - Save Reddit videos directly to your device storage with audio-video merging.',
    '<strong>🎛️ Volume & Brightness Gestures</strong> - Intuitive edge drag gesture controls for volume and brightness.',
    '<strong>⚡ Parallel Coroutine Fetching</strong> - High-throughput multi-subreddit API requests (3x–5x faster feed load times).',
    '<strong>🔍 Subreddit Search & Subscriptions</strong> - Search subreddits instantly and manage custom subscriptions stored 100% locally.',
    '<strong>📜 Local Persistence & History</strong> - Watch history, liked videos, and preferences stay on your device.',
    '<strong>🎨 Obsidian Dark Theme</strong> - Glassmorphism UI, vibrant crimson accents (#FF2A4B), and rounded edge styling.'
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

// Fetch pre-computed statistics from local stats.json
async function fetchGithubStats() {
  try {
    const response = await fetch('./stats.json');
    if (!response.ok) throw new Error('Failed to load stats.json');
    
    const statsData = await response.json();
    
    for (const [repoKey, data] of Object.entries(statsData)) {
      const domId = repoMap[repoKey];
      if (domId) {
        const starsEl = document.getElementById(`stars-${domId}`);
        if (starsEl) {
          animateStat(starsEl, data.stars);
        }
        
        const downloadsEl = document.getElementById(`downloads-${domId}`);
        if (downloadsEl) {
          animateStat(downloadsEl, data.downloads);
        }
      }
    }
  } catch (error) {
    console.warn('Using pre-rendered static stats for project cards:', error);
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

  // Touch swipe support for mobile
  let touchStartX = 0;
  let touchEndX = 0;
  const imgWrapper = overlay.querySelector('.screenshot-img-wrapper');
  if (imgWrapper) {
    imgWrapper.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    imgWrapper.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      const swipeThreshold = 35;
      if (touchEndX < touchStartX - swipeThreshold) {
        // Swiped left -> Next
        let nextIdx = (currentIndex + 1) % repoData.files.length;
        updateImage(nextIdx);
      } else if (touchEndX > touchStartX + swipeThreshold) {
        // Swiped right -> Prev
        let prevIdx = currentIndex - 1;
        if (prevIdx < 0) prevIdx = repoData.files.length - 1;
        updateImage(prevIdx);
      }
    }, { passive: true });
  }
  
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

// Shuffle array using Fisher-Yates
function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// Render sponsor bubbles packed inside a pill like balls resting at the bottom of a container
function renderSponsors(view) {
  const container = document.getElementById('sponsors-bubbles');
  if (!container || typeof sponsorData === 'undefined') return;

  const data = sponsorData[view];
  if (!data || data.length === 0) {
    container.innerHTML = '<p style="color: var(--text-secondary); font-size: 14px;">No sponsors this month yet.</p>';
    return;
  }

  container.innerHTML = '';

  const isMobile = window.innerWidth < 768;
  const GAP = 4;

  // Pill dimensions — centered with margin: 0 auto, fluid on small devices
  const availableWidth = Math.max(280, window.innerWidth - 32);
  const pillWidth = isMobile ? Math.min(availableWidth, 380) : 820;
  const pillHeight = isMobile ? Math.min(240, Math.max(200, Math.round(pillWidth * 0.68))) : 300;
  const pillR = pillHeight / 2;

  container.style.width = pillWidth + 'px';
  container.style.maxWidth = '100%';
  container.style.height = pillHeight + 'px';

  // Area of pill stadium: rectangle + 2 semicircles = (W - H)*H + PI*(H/2)^2
  const pillArea = (pillWidth - pillHeight) * pillHeight + Math.PI * Math.pow(pillR, 2);
  const PACKING_FACTOR = 0.52; // fraction of container area allocated for 100% capacity fill

  // Build circles array with radii mathematically proportional to $700 / $1000 container capacity
  const totalCount = data.length;
  const circles = shuffleArray(data).map((sponsor, i) => {
    const circleArea = (sponsor.ratio || 0.001) * pillArea * PACKING_FACTOR;
    const rFromArea = Math.sqrt(circleArea / Math.PI);
    const minR = isMobile ? (pillWidth < 340 ? 10 : 12) : 14;
    const maxR = pillR - 6; // Max radius allowing unclamped 50%+ ratio balls
    const radius = Math.max(minR, Math.min(maxR, rFromArea));

    // Distribute initial X evenly across full pill width (from left cap to right cap)
    const margin = radius + 10;
    const x = margin + (i / Math.max(1, totalCount - 1)) * (pillWidth - 2 * margin);
    const y = radius + 10 + Math.random() * (pillHeight * 0.25);
    return {
      sponsor,
      r: radius,
      x,
      y
    };
  });

  // Sort largest first for priority placement
  circles.sort((a, b) => b.r - a.r);

  // Constrain circle center strictly inside stadium pill
  function constrainToPill(c) {
    const pad = c.r + 4;
    const maxR = pillR - pad;
    if (maxR <= 0) return;

    // Left cap
    if (c.x < pillR) {
      const dx = c.x - pillR;
      const dy = c.y - pillR;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist > maxR && dist > 0) {
        c.x = pillR + (dx / dist) * maxR;
        c.y = pillR + (dy / dist) * maxR;
      }
    }
    // Right cap
    else if (c.x > pillWidth - pillR) {
      const dx = c.x - (pillWidth - pillR);
      const dy = c.y - pillR;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist > maxR && dist > 0) {
        c.x = (pillWidth - pillR) + (dx / dist) * maxR;
        c.y = pillR + (dy / dist) * maxR;
      }
    }
    // Center rectangle section
    else {
      c.y = Math.max(pad, Math.min(pillHeight - pad, c.y));
    }
    c.x = Math.max(pad, Math.min(pillWidth - pad, c.x));
  }

  // Physics simulation steps (downward gravity + collision separation + wall bounds)
  const ITERATIONS = 400;

  for (let iter = 0; iter < ITERATIONS; iter++) {
    // 1. Downward gravity
    for (const c of circles) {
      c.y += 0.5;
    }

    // 2. Collision resolution between overlapping balls
    for (let i = 0; i < circles.length; i++) {
      for (let j = i + 1; j < circles.length; j++) {
        const a = circles[i];
        const b = circles[j];
        let dx = b.x - a.x;
        let dy = b.y - a.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        if (dist === 0) {
          dx = (Math.random() - 0.5) * 2;
          dy = (Math.random() - 0.5) * 2;
          dist = Math.sqrt(dx * dx + dy * dy);
        }
        const minDist = a.r + b.r + GAP;
        if (dist < minDist) {
          const overlap = (minDist - dist) / 2;
          const nx = dx / dist;
          const ny = dy / dist;
          a.x -= nx * overlap;
          a.y -= ny * overlap;
          b.x += nx * overlap;
          b.y += ny * overlap;
        }
      }
    }

    // 3. Wall constraint
    for (const c of circles) {
      constrainToPill(c);
    }
  }

  // Render the settled balls inside container
  circles.forEach((c) => {
    const baseWidth = Math.round(c.r * 2);
    const name = c.sponsor.name;
    const isMultiWord = name.includes(' ');

    const maxWordLength = isMultiWord
      ? Math.max(...name.split(' ').map(w => w.length))
      : name.length;

    // Dynamically calculate font size per circle name (non-hover)
    // Sized so name fits inside available circle width if possible (clamped 7.5px - 14px)
    const idealFontSize = parseFloat(((baseWidth * 0.80) / (maxWordLength * 0.58)).toFixed(1));
    const fontSize = Math.max(7.5, Math.min(14, idealFontSize));

    const x = c.x - c.r;
    const y = c.y - c.r;

    // Calculate text width needed at standard hover font size (11.5px on mobile, 13px on desktop)
    const hoverFontSize = isMobile ? 11.5 : 13;
    const hoverTextWidth = maxWordLength * (hoverFontSize * 0.65);
    const availableWidthAtHoverFont = baseWidth * 0.72;

    let hoverWidth = baseWidth;
    if (hoverTextWidth > availableWidthAtHoverFont) {
      // Expand circle diameter so hover font fits comfortably inside with padding
      const maxAllowedHoverWidth = isMobile ? (pillWidth - 16) : (pillWidth - 24);
      const computedHoverWidth = Math.ceil((hoverTextWidth / 0.66) + 18);
      hoverWidth = Math.min(maxAllowedHoverWidth, computedHoverWidth);
    }

    const offsetX = -Math.round((hoverWidth - baseWidth) / 2);
    const offsetY = -Math.round((hoverWidth - baseWidth) / 2);

    const isLink = !!c.sponsor.github;
    const el = document.createElement(isLink ? 'a' : 'div');
    el.className = `sponsor-bubble tier-${c.sponsor.tier} ${isMultiWord ? 'multi-word' : 'single-word'}`;
    el.style.setProperty('--base-width', `${baseWidth}px`);
    el.style.setProperty('--hover-width', `${hoverWidth}px`);
    el.style.setProperty('--offset-x', `${offsetX}px`);
    el.style.setProperty('--offset-y', `${offsetY}px`);
    el.style.setProperty('--font-size', `${fontSize}px`);
    el.style.left = `${x}px`;
    el.style.top = `${y}px`;

    if (isLink) {
      el.href = `https://github.com/${c.sponsor.github}`;
      el.target = '_blank';
      el.rel = 'noopener noreferrer';
    }

    const nameSpanEl = document.createElement('span');
    nameSpanEl.className = 'sponsor-bubble-name';
    nameSpanEl.textContent = name;
    el.appendChild(nameSpanEl);

    container.appendChild(el);
  });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  fetchGithubStats();
  initSpotlightEffect();
  initHeaderScroll();
  initScrollRevealFallback();

  // Render sponsor bubbles
  renderSponsors('allTime');

  // Sponsor view toggle
  const toggleBtns = document.querySelectorAll('.sponsor-toggle-btn');
  toggleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      toggleBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderSponsors(btn.getAttribute('data-view'));
    });
  });
  
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

    // Touch swipe support for fullscreen lightbox
    let lbTouchStartX = 0;
    let lbTouchEndX = 0;
    lightbox.addEventListener('touchstart', (e) => {
      lbTouchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    lightbox.addEventListener('touchend', (e) => {
      lbTouchEndX = e.changedTouches[0].screenX;
      const threshold = 40;
      if (lbTouchEndX < lbTouchStartX - threshold && activeCardNextBtn) {
        activeCardNextBtn.click();
      } else if (lbTouchEndX > lbTouchStartX + threshold && activeCardPrevBtn) {
        activeCardPrevBtn.click();
      }
    }, { passive: true });
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

  // Mobile navigation drawer toggle with scroll lock and outside-click dismissal
  const mobileToggle = document.getElementById('mobile-toggle');
  const navMenu = document.getElementById('nav-menu');
  
  if (mobileToggle && navMenu) {
    const closeMenu = () => {
      mobileToggle.classList.remove('active');
      navMenu.classList.remove('active');
      document.body.classList.remove('menu-open');
    };

    mobileToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const isActive = navMenu.classList.toggle('active');
      mobileToggle.classList.toggle('active', isActive);
      document.body.classList.toggle('menu-open', isActive);
    });
    
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        closeMenu();
      });
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (navMenu.classList.contains('active') && !navMenu.contains(e.target) && !mobileToggle.contains(e.target)) {
        closeMenu();
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navMenu.classList.contains('active')) {
        closeMenu();
      }
    });
  }

  // Active scroll-spy for desktop and mobile navigation links
  const sections = document.querySelectorAll('section[id], footer[id]');
  const navLinksAll = document.querySelectorAll('.nav-link');

  const onScrollSpy = () => {
    // Check if user has scrolled to the bottom of the page
    const isAtBottom = (window.innerHeight + window.scrollY) >= (document.documentElement.scrollHeight - 60);

    if (isAtBottom) {
      navLinksAll.forEach(link => {
        if (link.getAttribute('href') === '#contact') {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
      return;
    }

    const scrollPos = window.scrollY + 140;
    let currentId = '';

    sections.forEach(sec => {
      const top = sec.offsetTop;
      const height = sec.offsetHeight;
      if (scrollPos >= top && scrollPos < top + height) {
        currentId = sec.getAttribute('id');
      }
    });

    navLinksAll.forEach(link => {
      const href = link.getAttribute('href');
      if (href === '#' + currentId) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  };

  window.addEventListener('scroll', onScrollSpy, { passive: true });
  onScrollSpy();

  // Handle window resize dynamically for sponsor bubbles
  let resizeDebounce;
  window.addEventListener('resize', () => {
    clearTimeout(resizeDebounce);
    resizeDebounce = setTimeout(() => {
      const activeToggle = document.querySelector('.sponsor-toggle-btn.active');
      const view = activeToggle ? activeToggle.getAttribute('data-view') : 'allTime';
      renderSponsors(view);
      onScrollSpy();
    }, 150);
  });
});
