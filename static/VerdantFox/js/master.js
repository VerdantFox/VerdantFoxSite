

$('#quote-form').submit(function(ev) {
    $('#quote-submit').html('<i class="fas fa-spinner fa-spin"></i> Getting quote...');
    $('#quote-submit').attr('disabled', true)
});

$('#buy-form').submit(function(ev) {
    $('#buy-submit').html('<i class="fas fa-spinner fa-spin"></i> Buying...');
    $('#buy-submit').attr('disabled', true)
});

$('#funds-form').submit(function(ev) {
    $('#add-funds-button').html('<i class="fas fa-spinner fa-spin"></i> Adding Funds');
    $('#add-funds-button').attr('disabled', true)
});
