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

function refreshList() {
    var category_id = $('.category-list-item.active').attr('category-id');

    $.ajax({
        type: 'POST',
        url: urlForBookList,
        data: {'category-id': category_id},
        success: function (data) {
            $('input.rating').off();
            $('.book-item-container').empty();

            for (var index in data) {
                var item = data[index];
                var elem = "    <div class=\"book-item\" item-id=\"" + item['id'] + "\"> \
                                <div class=\"img-container\"> \
                                <img src=\"" + item['image_url'] + "\" /> \
                                </div> \
                                <div class=\"star-rating-container\"> \
                                  <div class=\"item-title\">" + item['name'] + "</div> \
                                  <div class=\"item-author\">" + item['author'] + "</div> \
                                  <input type=\"hidden\" class=\"rating\" data-fractions=\"2\"/> \
                                </div> \
                                </div>";
                $('.book-item-container').append(elem);
            }
            $('input.rating').rating();
            $('input.rating').on('change', function () {
                var current_item = $(this).parent().parent();
                $.ajax({
                    type: 'POST',
                    url: urlForBookRating,
                    data: {
                        "item-id": $(this).parent().parent().attr('item-id'),
                        "rating": $(this).val()
                    },
                    success: function () {
                        alertDiv.show();
                        setTimeout(function() {
                            alertDiv.hide();
                        }, 2000);
                        current_item.remove();
                    },
                    error: function (xhr, type, exception) {
                        alert("ajax error response type2 " + type);
                    },
                    beforeSend: function () {
                        loadingDiv.show();
                    },
                    complete: function () {
                        loadingDiv.hide();
                    }
                })
            })
        },
        error: function (xhr, type, exception) {
            alert("ajax communication error" + type);
        },
        beforeSend: function () {
            loadingDiv.show();
        },
        complete: function () {
            loadingDiv.hide();
        }
    });
}


$(document).ready(function () {

    loadingDiv = $("#loadingDiv");
    alertDiv = $("#alert-container");

    loadingDiv.hide();

    $('.category-list-item').click(function(e) {
        e.preventDefault();
        $('.category-list-item.active').removeClass('active');
        $(this).addClass('active');
        refreshList();
    });

    refreshList();
});
