$(document).ready(function() {
    // Attach event listener to the document, targeting dynamically added .product-select elements
    $(document).on('change', '.product-select', function() {
        var selectedProductPk = $(this).val();
        var purchasePriceInput = $(this).closest('.purchase-order-item').find('.purchase-price-input');

        if (selectedProductPk) {
            $.ajax({
                url: '/produit/' + selectedProductPk + '/prix_achat_initial/',
                success: function(data) {
                    purchasePriceInput.val(data.initial_buying_price);
                },
                error: function() {
                    alert('Produit non trouvé');
                    purchasePriceInput.val('0');
                }
            });
        } else {
            purchasePriceInput.val('');
        }
    });
});