function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$( document ).ready(function() {
    $('.category-item').click( function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: urlForScrap,
            data: {
                'category-code': $(this).attr('category-code'),
                'category-name': $(this).attr('category-name')
            },
            success: function(data){
                var value = data['testkey'];
                alert( value );
            },
            error: function(xhr, type, exception) {
                alert("ajax error response type "+type);
            }
        });
    });
});