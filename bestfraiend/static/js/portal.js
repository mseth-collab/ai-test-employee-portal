/**
 * BestFrAIend corporate portal — all UI interactions.
 * Run: python -m bestfraiend → http://127.0.0.1:8003
 */
(function () {
  'use strict';

  const API = { chat: '/chat', feed: '/api/org-feed', sources: '/api/sources' };
  let orgFeed = null;
  let sources = [];
  let serverOk = false;

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  function toast(msg) {
    const el = document.createElement('div');
    el.className = 'toast';
    el.textContent = msg;
    $('#toast-wrap').appendChild(el);
    setTimeout(() => el.remove(), 3200);
  }

  function openModal(title, bodyHtml, actions) {
    $('#modal-title').textContent = title;
    $('#modal-body').innerHTML = bodyHtml;
    const foot = $('#modal-foot');
    foot.innerHTML = '';
    (actions || [{ label: 'Close', class: 'btn-secondary', close: true }]).forEach((a) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'btn ' + (a.class || 'btn-secondary');
      b.textContent = a.label;
      b.addEventListener('click', () => {
        if (a.onClick) a.onClick();
        if (a.close !== false) closeModal();
      });
      foot.appendChild(b);
    });
    $('#modal-backdrop').classList.add('open');
  }

  function closeModal() {
    $('#modal-backdrop').classList.remove('open');
  }

  function renderMd(text) {
    const safe = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return safe.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/_([^_]+)_/g, '<em>$1</em>');
  }

  function addBubble(text, isUser) {
    const el = document.createElement('div');
    el.className = 'bubble ' + (isUser ? 'user' : 'bot');
    el.innerHTML = isUser ? text.replace(/</g, '&lt;') : renderMd(text);
    $('#chat-messages').appendChild(el);
    el.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }

  async function sendChat(text) {
    const msg = (text || '').trim();
    if (!msg) return;
    if (!serverOk) {
      toast('Run: python -m bestfraiend then open http://127.0.0.1:8003');
      addBubble('Start the server first: **python -m bestfraiend** (do not open the HTML file directly).', false);
      return;
    }
    addBubble(msg, true);
    const input = $('#chat-input');
    const sendBtn = $('#chat-send');
    input.value = '';
    sendBtn.disabled = true;
    try {
      const res = await fetch(API.chat, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg, session_id: 'default' }),
      });
      if (!res.ok) throw new Error('fail');
      const data = await res.json();
      addBubble(data.reply || 'No response.', false);
    } catch {
      addBubble('Chat unavailable. Is the server running on port 8003?', false);
      toast('Chat API error');
    }
    sendBtn.disabled = false;
    input.focus();
  }

  function switchView(viewId) {
    $$('.view').forEach((v) => v.classList.remove('active'));
    $$('.nav-btn[data-view]').forEach((b) => b.classList.remove('active'));
    const view = $('#view-' + viewId);
    if (view) view.classList.add('active');
    const nav = document.querySelector('.nav-btn[data-view="' + viewId + '"]');
    if (nav) nav.classList.add('active');
    if (viewId === 'chat') $('#chat-input').focus();
  }

  function renderWidgets(feed) {
    ['widget-ai-news', 'widget-streams', 'widget-ongoing', 'widget-tech'].forEach((id) => {
      const el = $('#' + id);
      if (el) el.innerHTML = '';
    });

    // AI developments
    (feed.ai_news || []).slice(0, 6).forEach((n) => {
      const d = document.createElement('div');
      d.className = 'widget-ai-item';
      d.innerHTML =
        '<strong>' + n.title + '</strong>' +
        '<span class="ai-company">' + n.company + '</span>' +
        '<span class="ai-date">' + n.published + '</span>';
      d.addEventListener('click', () => showAiNews(n));
      $('#widget-ai-news').appendChild(d);
    });

    // Live streams
    (feed.streams || []).slice(0, 3).forEach((s) => {
      const d = document.createElement('div');
      d.className = 'widget-item';
      d.innerHTML = (s.status === 'live' ? '<span class="live-dot"></span>' : '') +
        '<strong>' + s.title + '</strong><small>' + s.when + '</small>';
      d.addEventListener('click', () => showStream(s));
      $('#widget-streams').appendChild(d);
    });

    // Ongoing events
    (feed.ongoing_events || []).slice(0, 3).forEach((e) => {
      const d = document.createElement('div');
      d.className = 'widget-item';
      d.innerHTML = '<strong>' + e.title + '</strong><small>' + e.when + '</small>';
      d.addEventListener('click', () => showEvent(e));
      $('#widget-ongoing').appendChild(d);
    });

    // Internal tech news
    (feed.tech_news || (feed.news || []).filter((n) => n.tag === 'Tech')).slice(0, 3).forEach((n) => {
      const d = document.createElement('div');
      d.className = 'widget-item';
      d.innerHTML = '<strong>' + n.headline + '</strong><small>' + n.published + '</small>';
      d.addEventListener('click', () => showNews(n));
      $('#widget-tech').appendChild(d);
    });
  }

  function renderFaqPanel(data) {
    const panel = $('#faq-panel');
    if (!panel) return;
    panel.innerHTML = '';
    if (!serverOk || !data || !data.categories) {
      panel.innerHTML = '<p class="empty-msg">Start the server to load FAQs: python -m bestfraiend</p>';
      return;
    }
    const CAT_ICONS = { vacation: '🏖', hr: '👤', confluence: '📖', travel: '✈', contacts: '📞' };
    data.categories.forEach((cat) => {
      const section = document.createElement('div');
      section.style.marginBottom = '1.5rem';
      const heading = document.createElement('h2');
      heading.className = 'section-sub';
      heading.textContent = (CAT_ICONS[cat.id] || '❓') + '  ' + cat.label;
      section.appendChild(heading);
      const grid = document.createElement('div');
      grid.className = 'card-grid';
      cat.faqs.forEach((faq) => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML =
          '<h3 style="font-size:0.9rem;">' + faq.question + '</h3>' +
          '<div class="card-actions" style="margin-top:0.5rem;">' +
          '<button type="button" class="btn btn-primary btn-sm">Get answer</button>' +
          '<button type="button" class="btn btn-secondary btn-sm">Ask in chat</button>' +
          '</div>';
        card.querySelector('.btn-primary').addEventListener('click', () => {
          switchView('chat');
          sendChat(faq.question);
        });
        card.querySelector('.btn-secondary').addEventListener('click', () => {
          switchView('chat');
          $('#chat-input').value = faq.question;
          $('#chat-input').focus();
        });
        grid.appendChild(card);
      });
      section.appendChild(grid);
      panel.appendChild(section);
    });
  }

  function renderPolicyCards(docs, gridId) {
    const el = $(gridId);
    if (!el) return;
    el.innerHTML = '';
    if (!docs.length) {
      el.innerHTML = '<p class="empty-msg">No documents loaded. Start the server: python -m bestfraiend</p>';
      return;
    }
    docs.forEach((doc) => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML =
        '<h3>' + doc.title + '</h3>' +
        '<div class="card-meta">' + doc.source + ' · ' + doc.id + '</div>' +
        '<p>' + doc.summary + '</p>' +
        '<div class="card-actions">' +
        '<button type="button" class="btn btn-primary btn-sm">Read policy</button>' +
        '<button type="button" class="btn btn-secondary btn-sm">Ask BestFrAIend</button></div>';
      card.querySelector('.btn-primary').addEventListener('click', () => {
        openModal(doc.title, '<p>' + doc.content + '</p><p><em>Ref: ' + doc.id + '</em></p>', [
          { label: 'Ask follow-up', class: 'btn-primary', onClick: () => { switchView('chat'); sendChat('Explain: ' + doc.title); } },
          { label: 'Close', class: 'btn-secondary', close: true },
        ]);
      });
      card.querySelector('.btn-secondary').addEventListener('click', () => {
        switchView('chat');
        sendChat(doc.title);
      });
      el.appendChild(card);
    });
  }

  async function loadPolicySection(category, gridId) {
    if (!serverOk) {
      renderPolicyCards([], gridId);
      return;
    }
    try {
      const res = await fetch('/api/knowledge/' + category);
      const data = await res.json();
      renderPolicyCards(data.documents || [], gridId);
    } catch {
      renderPolicyCards([], gridId);
    }
  }

  function renderNewsPage(feed) {
    const techEl = $('#tech-news-grid');
    const coEl = $('#company-news-grid');
    techEl.innerHTML = '';
    coEl.innerHTML = '';
    (feed.tech_news || []).forEach((n) => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = '<h3>' + n.headline + ' <span class="tag">' + n.tag + '</span></h3>' +
        '<div class="card-meta">' + n.published + '</div><p>' + n.summary + '</p>' +
        '<div class="card-actions"><button type="button" class="btn btn-primary btn-sm">Read</button></div>';
      card.querySelector('.btn-primary').addEventListener('click', () => showNews(n));
      techEl.appendChild(card);
    });
    (feed.company_news || (feed.news || []).filter((n) => n.tag !== 'Tech')).forEach((n) => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = '<h3>' + n.headline + ' <span class="tag">' + n.tag + '</span></h3>' +
        '<div class="card-meta">' + n.published + '</div><p>' + n.summary + '</p>' +
        '<div class="card-actions"><button type="button" class="btn btn-primary btn-sm">Read</button></div>';
      card.querySelector('.btn-primary').addEventListener('click', () => showNews(n));
      coEl.appendChild(card);
    });
  }

  function renderEventsPage(feed) {
    const el = $('#events-grid');
    el.innerHTML = '';
    [...(feed.ongoing_events || []), ...(feed.upcoming_events || [])].forEach((e) => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML =
        '<h3>' + e.title + ' <span class="tag">' + (e.status === 'ongoing' ? 'Ongoing' : 'Upcoming') + '</span></h3>' +
        '<div class="card-meta">' + e.when + ' · ' + e.where + '</div><p>' + e.description + '</p>' +
        '<div class="card-actions"><button type="button" class="btn btn-primary btn-sm">Details</button>' +
        '<button type="button" class="btn btn-secondary btn-sm">Ask BestFrAIend</button></div>';
      card.querySelector('.btn-primary').addEventListener('click', () => showEvent(e));
      card.querySelector('.btn-secondary').addEventListener('click', () => { switchView('chat'); sendChat('Tell me about: ' + e.title); });
      el.appendChild(card);
    });
  }

  function renderJobsPage(feed) {
    const el = $('#jobs-grid');
    el.innerHTML = '';
    (feed.internal_jobs || []).forEach((j) => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML =
        '<h3>' + j.title + '</h3><div class="card-meta">' + j.team + ' · ' + j.location + '</div>' +
        '<p>' + j.type + ' · Posted ' + j.posted + '</p>' +
        '<div class="card-actions"><button type="button" class="btn btn-primary btn-sm">View & apply</button>' +
        '<button type="button" class="btn btn-secondary btn-sm">Ask about role</button></div>';
      card.querySelector('.btn-primary').addEventListener('click', () => showJob(j));
      card.querySelector('.btn-secondary').addEventListener('click', () => { switchView('chat'); sendChat('Tell me about internal job: ' + j.title); });
      el.appendChild(card);
    });
  }

  function renderKnowledgePage(srcList) {
    const el = $('#knowledge-grid');
    el.innerHTML = '';
    const samples = {
      hr: 'How much PTO do I get?',
      confluence: 'Production deployment runbook',
      finance: 'Budget approval limits',
      expense: 'Travel expense limits',
      education: 'Tuition reimbursement',
      onboarding: 'New hire day 1 checklist',
      tax: 'US W-4 withholding and year-end W-2',
      benefits: '401k company match and health enrollment',
      it: 'MFA and password reset policy',
    };
    srcList.forEach((s) => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = '<h3>' + s.label + '</h3><div class="card-meta">' + s.count + ' documents</div><p>Search this source via BestFrAIend.</p>' +
        '<div class="card-actions"><button type="button" class="btn btn-primary btn-sm">Search policies</button></div>';
      card.querySelector('.btn-primary').addEventListener('click', () => { switchView('chat'); sendChat(samples[s.category] || 'help'); });
      el.appendChild(card);
    });
  }

  function showEvent(e) {
    openModal(e.title, '<p><strong>When:</strong> ' + e.when + '</p><p><strong>Where:</strong> ' + e.where + '</p><p>' + e.description + '</p>', [
      { label: 'Add to calendar', class: 'btn-primary', onClick: () => toast('Calendar invite sent (demo)') },
      { label: 'Close', class: 'btn-secondary', close: true },
    ]);
  }

  function showNews(n) {
    openModal(n.headline, '<p><span class="tag">' + n.tag + '</span> · ' + n.published + '</p><p>' + n.summary + '</p>', [
      { label: 'Read article', class: 'btn-primary', onClick: () => toast('Opening intranet (demo)') },
      { label: 'Close', class: 'btn-secondary', close: true },
    ]);
  }

  function showStream(s) {
    openModal(s.title, '<p><strong>Status:</strong> ' + s.status + '</p><p>' + s.when + '</p><p>' + s.channel + '</p>', [
      { label: s.status === 'live' ? 'Join stream' : 'Remind me', class: 'btn-primary', onClick: () => toast('Stream opened (demo)') },
      { label: 'Close', class: 'btn-secondary', close: true },
    ]);
  }

  function showAiNews(n) {
    const CAT_LABELS = { model: 'New Model', product: 'Product', research: 'Research', industry: 'Industry' };
    openModal(
      n.title,
      '<p><span class="tag ai">' + (CAT_LABELS[n.category] || n.category) + '</span> &nbsp;<strong>' + n.company + '</strong> &nbsp;<small>· ' + n.published + '</small></p>' +
      '<p style="margin-top:0.75rem;line-height:1.65;">' + n.summary + '</p>',
      [
        { label: 'Ask BestFrAIend', class: 'btn-primary', onClick: () => { switchView('chat'); sendChat('Tell me about: ' + n.title); } },
        { label: 'Close', class: 'btn-secondary', close: true },
      ]
    );
  }

  function showJob(j) {
    openModal(j.title, '<p><strong>Team:</strong> ' + j.team + '</p><p><strong>Location:</strong> ' + j.location + '</p><p>Apply via Workday Internal Jobs.</p>', [
      { label: 'Apply internally', class: 'btn-primary', onClick: () => toast('Opening Workday (demo)') },
      { label: 'Close', class: 'btn-secondary', close: true },
    ]);
  }

  async function loadData() {
    try {
      const health = await fetch('/health');
      if (!health.ok) throw new Error('no health');
      const [feedRes, srcRes] = await Promise.all([fetch(API.feed), fetch(API.sources)]);
      orgFeed = await feedRes.json();
      sources = (await srcRes.json()).sources || [];
      serverOk = true;
    } catch {
      serverOk = false;
      orgFeed = { ongoing_events: [], upcoming_events: [], news: [], streams: [], internal_jobs: [] };
      sources = [];
    }
    renderWidgets(orgFeed);
    renderEventsPage(orgFeed);
    renderJobsPage(orgFeed);
    renderNewsPage(orgFeed);
    renderKnowledgePage(sources);
    if (serverOk) {
      await Promise.all([
        loadPolicySection('onboarding', '#onboarding-grid'),
        loadPolicySection('tax', '#tax-grid'),
        loadPolicySection('benefits', '#benefits-grid'),
        fetch('/api/faqs').then(r => r.json()).then(renderFaqPanel).catch(() => renderFaqPanel(null)),
      ]);
    } else {
      renderFaqPanel(null);
    }
  }

  function bindUi() {
    $$('.nav-btn[data-view]').forEach((btn) => btn.addEventListener('click', () => switchView(btn.dataset.view)));
    $('#chat-send').addEventListener('click', () => sendChat($('#chat-input').value));
    $('#chat-input').addEventListener('keydown', (e) => { if (e.key === 'Enter') sendChat($('#chat-input').value); });
    $('#btn-ask-pto').addEventListener('click', () => { switchView('chat'); sendChat('How much PTO do I get?'); });
    $('#btn-open-jobs').addEventListener('click', () => switchView('jobs'));
    $('#btn-open-events').addEventListener('click', () => switchView('events'));
    $('#header-search').addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && e.target.value.trim()) {
        switchView('chat');
        sendChat(e.target.value);
        e.target.value = '';
      }
    });
    $$('.chip-btn').forEach((chip) => chip.addEventListener('click', () => { switchView('chat'); sendChat(chip.dataset.q); }));
    $('#modal-close').addEventListener('click', closeModal);
    $('#modal-backdrop').addEventListener('click', (e) => { if (e.target.id === 'modal-backdrop') closeModal(); });
    $('#btn-notifications').addEventListener('click', () => toast('3 updates: All-hands live · 2 jobs · Benefits enrollment'));
  }

  async function init() {
    bindUi();
    await loadData();
    if (!serverOk && location.protocol === 'file:') $('#file-warning').hidden = false;
    addBubble('Welcome to **BestFrAIend** on the employee portal. Use the left menu, header buttons, or type a question below.', false);
    $('#chat-input').focus();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
