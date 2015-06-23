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

var mypage_container;
var check_rating_history_container;

$(document).ready(function () {

    mypage_container = $(".mypage-container");
    check_rating_history_container = $(".book-item-container");

    $('#mypage').click( function(e) {
        e.preventDefault();
        mypage_container.show();
        check_rating_history_container.hide();
    });
    $('#check-rating-history').click(function (e) {
        e.preventDefault();
        mypage_container.hide();
        check_rating_history_container.show();

        $.ajax({
            type: 'POST',
            url: urlForRatedBook,
            data: {},
            success: function (data) {
                $('input.rating').off();
                $('.book-item-container').empty();
                for (var index in data) {
                    var item = data[index];
                    var elem = "    <div class=\"book-item\" item-id=\"" + item['id'] + "\"> \
                                        <div class=\"img-container\"> \
                                            <img src=\"" + item['image_url'] + "\" /> \
                                        </div> \
                                        <div class=\"star-rating-container\" score=\"" + item['score'] + "\"> \
                                        <div class=\"item-title\">" + item['title'] + "</div> \
                                        <div class=\"item-author\">" + item['author'] + "</div> \
                                            <input type=\"hidden\" class=\"rating\" readonly=\"readonly\" data-fractions=\"2\"/> \
                                            <button type=\"button\" class=\"cancel btn btn-default btn-sm\">평가 취소</button> \
                                        </div> \
                                    </div>";
                    $('.book-item-container').append(elem);
                }
                $('input.rating').each(function (index) {
                    var score = $(this).parent().attr('score');
                    $(this).rating('rate', score / 2);
                })
                $('button.cancel').click(function (e) {
                    var current_item = $(this).parent().parent();
                    e.preventDefault();
                    $.ajax({
                        type: 'POST',
                        url: urlForCancelRating,
                        data: {
                            "item-id": $(this).parent().parent().attr('item-id')
                        },
                        success: function (data) {
                            current_item.remove();
                        },
                        error: function (xhr, type, exception) {
                            alert("ajax error response type " + type);
                        }
                    });
                });

            },
            error: function (xhr, type, exception) {
                alert("ajax error response type " + type);
            }
        });
    });

    $('.mypage-list-item').click(function(e) {
        e.preventDefault();

        $('.mypage-list-item.active').removeClass('active');
        $(this).addClass('active');
    });

});
