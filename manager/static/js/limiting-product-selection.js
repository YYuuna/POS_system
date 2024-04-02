function updateProductSelection() {
    // Enable all options
    $('.product-select option').prop('disabled', false);

    // For each visible product select element
    $('.product-select:visible').each(function() {
        var select = $(this);
        var selectedOption = select.find('option:selected');

        // If a product is selected
        if (selectedOption.val()) {
            // Disable this option in all other visible select elements
            $('.product-select:visible').not(select).find('option[value="' + selectedOption.val() + '"]').prop('disabled', true);
        }
    });
}

$(document).ready(function() {
    // Attach event listener to the document, targeting dynamically added .product-select elements
    $(document).on('change', '.product-select', function() {
        // Your existing code...

        // Update product selection
        updateProductSelection();
    });
    // Call updateProductSelection on page load
    updateProductSelection();
});