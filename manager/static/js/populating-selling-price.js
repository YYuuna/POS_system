$(document).ready(function() {
    // Attach event listener to the document, targeting dynamically added .product-select elements
    $(document).on('change', '.product-select', function() {
        var selectedProductPk = $(this).val();
        var initialSellingPriceInput = $(this).closest('.sale-item').find('.sale-price-input');

        if (selectedProductPk) {
            $.ajax({
                url: '/produit/' + selectedProductPk + '/prix_vente_initial/',
                success: function(data) {
                    initialSellingPriceInput.val(data.initial_selling_price);
                },
                error: function() {
                    alert('Produit non trouvé');
                    initialSellingPriceInput.val('0');
                }
            });
        } else {
            initialSellingPriceInput.val('');
        }
    });
});