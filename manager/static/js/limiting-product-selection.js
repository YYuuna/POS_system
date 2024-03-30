// Function to limit the select options
function limitSelects() {
    const select = $(this);
    const selectedValue = select.val();

    // Enable all options
    select.find('option').prop("disabled", false);

    // Get all selected values
    const selectedValues = $(".product-select").map(function() {
        return $(this).val();
    }).get();

    // Disable options that are selected in other select fields
    selectedValues.forEach(function(value) {
        if (value !== selectedValue && value !== "") {
            select.find(`option[value=${value}]`).prop("disabled", true);
        }
    });

    // Re-enable options that are not selected in any select field
    select.find('option').each(function() {
        const option = $(this);
        if (!selectedValues.includes(option.val())) {
            option.prop("disabled", false);
        }
    });

}

// Function to handle the change event
function handleChange() {
    // Loop through all select fields
    $(".product-select").each(limitSelects);
}

$(document).ready(function() {
    // Attach event listener to the document, targeting dynamically added .product-select elements
    $(document).on('change', '.product-select', handleChange);

    // Create a MutationObserver instance to watch for changes in the DOM
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                handleChange();
            }
        });
    });

    // Start observing the document with the configured parameters
    observer.observe(document.body, { childList: true, subtree: true });

    // Call handleChange for initially populated forms
    handleChange();
});