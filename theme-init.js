// Early theme initialization to prevent Flash of Unstyled Content (FOUC)
(function () {
  try {
    var stored = localStorage.getItem('leanbitlab-theme');
    var theme = stored || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
    document.documentElement.setAttribute('data-theme', theme);
  } catch (e) {}
})();
