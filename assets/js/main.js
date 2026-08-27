/* ========================================
   LOGINTEL - SCRIPT PRINCIPAL
   ======================================== */

document.addEventListener('DOMContentLoaded', () => {
    console.log('[v0] Inicializando aplicación Logintel');
    
    // Scroll suave
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
});
