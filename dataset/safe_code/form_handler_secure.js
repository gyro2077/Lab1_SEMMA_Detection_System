/**
 * Ejemplo de código seguro - Manejo de formularios en JavaScript
 */

class SecureFormHandler {
    constructor(formId) {
        this.form = document.getElementById(formId);
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });
    }

    sanitizeInput(input) {
        // Crear un elemento temporal para escapar HTML
        const temp = document.createElement('div');
        temp.textContent = input;
        return temp.innerHTML;
    }

    validateEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    handleSubmit() {
        const name = this.form.querySelector('#name').value;
        const email = this.form.querySelector('#email').value;

        // Validar entrada
        if (!name || name.length < 2) {
            alert('Nombre inválido');
            return;
        }

        if (!this.validateEmail(email)) {
            alert('Email inválido');
            return;
        }

        // Sanitizar antes de usar
        const safeName = this.sanitizeInput(name);
        const safeEmail = this.sanitizeInput(email);

        // Usar textContent en lugar de innerHTML
        document.getElementById('result').textContent =
            `Nombre: ${safeName}, Email: ${safeEmail}`;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new SecureFormHandler('userForm');
});
