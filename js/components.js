/**
 * Jay Spudvilas — Shared Component System
 *
 * Injects header, mobile menu, and footer into every page automatically.
 * New pages only need:
 *   &lt;div id="js-header"&gt;&lt;/div&gt;
 *   &lt;div id="js-footer"&gt;&lt;/div&gt;
 *   &lt;script src="/js/components.js"&gt;&lt;/script&gt;
 *
 * Nav links, footer text, and branding are maintained here — one place only.
 */

const JS_SITE = {

  header: `
    <header class="header">
      <div class="header-inner">
        <div class="logo-area">
          <a href="https://jayspudvilas.com" class="logo-link" aria-label="Jay Spudvilas home">
            <svg viewBox="0 0 80 80" aria-hidden="true">
              <path d="M 20 55 Q 40 35, 60 55" stroke="#1e40af" stroke-width="3.5" fill="none" opacity="0.7" />
              <circle cx="40" cy="43" r="8" fill="#6b21a8" />
              <circle cx="60" cy="55" r="6" fill="#3E5BE8" />
            </svg>
            <span class="logo-text">Jay Spudvilas</span>
          </a>
        </div>
        <nav class="global-nav" aria-label="Primary">
          <a class="global-nav__link" href="https://glasscase.org" target="_blank" rel="noopener">GlassCase</a>
          <a class="global-nav__link" href="https://lightkey.org" target="_blank" rel="noopener">LightKey</a>
          <a class="global-nav__link" href="https://lawandlearning.com" target="_blank" rel="noopener">Law &amp; Learning</a>
          <a class="global-nav__link" href="https://jayspudvilas.com/education/">Education</a>
          <a class="global-nav__link" href="https://jayspudvilas.com/legal/">Use &amp; Privacy</a>
          <a class="global-nav__link" href="mailto:jay@jayspudvilas.com">Contact</a>
        </nav>
        <button class="js-reading-toggle" id="jsReadingToggle"
                aria-pressed="false"
                aria-label="Toggle relaxed reading spacing"
                title="Wider line spacing for easier reading">
          <span class="toggle-icon" aria-hidden="true">Aa</span>
          <span>Relaxed reading</span>
        </button>
        <button class="mobile-menu-button" onclick="toggleMobileMenu()" aria-label="Toggle menu" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </div>
    </header>
  `,

  mobileMenu: `
    <div class="mobile-menu" id="mobileMenu">
      <div class="mobile-menu-header">
        <h2 class="mobile-menu-title">Jay Spudvilas</h2>
        <p class="mobile-menu-subtitle">Fairness by Design</p>
      </div>
      <nav>
        <a href="https://glasscase.org" onclick="closeMobileMenu()" target="_blank" rel="noopener">GlassCase</a>
        <a href="https://lightkey.org" onclick="closeMobileMenu()" target="_blank" rel="noopener">LightKey</a>
        <a href="https://lawandlearning.com" onclick="closeMobileMenu()" target="_blank" rel="noopener">Law &amp; Learning</a>
        <a href="https://jayspudvilas.com/education/" onclick="closeMobileMenu()">Education</a>
        <a href="https://jayspudvilas.com/legal/" onclick="closeMobileMenu()">Use &amp; Privacy</a>
        <a href="mailto:jay@jayspudvilas.com" onclick="closeMobileMenu()">Contact</a>
      </nav>
    </div>
    <div class="mobile-menu-overlay" id="mobileMenuOverlay" onclick="closeMobileMenu()"></div>
  `,

  footer: `
    <footer class="footer">
      <div class="footer-layout">
        <section class="footer-brand">
          <a href="https://jayspudvilas.com" class="footer-logo" aria-label="Jay Spudvilas home">
            <svg viewBox="0 0 80 80" aria-hidden="true">
              <path d="M 20 55 Q 40 35, 60 55" stroke="#1e40af" stroke-width="3.5" fill="none" opacity="0.7" />
              <circle cx="40" cy="43" r="8" fill="#6b21a8" />
              <circle cx="60" cy="55" r="6" fill="#3E5BE8" />
            </svg>
            <div>
              <span class="logo-text">Jay Spudvilas</span>
              <div class="hero-tagline" style="font-size: 0.75rem; letter-spacing: 0.24em; margin-bottom: 0;">FAIRNESS BY DESIGN</div>
            </div>
          </a>
          <p>Evidence systems across education and civic-tech, designed for fairness.</p>
        </section>

        <nav class="footer-links-group" aria-label="Site and project links">
          <div class="footer-column">
            <h2 class="footer-heading">Site</h2>
            <a href="/">Home</a>
            <a href="/education/">Education</a>
            <a href="/legal/">Use &amp; Privacy</a>
          </div>
          <div class="footer-column">
            <h2 class="footer-heading">Projects</h2>
            <a href="https://glasscase.org">GlassCase</a>
            <a href="https://lightkey.org" target="_blank" rel="noopener">LightKey</a>
            <a href="https://lawandlearning.com">Law &amp; Learning</a>
          </div>
        </nav>

        <section class="footer-cta" aria-label="Join the community">
          <h2 class="footer-heading">Join the community</h2>
          <p>Updates on evidence systems and civic-tech.</p>
          <a href="https://linkedin.com/in/jayspudvilas/" class="footer-cta-button">Follow on LinkedIn</a>
        </section>
      </div>

      <div class="footer-bottom">
        <p class="footer-attribution">&copy; 2014&ndash;2026 Jay Spudvilas</p>
        <p class="footer-meta">Built in Australia &middot; Founder of GlassCase.org and Law &amp; Learning &middot; Made for everyone who believes fairness should be visible &middot; <span style="opacity: 0.6;">Information only, not legal advice</span> &middot; <a href="#" onclick="if(typeof resetAnalyticsConsent==='function')resetAnalyticsConsent();return false;" style="opacity:0.6;text-decoration:underline;">Cookie settings</a></p>
      </div>
    </footer>
  `
};

function jsInjectComponents() {
  const headerEl = document.getElementById('js-header');
  const footerEl = document.getElementById('js-footer');

  if (headerEl) headerEl.outerHTML = JS_SITE.header + JS_SITE.mobileMenu;
  if (footerEl) footerEl.outerHTML = JS_SITE.footer;
}

function toggleMobileMenu() {
  const menu = document.getElementById('mobileMenu');
  const overlay = document.getElementById('mobileMenuOverlay');
  const button = document.querySelector('.mobile-menu-button');
  if (!menu || !overlay || !button) return;
  const isOpen = menu.classList.contains('active');
  if (isOpen) {
    closeMobileMenu();
  } else {
    menu.classList.add('active');
    overlay.classList.add('active');
    button.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }
}

function closeMobileMenu() {
  const menu = document.getElementById('mobileMenu');
  const overlay = document.getElementById('mobileMenuOverlay');
  const button = document.querySelector('.mobile-menu-button');
  if (!menu || !overlay || !button) return;
  menu.classList.remove('active');
  overlay.classList.remove('active');
  button.setAttribute('aria-expanded', 'false');
  document.body.style.overflow = '';
}

function jsInitReadingToggle() {
  const btn = document.getElementById('jsReadingToggle');
  if (!btn) return;

  function shouldShow() {
    const path = window.location.pathname;
    const isHome = path === '/' || path === '/index.html';
    const isEducation = path.startsWith('/education');
    const isLegal = path.startsWith('/legal');
    const isMobile = window.matchMedia('(max-width: 720px)').matches;
    return (isHome || isEducation || isLegal) && !isMobile;
  }

  function syncVisibility() {
    btn.style.display = shouldShow() ? '' : 'none';
  }

  syncVisibility();
  window.addEventListener('resize', syncVisibility);

  btn.addEventListener('click', function() {
    const pressed = btn.getAttribute('aria-pressed') === 'true';
    btn.setAttribute('aria-pressed', String(!pressed));
    document.body.classList.toggle('reading-relaxed', !pressed);
  });
}

function jsSyncMobileHeaderCentering() {
  const headerInner = document.querySelector('.header-inner');
  const logoArea = document.querySelector('.logo-area');
  const menuButton = document.querySelector('.mobile-menu-button');
  if (!headerInner || !logoArea) return;

  const isMobile = window.matchMedia('(max-width: 720px)').matches;
  if (isMobile) {
    headerInner.style.position = 'relative';
    headerInner.style.justifyContent = 'flex-end';
    logoArea.style.position = 'absolute';
    logoArea.style.left = '50%';
    logoArea.style.transform = 'translateX(-50%)';
    logoArea.style.justifyContent = 'center';
    logoArea.style.margin = '0';
    logoArea.style.width = 'max-content';
    logoArea.style.zIndex = '100';

    if (menuButton) {
      menuButton.style.marginLeft = 'auto';
      menuButton.style.position = 'relative';
      menuButton.style.zIndex = '101';
    }
  } else {
    headerInner.style.position = '';
    headerInner.style.justifyContent = '';
    logoArea.style.position = '';
    logoArea.style.left = '';
    logoArea.style.transform = '';
    logoArea.style.justifyContent = '';
    logoArea.style.margin = '';
    logoArea.style.width = '';
    logoArea.style.zIndex = '';

    if (menuButton) {
      menuButton.style.marginLeft = '';
      menuButton.style.position = '';
      menuButton.style.zIndex = '';
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  jsInjectComponents();
  jsInitReadingToggle();
  jsSyncMobileHeaderCentering();
  window.addEventListener('resize', jsSyncMobileHeaderCentering);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMobileMenu();
  });
});
