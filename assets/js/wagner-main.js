document.addEventListener('DOMContentLoaded', () => {
    // Navbar Scroll Effect
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile Menu Toggle
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            
            // Toggle hamburger animation
            const spans = menuToggle.querySelectorAll('span');
            if(navLinks.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -8px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
        
        // Cerrar menú al hacer clic en un link en móvil
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                const spans = menuToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });
    }

    // Intersection Observer for scroll animations (Bento items)
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
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animateElements = document.querySelectorAll('.service-circle-card, .feature-item, .team-member, .coverage-content-wrapper, .contact-layout');
    animateElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = `all 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.1}s`;
        observer.observe(el);
    });
});

// Modal Logic
function openBookingModal() {
    document.getElementById('bookingModal').classList.add('active');
}

function closeBookingModal() {
    document.getElementById('bookingModal').classList.remove('active');
}

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    const modal = document.getElementById('bookingModal');
    if (e.target === modal) {
        closeBookingModal();
    }
});

// Handle form submission to WhatsApp
function handleBookingSubmit(e) {
    e.preventDefault();
    
    const name = document.getElementById('b-name').value;
    const service = document.getElementById('b-service').value;
    const date = document.getElementById('b-date').value;
    const time = document.getElementById('b-time').value;
    
    // Format Date from YYYY-MM-DD to DD/MM/YYYY
    const dateParts = date.split('-');
    const formattedDate = `${dateParts[2]}/${dateParts[1]}/${dateParts[0]}`;
    
    // Build message
    const message = `Hola Enjoy Dental, mi nombre es *${name}*.\n\nQuisiera solicitar un turno para *${service}*.\n🗓️ Fecha: ${formattedDate}\n⏰ Horario: ${time}\n\n¿Tienen disponibilidad?`;
    
    const encodedMessage = encodeURIComponent(message);
    const whatsappNumber = "5491130400061"; // Number without + or spaces
    
    const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodedMessage}`;
    
    window.open(whatsappUrl, '_blank');
    closeBookingModal();
    
    // Optional: reset form
    document.getElementById('bookingForm').reset();
}

// Auto-scroll logic for team carousel on mobile
document.addEventListener('DOMContentLoaded', () => {
    const teamGrid = document.querySelector('.team-grid');
    if (teamGrid) {
        let isDown = false;
        
        teamGrid.addEventListener('mousedown', () => isDown = true);
        teamGrid.addEventListener('mouseleave', () => isDown = false);
        teamGrid.addEventListener('mouseup', () => isDown = false);
        teamGrid.addEventListener('touchstart', () => isDown = true, {passive: true});
        teamGrid.addEventListener('touchend', () => isDown = false, {passive: true});

        setInterval(() => {
            if (window.innerWidth <= 768 && !isDown) {
                const maxScroll = teamGrid.scrollWidth - teamGrid.clientWidth;
                // If reached the end, loop back to start
                if (teamGrid.scrollLeft >= maxScroll - 10) {
                    teamGrid.scrollTo({ left: 0, behavior: 'smooth' });
                } else {
                    // Scroll by roughly the width of one card
                    teamGrid.scrollBy({ left: 320, behavior: 'smooth' });
                }
            }
        }, 3000);
    }
});
