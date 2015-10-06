function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var loadingDiv;
var alertDiv;

$(document).ready(function () {

    loadingDiv = $("#loadingDiv");
    alertDiv = $("#rating-success-alert-container");

    loadingDiv.hide();


    $(".star-rating-container").fadeTo(0, 0);
    $(".book-item").mouseover(function(){
      //var current_item =
        $(this).find('div.star-rating-container').fadeTo(0, 0.8);
    }).mouseout(function(){
        $(this).find('div.star-rating-container').fadeTo(0, 0);
    });

    $('input.rating').rating();
    $('input.rating').on('change', function () {
        var current_item = $(this).parent().parent().parent().parent();
        $.ajax({
            type: 'POST',
            url: urlForBookRating,
            data: {
                "item-id": current_item.attr('item-id'),
                "rating": $(this).val()
            },
            success: function () {
              alertDiv.show();
              setTimeout(function() {
                  alertDiv.hide();
              }, 2000);
                current_item.fadeTo(400, 0.5);
            },
            error: function (xhr, type, exception) {
                alert("ajax error response type " + type);
            },
            beforeSend: function () {
                loadingDiv.show();
            },
            complete: function () {
                loadingDiv.hide();
            }
        });
    });
});
