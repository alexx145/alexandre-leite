document.addEventListener("DOMContentLoaded", () => {
    // 1. Atualizar o ano no rodapé automaticamente
    const yearSpan = document.getElementById("year");
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // 2. Animação simples de fade-in nos elementos ao rolar a página
    // O Intersection Observer traz uma sensação de movimento suave e premium
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target); // Para animar apenas 1 vez
            }
        });
    }, observerOptions);

    // Selecionamos as que queremos animar
    const elementsToAnimate = document.querySelectorAll('section, .project-card, .skill-tag');
    elementsToAnimate.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.7s ease-out, transform 0.7s ease-out';
        observer.observe(el);
    });
});

// Envio de Form para WhatsApp
window.sendWhatsApp = function(e) {
    e.preventDefault();
    const name = document.getElementById('waName').value;
    const phone = document.getElementById('waPhone').value;
    const email = document.getElementById('waEmail').value;
    const reason = document.getElementById('waReason').value;
    
    const text = `Olá! Meu nome é ${name}.\nTelefone: ${phone}\nE-mail: ${email}\nMotivo do contato: ${reason}`;
    const encodedText = encodeURIComponent(text);
    
    // Abre a janela do WhatsApp via redirect Web
    window.open(`https://wa.me/message/QADTUQVEGRIUJ1?text=${encodedText}`, '_blank');
};

// Clipboard Email e Toast Alert (Substitui Alerta Nativo)
window.copyEmail = function(e) {
    navigator.clipboard.writeText("alexandreaugusto145@gmail.com").catch(err => console.log('Clipboard access denied', err));
    
    const toast = document.getElementById('emailToast');
    if(toast) {
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 4000);
    }
};
