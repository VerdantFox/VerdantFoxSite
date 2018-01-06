

$('#quote-form').submit(function(ev) {
    $('#quote-submit').html('<i class="fas fa-spinner fa-spin"></i> Getting quote...');
    $('#quote-submit').attr('disabled', true)
});

$('#buy-form').submit(function(ev) {
    $('#buy-submit').html('<i class="fas fa-spinner fa-spin"></i> Buying...');
    $('#buy-submit').attr('disabled', true)
});
