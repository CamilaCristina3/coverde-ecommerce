document.addEventListener('DOMContentLoaded', function() {
    // Adicionar ao carrinho
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const button = this;
            
            // Feedback visual
            const originalText = button.innerHTML;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Adicionando...';
            button.disabled = true;
            
            // Requisição AJAX
            fetch("{% url 'ecommerce_coverde:add_to_cart' 0 %}".replace('0', productId), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: `quantity=1`
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    // Feedback de sucesso
                    button.innerHTML = '<i class="fas fa-check me-2"></i>Adicionado!';
                    
                    // Atualizar contador do carrinho
                    const counter = document.getElementById('cart-counter');
                    if(counter) {
                        counter.textContent = data.total_items;
                        counter.classList.remove('d-none');
                    }
                    
                    // Redirecionar após 1.5 segundos
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 1500);
                } else {
                    throw new Error(data.error || 'Erro desconhecido');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                button.innerHTML = originalText;
                button.disabled = false;
                alert('Erro ao adicionar ao carrinho: ' + error.message);
            });
        });
    });

    // Limpar carrinho (existente)
    const clearCartBtn = document.getElementById('clear-cart-btn');
    if (clearCartBtn) {
        clearCartBtn.addEventListener('click', function(e) {
            if(!confirm('Tem certeza que deseja limpar todo o carrinho?')) {
                e.preventDefault();
            }
        });
    }
});