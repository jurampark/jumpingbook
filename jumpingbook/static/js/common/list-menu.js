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

$(function() {

    //$(".star-rating-container").fadeTo(0, 0);
    //$(".book-item").mouseover(function(){
    //  //var current_item =
    //    $(this).find('div.star-rating-container').fadeTo(0, 0.8);
    //}).mouseout(function(){
    //    $(this).find('div.star-rating-container').fadeTo(0, 0);
    //});

    $('.list-menu').click(function (e) {
        e.preventDefault();
        $('html, body').animate({scrollTop: 0}, 'fast');
        $('.list-menu.active .highlight').remove();
        $('.list-menu.active').removeClass('active');
        $(this).addClass('active');
        $('.list-menu.active .text').append('<span class="highlight"></span>');

        listMenuRefresh();
    });
});