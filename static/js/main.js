// Scripts customizados para o Sistema de Gestão de Estoque

$(document).ready(function() {
    // Auto-hide alerts após 5 segundos
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Confirmação antes de excluir
    $('.btn-delete').on('click', function(e) {
        if (!confirm('Tem certeza que deseja excluir este item?')) {
            e.preventDefault();
        }
    });
    
    // Adicionar classe active ao item do menu atual
    var currentPath = window.location.pathname;
    $('.navbar-nav .nav-link').each(function() {
        var href = $(this).attr('href');
        if (currentPath.indexOf(href) !== -1 && href !== '/') {
            $(this).addClass('active');
        }
    });
    
    // Formatar campos de valor monetário
    $('input[type="number"][step="0.01"]').on('blur', function() {
        var value = parseFloat($(this).val());
        if (!isNaN(value)) {
            $(this).val(value.toFixed(2));
        }
    });
    
    // Tooltip Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Validação de formulários
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Função para confirmar exclusão (usada nos templates)
function confirmarExclusao(id, nome) {
    if (confirm('Tem certeza que deseja excluir "' + nome + '"? Esta ação não pode ser desfeita.')) {
        document.getElementById('form-excluir-' + id).submit();
    }
}

// Função para atualizar estoque em tempo real (pode ser expandida com AJAX)
function atualizarEstoque(produtoId) {
    // Implementação futura com AJAX
    console.log('Atualizando estoque do produto: ' + produtoId);
}
