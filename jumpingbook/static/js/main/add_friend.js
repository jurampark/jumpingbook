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

$(document).ready(function () {

    //loadingDiv = $("#loadingDiv");
    //loadingDiv.hide();

    $('.btn-friend').click(function (e) {

        e.preventDefault();

        var td = $(this).parent();
        $.ajax({
            type: 'POST',
            url: urlForAddFriend,
            data: {
                'user-id': $(this).attr('user-id')
            },
            success: function(data){
                td.empty();
                td.append("<span class=\"badge\">friend</span>");
            },
            error: function(xhr, type, exception) {
            }
        });
    });

});
