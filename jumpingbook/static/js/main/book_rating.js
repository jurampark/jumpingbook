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

function offRatingLibrary(selector) {
    $(selector).off();
}
function onRatingLibrary(selector) {
    $(selector).rating();
    $(selector).on('change', function () {
        var current_item = $(this).parent().parent().parent().parent();

        $.ajax({
            type: 'POST',
            url: urlForBookRating,
            data: {
                "item-id": $(this).attr('item-id'),
                "rating": $(this).val()
            },
            success: function () {
                alertDiv.show();
                setTimeout(function () {
                    alertDiv.hide();
                }, 2000);
                current_item.fadeTo(400, 0.5);
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

            if (page == 1) {
                $('.book-item-container').empty();
            }

            nextPage = data['next_page_num'];

            for (var index in data['items']) {
                var item = data['items'][index];
                if ( item['image_url'].length == 0 ) item['image_url'] = urlNoThumbnail;
                var elem = "    <a href=\"" + get_book_detail_url(item['id']) + "\"> <div class=\"book-item\" item-id=\"" + item['id'] + "\"> \
                                <div class=\"img-container\"> \
                                <img src=\"" + item['image_url'] + "\" /> \
                                </div> \
                                <div class=\"star-rating-container\"> \
                                  <div class=\"item-title\"><span class='text'>" + item['title'] + "</span></div> \
                                  <div class=\"item-author\">" + item['author'] + "</div> \
                                  <input item-id=\"" + item['id'] + "\" type=\"number\" class=\"rating\" min=0 max=10 step=1 data-size=\"sm\" > \
                                </a>";
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

    $('.list-menu').click(function (e) {
        e.preventDefault();
        $('html, body').animate({scrollTop: 0}, 'fast');
        categoryId = $(this).attr('category-id');
        nextPage = -1;
        $('.list-menu.active .highlight').remove();
        $('.list-menu.active').removeClass('active');
        $(this).addClass('active');
        $('.list-menu.active .text').append('<span class="highlight"></span>');

        getItemList(1);
    });

    getItemList(1);

});
