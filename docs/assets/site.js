(() => {
  const valid = ['r', 'stata', 'python'];
  function selectLanguage(language, updateUrl = true) {
    if (!valid.includes(language)) language = 'r';
    document.querySelectorAll('[data-lang]').forEach(panel => {
      panel.hidden = panel.dataset.lang !== language;
    });
    document.querySelectorAll('[data-select-lang]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.selectLang === language));
    });
    document.querySelectorAll('a[href]').forEach(link => {
      if (link.closest('.hero-languages, .package-card')) return;
      const url = new URL(link.href);
      if (url.origin !== location.origin || !['/get-started/', '/empirical-example/'].some(path => url.pathname.endsWith(path))) return;
      url.searchParams.set('lang', language);
      link.href = url.href;
    });
    if (updateUrl) {
      const url = new URL(location.href);
      url.searchParams.set('lang', language);
      history.replaceState(null, '', url);
    }
  }
  document.querySelectorAll('[data-select-lang]').forEach(button => {
    button.addEventListener('click', () => selectLanguage(button.dataset.selectLang));
  });
  selectLanguage(new URLSearchParams(location.search).get('lang') || 'r', false);
  window.addEventListener('popstate', () => selectLanguage(new URLSearchParams(location.search).get('lang') || 'r', false));
  document.querySelectorAll('.highlight').forEach(block => {
    const code = block.querySelector('code');
    if (!code) return;
    const button = document.createElement('button');
    button.className = 'copy-button';
    button.type = 'button';
    button.textContent = 'Copy';
    button.setAttribute('aria-label', 'Copy code');
    button.setAttribute('aria-live', 'polite');
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(code.textContent);
        button.textContent = 'Copied';
      } catch {
        button.textContent = 'Select code';
        const range = document.createRange();
        range.selectNodeContents(code);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
      }
      window.setTimeout(() => { button.textContent = 'Copy'; }, 1800);
    });
    block.append(button);
  });
})();
