document.addEventListener('DOMContentLoaded', function() {
    const iconeInput = document.getElementById('id_icone');
    if (iconeInput) {
        iconeInput.placeholder = 'fa-leaf, fa-apple-alt, etc';
        iconeInput.addEventListener('focus', function() {
            this.placeholder = 'Digite o nome do ícone Font Awesome';
        });
        iconeInput.addEventListener('blur', function() {
            this.placeholder = 'fa-leaf, fa-apple-alt, etc';
        });
    }
});