$(document).ready(function() {
    // Function to show or hide fields
    function showOrHideFields() {
        if ($('#id_state').val() == 'En réparation') {
            // Hide fields and set their values to null
            $('#id_initial_buying_price').hide().val(null);
            $('#id_initial_selling_price').hide().val(null);
            $('#id_supplier').hide().val(null).prev('label').hide();
        } else {
            // Show fields
            $('#id_initial_buying_price').show();
            $('#id_initial_selling_price').show();
            $('#id_supplier').show().prev('label').show();
        }
    }

    // Call showOrHideFields when the page loads
    showOrHideFields();

    // Call showOrHideFields whenever the selected state changes
    $('#id_state').change(showOrHideFields);
});