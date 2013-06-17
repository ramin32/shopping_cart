$(function () {
    $('.add-to-cart').click(function () {
        $.post($(this).attr('href'), function (data) {
            if (data.new_total) {
                $('#cart-total').html(data.new_total);
            }
            var flash = $('<div class="flash hidden">Item added to cart!</div>');
            $('header').after(flash);
            flash.slideDown(function () {
                setTimeout(function () {
                    flash.slideUp();
                }, 2000);
            });

        });
        return false;
    });

    $('#checkout-form-toggle').click(function () {
        $('#checkout-form').slideToggle();
    });
});
