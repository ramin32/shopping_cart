$(function () {
    $('.add-to-cart').click(function () {
        $.post($(this).attr('href'), function (data) {
            if (data.new_total) {
                $('#cart-total').html(data.new_total);
            }
        });
        return false;
    });
});
