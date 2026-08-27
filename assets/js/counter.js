/* ========================================
   CONTADOR ANIMADO
   ======================================== */

class AnimatedCounter {
    constructor() {
        this.statsSection = document.querySelector('.stats-section');
        this.statNumbers = document.querySelectorAll('.stat-number');
        this.hasAnimated = false;
    }

    init() {
        if (!this.statsSection) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !this.hasAnimated) {
                    this.animateCounters();
                    this.hasAnimated = true;
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(this.statsSection);
    }

    animateCounters() {
        this.statNumbers.forEach(element => {
            const target = parseInt(element.dataset.target);
            const duration = 2000; // 2 segundos
            const steps = 60;
            const stepValue = target / steps;
            let current = 0;
            let step = 0;

            const interval = setInterval(() => {
                step++;
                current += stepValue;

                if (step >= steps) {
                    element.textContent = this.formatNumber(target);
                    clearInterval(interval);
                } else {
                    element.textContent = this.formatNumber(Math.floor(current));
                }
            }, duration / steps);
        });

        console.log('[v0] Contadores animados iniciados');
    }

    formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(0) + 'M+';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(0) + 'K+';
        }
        return num.toLocaleString('es-VE');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const counter = new AnimatedCounter();
    counter.init();
});
