var alertDiv;
var commentList;

function RefreshCommentList(response) {
    commentList.empty();

    if ( typeof response === 'undefined' ) {
        $.ajax({
            url: urlForBookComment,
            type: 'GET',
            success: function (response) {
                RefreshCommentList(response);
            }
        });
    }

    for ( var i in response ) {
        commentList.append("<li class=\"list-group-item\"><span class=\"badge\">"+response[i]['user__username'] + "</span>" + response[i]['comment']+"</li>");
    }
}
$(function () {

    commentList = $('#list-comment');

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

    // comment form
    $('#form-comment').submit(function (e) {
        var form = $(this);
        $.ajax({
            url: urlForBookComment,
            type: form.attr('method'),
            data: form.serialize(),
            success: function (response) {
                RefreshCommentList(response);
            }
        });
        return false;
    });

    RefreshCommentList();
});