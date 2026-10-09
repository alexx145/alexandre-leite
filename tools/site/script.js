document.documentElement.classList.add('js');

document.addEventListener('DOMContentLoaded', () => {
    // 1. Ano do rodapé
    const yearSpan = document.getElementById('year');
    if (yearSpan) yearSpan.textContent = new Date().getFullYear();

    // 2. Fade-in suave ao rolar (o conteúdo continua visível se o JS falhar)
    const revealEls = document.querySelectorAll('.reveal');
    const showAll = () => revealEls.forEach(el => el.classList.add('visible'));
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0, rootMargin: '0px 0px -5% 0px' });
        revealEls.forEach(el => observer.observe(el));
        setTimeout(showAll, 2500);
    } else {
        showAll();
    }

    // Botão flutuante de contato (celular): aparece depois do topo e some no rodapé
    const fab = document.getElementById('fab');
    const hero = document.getElementById('home');
    const footer = document.getElementById('contato');
    if (fab && hero && footer && 'IntersectionObserver' in window) {
        const seen = { hero: true, footer: false };
        const update = () => fab.classList.toggle('fab-hidden', seen.hero || seen.footer);
        new IntersectionObserver(es => { seen.hero = es[0].isIntersecting; update(); }).observe(hero);
        new IntersectionObserver(es => { seen.footer = es[0].isIntersecting; update(); }).observe(footer);
    }

    // 3. Filtro do jornalismo
    const filterButtons = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.journalism-card');
    const applyFilter = (value) => {
        cards.forEach(card => {
            const match = value === 'all' || card.getAttribute('data-category') === value;
            card.classList.toggle('hidden', !match);
        });
    };
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => {
                b.classList.remove('active');
                b.setAttribute('aria-pressed', 'false');
            });
            btn.classList.add('active');
            btn.setAttribute('aria-pressed', 'true');
            applyFilter(btn.getAttribute('data-filter'));
        });
    });
    const initial = document.querySelector('.filter-btn.active');
    if (initial) applyFilter(initial.getAttribute('data-filter'));
});

// Envio do formulário para o WhatsApp
window.sendWhatsApp = function (e) {
    e.preventDefault();
    const form = e.target;
    const name = document.getElementById('waName').value;
    const phone = document.getElementById('waPhone').value;
    const email = document.getElementById('waEmail').value;
    const reason = document.getElementById('waReason').value;
    const tpl = form.getAttribute('data-template') || 'Olá! Meu nome é {name}.\nTelefone: {phone}\nE-mail: {email}\nMotivo do contato: {reason}';
    const text = tpl.replace('{name}', name).replace('{phone}', phone).replace('{email}', email).replace('{reason}', reason);
    window.open('https://api.whatsapp.com/send?phone=5531982034543&text=' + encodeURIComponent(text), '_blank', 'noopener');
};

// Copia o e-mail e mostra o aviso
window.copyEmail = function () {
    if (navigator.clipboard) {
        navigator.clipboard.writeText('alexandreaugusto145@gmail.com').catch(() => {});
    }
    const toast = document.getElementById('emailToast');
    if (toast) {
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 4000);
    }
};
