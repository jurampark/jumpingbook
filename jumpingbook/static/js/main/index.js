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
    //alert('test');

    $('#add-rating').click( function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: urlForBookList,
            data: {},
            success: function(data){
                for(var index in data) {
                    var item = data[index];
                    var elem = "    <div class=\"book-item\" item-id=\"" + item['id'] + "\"> \
                                        <div class=\"img-container\"> \
                                            <img src=\"http://youth.sangju.go.kr/fileUpload/contentsboard/book_00406.jpg\" /> \
                                        </div> \
                                        <div class=\"star-rating-container\"> \
                                            <div class=\"item-title\">" + item['name'] + "</div> \
                                            <div class=\"item-author\">" + item['author'] + "</div> \
                                            <div class=\"star-rating\"> \
                                                <input class=\"rb0\" id=\"Ans_1\" name=\"numericRating\" type=\"radio\" value=\"0\" checked=\"checked\"/> \
                                                <input class=\"rb1\" id=\"Ans_2\" name=\"numericRating\" type=\"radio\" value=\"1\"/> \
                                                <input class=\"rb2\" id=\"Ans_3\" name=\"numericRating\" type=\"radio\" value=\"2\"/> \
                                                <input class=\"rb3\" id=\"Ans_4\" name=\"numericRating\" type=\"radio\" value=\"3\"/> \
                                                <input class=\"rb4\" id=\"Ans_5\" name=\"numericRating\" type=\"radio\" value=\"4\"/> \
                                                <input class=\"rb5\" id=\"Ans_6\" name=\"numericRating\" type=\"radio\" value=\"5\"/> \
                                                <input class=\"rb6\" id=\"Ans_7\" name=\"numericRating\" type=\"radio\" value=\"6\"/> \
                                                <input class=\"rb7\" id=\"Ans_8\" name=\"numericRating\" type=\"radio\" value=\"7\"/> \
                                                <input class=\"rb8\" id=\"Ans_9\" name=\"numericRating\" type=\"radio\" value=\"8\"/> \
                                                <input class=\"rb9\" id=\"Ans_10\" name=\"numericRating\" type=\"radio\" value=\"9\"/> \
                                                <input class=\"rb10\" id=\"Ans_11\" name=\"numericRating\" type=\"radio\" value=\"10\"/> \
                                 \
                                                <label for=\"Ans_1\" class=\"star rb0l\" onclick=\"\"></label> \
                                                <label for=\"Ans_2\" class=\"star rb1l\" onclick=\"\"></label> \
                                                <label for=\"Ans_3\" class=\"star rb2l\" onclick=\"\"></label> \
                                                <label for=\"Ans_4\" class=\"star rb3l\" onclick=\"\"></label> \
                                                <label for=\"Ans_5\" class=\"star rb4l\" onclick=\"\"></label> \
                                                <label for=\"Ans_6\" class=\"star rb5l\" onclick=\"\"></label> \
                                                <label for=\"Ans_7\" class=\"star rb6l\" onclick=\"\"></label> \
                                                <label for=\"Ans_8\" class=\"star rb7l\" onclick=\"\"></label> \
                                                <label for=\"Ans_9\" class=\"star rb8l\" onclick=\"\"></label> \
                                                <label for=\"Ans_10\" class=\"star rb9l\" onclick=\"\"></label> \
                                                <label for=\"Ans_11\" class=\"star rb10l last\" onclick=\"\"></label> \
                                 \
                                                <label for=\"Ans_1\" class=\"rb\" onclick=\"\">0</label> \
                                                <label for=\"Ans_2\" class=\"rb\" onclick=\"\">1</label> \
                                                <label for=\"Ans_3\" class=\"rb\" onclick=\"\">2</label> \
                                                <label for=\"Ans_4\" class=\"rb\" onclick=\"\">3</label> \
                                                <label for=\"Ans_5\" class=\"rb\" onclick=\"\">4</label> \
                                                <label for=\"Ans_6\" class=\"rb\" onclick=\"\">5</label> \
                                                <label for=\"Ans_7\" class=\"rb\" onclick=\"\">6</label> \
                                                <label for=\"Ans_8\" class=\"rb\" onclick=\"\">7</label> \
                                                <label for=\"Ans_9\" class=\"rb\" onclick=\"\">8</label> \
                                                <label for=\"Ans_10\" class=\"rb\" onclick=\"\">9</label> \
                                                <label for=\"Ans_11\" class=\"rb\" onclick=\"\">10</label> \
                                 \
                                                <div class=\"rating\"></div> \
                                                <div class=\"rating-bg\"></div> \
                                            </div> \
                                            <!-- star-rating --> \
                                        </div> \
                                    </div>";
                    $('.book-item-container').append( elem );
                }
            },
            error: function(xhr, type, exception) {
                alert("ajax error response type "+type);
            }
        });
    });
});