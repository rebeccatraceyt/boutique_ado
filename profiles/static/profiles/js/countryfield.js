// Assigns country field to varaible
let countrySelected = $('#id_default_country').val();

// Checks whether it is the country that has been selected
if(!countrySelected) {
    // If country selected is false, add css to placeholder
    $('#id_default_country').css('color', '#aab7c4');
};

// capture change event
$('#id_default_country').change(function() {
    // every time the box changes, get the value of it
    countrySelected = $(this).val();
    
    // determine the proper colour
    if(!countrySelected) {
        $(this).css('color', '#aab7c4');
    } else {
        $(this).css('color', '#000');
    }
});