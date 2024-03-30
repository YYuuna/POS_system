$(document).ready(function() {
    // Attach event listener to the document, targeting dynamically added .product-select elements
    $(document).on('change', '.product-select', function() {
        const select = $(this);
        const productId = select.val();

        // Make an AJAX request to fetch the initial selling price of the product
        $.ajax({
            url: '/get_initial_selling_price/',  // Update with the actual URL of your new view
            data: {
                'product_id': productId
            },
            success: function(data) {
                // Update the 'sale_price' field in the form
                select.closest('.sale-item').find('.sale-price-input').val(data.initial_selling_price);
            }
        });
    });
});