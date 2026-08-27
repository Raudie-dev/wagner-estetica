/* ========================================
   NAVEGACIÓN Y MENÚ RESPONSIVO
   ======================================== */

class Navigation {
    constructor() {
        this.hamburger = document.querySelector('#hamburger');
        this.navMenu = document.querySelector('#navMenu');
        this.navLinks = document.querySelectorAll('.nav-link');
        this.dropdownItems = document.querySelectorAll('.nav-item-dropdown');
        this.init();
    }

    init() {
        // Toggle menú hamburguesa
        this.hamburger.addEventListener('click', () => this.toggleMenu());

        // Cerrar menú al hacer clic en un enlace
        this.navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    this.closeMenu();
                }
                this.setActiveLink(link);
            });
        });

        // Dropdown para mobile
        this.dropdownItems.forEach(item => {
            const link = item.querySelector('.nav-link');
            link.addEventListener('click', (e) => {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    item.classList.toggle('active');
                }
            });
        });

        // Cerrar menú al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.header')) {
                this.closeMenu();
            }
        });

        // Establecer enlace activo en página actual
        this.setCurrentPageActive();

        console.log('[v0] Navegación inicializada');
    }

    toggleMenu() {
        this.hamburger.classList.toggle('active');
        this.navMenu.classList.toggle('active');
        console.log('[v0] Menú toggle: ' + (this.navMenu.classList.contains('active') ? 'abierto' : 'cerrado'));
    }

    closeMenu() {
        this.hamburger.classList.remove('active');
        this.navMenu.classList.remove('active');
        this.dropdownItems.forEach(item => item.classList.remove('active'));
    }

    setActiveLink(link) {
        this.navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    }

    setCurrentPageActive() {
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        this.navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPage || (currentPage === '' && href === 'index.html')) {
                link.classList.add('active');
            }
        });
    }
}

// Validación de formularios en tiempo real
class FormValidator {
    constructor() {
        this.forms = document.querySelectorAll('form');
        this.init();
    }

    init() {
        this.forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validate(form)) {
                    e.preventDefault();
                    console.log('[v0] Formulario inválido');
                }
            });

            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', () => {
                    this.validateField(input);
                });

                input.addEventListener('input', () => {
                    this.validateField(input, true);
                });
            });
        });
    }

    validate(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    validateField(input, isRealTime = false) {
        const value = input.value.trim();
        const type = input.type;
        const name = input.name;
        let isValid = true;
        let errorMessage = '';

        const formGroup = input.closest('.form-group');

        // Validaciones
        if (value === '') {
            isValid = false;
            errorMessage = 'Este campo es requerido';
        } else if (type === 'email' && !this.isValidEmail(value)) {
            isValid = false;
            errorMessage = 'Email inválido';
        } else if (name === 'license-id' && !this.isValidLicense(value)) {
            isValid = false;
            errorMessage = 'ID de licencia inválido';
        } else if (name === 'rif' && !this.isValidRIF(value)) {
            isValid = false;
            errorMessage = 'RIF inválido';
        } else if (name === 'message' && value.length < 10) {
            isValid = false;
            errorMessage = 'Mínimo 10 caracteres';
        }

        // Mostrar retroalimentación
        if (isRealTime && isValid) {
            this.showSuccess(formGroup, input);
        } else if (!isValid) {
            this.showError(formGroup, input, errorMessage);
        }

        return isValid;
    }

    showSuccess(formGroup, input) {
        formGroup.classList.remove('error');
        formGroup.classList.add('success');

        let feedback = formGroup.querySelector('.form-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'form-feedback success show';
            feedback.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg> <span>Válido</span>';
            formGroup.appendChild(feedback);
        } else {
            feedback.className = 'form-feedback success show';
            feedback.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg> <span>Válido</span>';
        }
    }

    showError(formGroup, input, message) {
        formGroup.classList.remove('success');
        formGroup.classList.add('error');

        let feedback = formGroup.querySelector('.form-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'form-feedback error show';
            feedback.innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/></svg> <span>${message}</span>`;
            formGroup.appendChild(feedback);
        } else {
            feedback.className = 'form-feedback error show';
            feedback.innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/></svg> <span>${message}</span>`;
        }
    }

    isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    isValidLicense(license) {
        return license.length >= 5;
    }

    isValidRIF(rif) {
        return rif.match(/^[VEJGP]-\d{7,8}-\d$/) || rif.length >= 6;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new Navigation();
    new FormValidator();
});

document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav-link');

    if (hamburger) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    document.addEventListener('click', function(event) {
        if (!event.target.closest('.header')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }
    });
});
