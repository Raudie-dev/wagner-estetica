/* ========================================
   SOLUCIONES CON FILTROS DINÁMICOS
   ======================================== */

const solutionsData = [
    {
        id: 1,
        category: 'hogar',
        title: 'ESET Home Windows',
        description: 'Protección completa para Windows con antivirus y anti-malware en tiempo real',
        features: ['Antivirus en tiempo real', 'Anti-spyware', 'Protección web', 'Soporte 24/7'],
        icon: 'desktop'
    },
    {
        id: 2,
        category: 'hogar',
        title: 'ESET Home Mac',
        description: 'Seguridad especializada para dispositivos macOS y OS X',
        features: ['Detección de malware', 'Protección en tiempo real', 'Compatible M1/M2', 'Soporte técnico'],
        icon: 'laptop'
    },
    {
        id: 3,
        category: 'hogar',
        title: 'ESET Home Android',
        description: 'Defensa contra amenazas en dispositivos Android y tablets',
        features: ['Protección de apps', 'Anti-phishing', 'Bloqueo de llamadas', 'Optimización'],
        icon: 'smartphone'
    },
    {
        id: 4,
        category: 'hogar',
        title: 'ESET Home Linux',
        description: 'Protección ligera y eficiente para sistemas Linux',
        features: ['Bajo consumo de recursos', 'Detección de amenazas', 'Escaneo rápido', 'Compatible'],
        icon: 'server'
    },
    {
        id: 5,
        category: 'empresa',
        title: 'Endpoint Protection',
        description: 'Solución empresarial de protección para estaciones de trabajo',
        features: ['Control centralizado', 'Detección avanzada', 'Reportes detallados', 'Escalabilidad'],
        icon: 'shield'
    },
    {
        id: 6,
        category: 'empresa',
        title: 'Seguridad Móvil Corporativa',
        description: 'Protección especializada para dispositivos móviles empresariales',
        features: ['MDM integrado', 'Control de apps', 'Cifrado de datos', 'Bloqueo remoto'],
        icon: 'lock'
    },
    {
        id: 7,
        category: 'empresa',
        title: 'Protección de Servidores',
        description: 'Defensa crítica para servidores y centros de datos',
        features: ['Monitoreo 24/7', 'Actualizaciones automáticas', 'Rendimiento optimizado', 'Escalable'],
        icon: 'database'
    },
    {
        id: 8,
        category: 'empresa',
        title: 'Cifrado de Datos',
        description: 'Protección de información sensible con cifrado empresarial',
        features: ['Cifrado AES-256', 'Control de USB', 'Protección de carpetas', 'Auditoría'],
        icon: 'key'
    },
    {
        id: 9,
        category: 'empresa',
        title: 'Doble Autenticación',
        description: 'Control de acceso avanzado con autenticación multifactor',
        features: ['2FA/MFA', 'Integración LDAP', 'Reportes de acceso', 'Biometría'],
        icon: 'fingerprint'
    }
];

const iconSVGs = {
    desktop: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><path d="M8 21h8M12 17v4"/></svg>',
    laptop: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 3H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-11 19h6M9 20h6"/></svg>',
    smartphone: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><path d="M12 18h.01"/></svg>',
    server: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="8"/><rect x="2" y="14" width="20" height="8"/><circle cx="6" cy="6" r="1"/><circle cx="6" cy="18" r="1"/></svg>',
    shield: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    lock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    database: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5c0 1.66 4 3 9 3s9-1.34 9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/></svg>',
    key: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="7.5" cy="15.5" r="5.5"/><path d="M21 2l-9.6 9.6M15.5 10l3.5-3.5"/></svg>',
    fingerprint: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 10c-1.657 0-3 1.343-3 3v7c0 1.657 1.343 3 3 3s3-1.343 3-3v-7c0-1.657-1.343-3-3-3zm0 0V4m0 0c-2.761 0-5 2.239-5 5v7c0 2.761 2.239 5 5 5s5-2.239 5-5v-7c0-2.761-2.239-5-5-5z"/></svg>'
};

class SolutionsFilter {
    constructor() {
        this.container = document.querySelector('#solutionsGrid');
        this.filterBtns = document.querySelectorAll('.filter-btn');
        this.currentFilter = 'all';
        this.init();
    }

    init() {
        this.renderSolutions('all');
        
        this.filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.filterBtns.forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentFilter = e.target.dataset.filter;
                this.renderSolutions(this.currentFilter);
                console.log('[v0] Filtro aplicado: ' + this.currentFilter);
            });
        });
    }

    renderSolutions(filter) {
        let filtered = solutionsData;

        if (filter !== 'all') {
            filtered = solutionsData.filter(sol => sol.category === filter);
        }

        this.container.innerHTML = '';

        filtered.forEach(solution => {
            const card = document.createElement('div');
            card.className = 'solution-card';
            
            const featuresList = solution.features
                .map(f => `<li>${f}</li>`)
                .join('');

            card.innerHTML = `
                <span class="solution-category">${solution.category === 'hogar' ? 'Hogar' : 'Empresa'}</span>
                <div class="solution-icon">
                    ${iconSVGs[solution.icon] || iconSVGs.shield}
                </div>
                <h3>${solution.title}</h3>
                <p>${solution.description}</p>
                <ul class="solution-features">
                    ${featuresList}
                </ul>
                <a href="#" class="btn-secondary">Más Información</a>
            `;

            this.container.appendChild(card);
        });

        console.log('[v0] Renderizadas ' + filtered.length + ' soluciones');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new SolutionsFilter();
});
