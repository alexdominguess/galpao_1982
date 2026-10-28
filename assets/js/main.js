/* =========================================================
   ✏️ CONFIGURAÇÃO — editar antes da publicação definitiva
   ========================================================= */
const CONFIG = {
  // Número do WhatsApp com DDI + DDD, apenas dígitos (ex.: 5519999999999).
  // Enquanto não for confirmado, usa o telefone divulgado (19) 3363-1012.
  whatsapp: '551933631012',

  // Busca usada nos botões "Como chegar" / "Abrir no Google Maps".
  maps: 'Galpão 1982, Av. José Paulino, 3802, Paulínia - SP',
};

/* ---------- Links de WhatsApp e Google Maps ---------- */
document.querySelectorAll('[data-wa]').forEach((a) => {
  const text = a.dataset.wa ? `?text=${encodeURIComponent(a.dataset.wa)}` : '';
  a.href = `https://wa.me/${CONFIG.whatsapp}${text}`;
});
document.querySelectorAll('[data-maps]').forEach((a) => {
  a.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(CONFIG.maps)}`;
});

/* ---------- Header: sólido ao rolar + botão WhatsApp flutuante ---------- */
const header = document.querySelector('.header');
const waFloat = document.querySelector('.wa-float');
const onScroll = () => {
  const y = window.scrollY;
  header.classList.toggle('is-scrolled', y > 40);
  waFloat.classList.toggle('is-visible', y > window.innerHeight * 0.5);
};
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

/* ---------- Menu mobile ---------- */
const toggle = document.querySelector('.menu-toggle');
const setMenu = (open) => {
  document.body.classList.toggle('menu-open', open);
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
};
toggle.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open')));
document.querySelectorAll('.nav a').forEach((a) => a.addEventListener('click', () => setMenu(false)));
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

/* ---------- Fade-in ao rolar ---------- */
const revealIO = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-in');
      revealIO.unobserve(entry.target);
    }
  });
}, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((el) => revealIO.observe(el));

/* ---------- Link ativo no menu ---------- */
const links = new Map([...document.querySelectorAll('.nav__link')].map((a) => [a.hash.slice(1), a]));
const navIO = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    links.forEach((a) => a.classList.remove('is-active'));
    links.get(entry.target.id)?.classList.add('is-active');
  });
}, { rootMargin: '-45% 0px -50% 0px' });
links.forEach((_, id) => { const s = document.getElementById(id); if (s) navIO.observe(s); });

/* ---------- Parallax suave na seção Churrasco (desktop) ---------- */
const fire = document.querySelector('.fire');
const fireImg = document.querySelector('.fire__media img');
const motionOK = window.matchMedia('(min-width: 900px) and (prefers-reduced-motion: no-preference)');
if (fire && fireImg) {
  let ticking = false;
  const parallax = () => {
    ticking = false;
    if (!motionOK.matches) { fireImg.style.transform = ''; return; }
    const r = fire.getBoundingClientRect();
    if (r.bottom < 0 || r.top > window.innerHeight) return;
    const progress = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
    fireImg.style.transform = `translate3d(0, ${(progress * 9).toFixed(2)}%, 0)`;
  };
  window.addEventListener('scroll', () => {
    if (!ticking) { ticking = true; requestAnimationFrame(parallax); }
  }, { passive: true });
  parallax();
}
