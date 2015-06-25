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
var categoryId;
var nextPage = -1;
var infinite;

function refreshWaypointsLibrary() {
    infinite = new Waypoint({
        element: $('.book-item-container')[0],
        handler: function (direction) {
            if (direction === 'down' && nextPage !== -1) {
                getItemList(nextPage);
            }
        },
        offset: 'bottom-in-view'
    });
}

function offRatingLibrary( selector ) {
    $(selector).off();
}
function onRatingLibrary( selector ) {
    $(selector).rating();
    $(selector).on('change', function () {
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
                setTimeout(function () {
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
        });
    });
}

function getItemList(page) {

    $.ajax({
        type: 'POST',
        url: urlForBookList,
        data: {
            'category-id': categoryId,
            'page': page
        },
        success: function (data) {

            offRatingLibrary('input.rating');

            if ( page == 1 ) {
                $('.book-item-container').empty();
            }

            nextPage = data['next_page_num'];

            for (var index in data['items']) {
                var item = data['items'][index];
                var elem = "    <div class=\"book-item\" item-id=\"" + item['id'] + "\"> \
                                <div class=\"img-container\"> \
                                <img src=\"" + item['image_url'] + "\" /> \
                                </div> \
                                <div class=\"star-rating-container\"> \
                                  <div class=\"item-title\">" + item['title'] + "</div> \
                                  <div class=\"item-author\">" + item['author'] + "</div> \
                                  <input type=\"hidden\" class=\"rating\" data-fractions=\"2\"/> \
                                </div> \
                                </div>";
                $('.book-item-container').append(elem);
            }

            Waypoint.refreshAll();

            onRatingLibrary('input.rating');

            $(".star-rating-container").fadeTo(0, 0);
            $(".book-item").mouseover(function () {
                //var current_item =
                $(this).find('div.star-rating-container').fadeTo(0, 0.8);
            }).mouseout(function () {
                $(this).find('div.star-rating-container').fadeTo(0, 0);
            });
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

    var sticky = new Waypoint.Sticky({
        element: $('.category-list')[0]
    });

    refreshWaypointsLibrary();

    loadingDiv = $("#loadingDiv");
    alertDiv = $("#rating-success-alert-container");

    loadingDiv.hide();

    $('.category-list-item').click(function (e) {
        e.preventDefault();
        $('html, body').animate({ scrollTop: 0 }, 'fast');
        categoryId = $(this).attr('category-id');

        nextPage = -1;
        $('.category-list-item.active').removeClass('active');
        $(this).addClass('active');

        getItemList(1);
    });

    getItemList(1);

});
