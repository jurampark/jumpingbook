var alertDiv;

$(function () {
    $(".input-rating").rating();
    $('.input-rating').rating('refresh', {showClear: false});
    alertDiv = $("#rating-success-alert-container");

    $('.input-rating').on('rating.change', function (event, value, caption) {
        $.ajax({
            type: 'POST',
            url: urlForBookRating,
            data: {
                "item-id": $(this).attr('item-id'),
                "rating": value
            },
            success: function (data, textStatus, jqXHR) {
                if (typeof alertDiv != 'undefined') {
                    alertDiv.show();
                    setTimeout(function () {
                        alertDiv.hide();
                    }, 2000);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert('Fail!');
            }
        });
    });
});