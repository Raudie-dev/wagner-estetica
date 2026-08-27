/* ========================================
   SLIDER DINÁMICO
   ======================================== */

class HeroSlider {
    constructor() {
        this.slider = document.querySelector('.hero-slider');
        this.items = document.querySelectorAll('.slider-item');
        this.dots = document.querySelectorAll('.slider-dot');
        this.currentIndex = 0;
        this.autoPlayInterval = null;
        
        if (this.items.length > 0) {
            this.init();
        }
    }

    init() {
        // Event listeners para los dots
        this.dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                this.goToSlide(index);
                this.resetAutoPlay();
            });
        });

        // Autoplay
        this.startAutoPlay();

        // Pausa al pasar el mouse
        this.slider.addEventListener('mouseenter', () => this.stopAutoPlay());
        this.slider.addEventListener('mouseleave', () => this.startAutoPlay());

        console.log('[v0] Slider iniciado con ' + this.items.length + ' slides');
    }

    goToSlide(index) {
        // Remover clase active
        this.items[this.currentIndex].classList.remove('active');
        this.dots[this.currentIndex].classList.remove('active');

        // Actualizar índice
        this.currentIndex = (index + this.items.length) % this.items.length;

        // Agregar clase active
        this.items[this.currentIndex].classList.add('active');
        this.dots[this.currentIndex].classList.add('active');
    }

    nextSlide() {
        this.goToSlide(this.currentIndex + 1);
    }

    startAutoPlay() {
        this.autoPlayInterval = setInterval(() => this.nextSlide(), 6000);
    }

    stopAutoPlay() {
        clearInterval(this.autoPlayInterval);
    }

    resetAutoPlay() {
        this.stopAutoPlay();
        this.startAutoPlay();
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new HeroSlider();
});
