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
    alertDiv = $("#alert-container");
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
        var current_item = $(this).parent().parent();
        $.ajax({
            type: 'POST',
            url: urlForBookRating,
            data: {
                "item-id": $(this).parent().parent().attr('item-id'),
                "rating": $(this).val()
            },
            success: function () {
              $("#alert-rate-container").show();
              setTimeout(function() {
                  $("#alert-rate-container").hide();
              }, 2000);
                current_item.remove();
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
    })


    $(".btn-wish").mouseover(function(){
      //var current_item =
        $(this).css("color", "blue");
    }).mouseout(function(){
        $(this).css("color", "black");
    });
    $(".btn-wish").on('click', function(){
      var current_item = $(this).parent().parent().parent();
      $.ajax({
          type: 'POST',
          url: urlForAddWishList,
          data: {
              "item-id": current_item.attr('item-id'),
          },
          success: function () {
            $("#alert-wish-container").show();
            setTimeout(function() {
                $("#alert-wish-container").hide();
            }, 2000);
              current_item.remove();
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

    $(".btn-black").mouseover(function(){
      //var current_item =
        $(this).css("color", "red");
    }).mouseout(function(){
        $(this).css("color", "black");
    });
    $(".btn-wish").on('click', function(){
      var current_item = $(this).parent().parent().parent();
      $.ajax({
          type: 'POST',
          url: urlForAddBlackList,
          data: {
              "item-id": current_item.attr('item-id'),
          },
          success: function () {
            $("#alert-black-container").show();
            setTimeout(function() {
                $("#alert-black-container").hide();
            }, 2000);
              current_item.remove();
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


    //$.ajax({
    //    type: 'POST',
    //    url: urlForRecommendedBook,
    //    data: {},
    //    success: function (data) {
    //        $('input.rating').off();
    //        for (var index in data) {
    //            var item = data[index];
    //            var elem = "    <div class=\"book-item\" item-id=\"" + item['id'] + "\"> \
    //    <div class=\"img-container\"> \
    //    <img src=\"http://youth.sangju.go.kr/fileUpload/contentsboard/book_00406.jpg\" /> \
    //    </div> \
    //    <div class=\"star-rating-container\"> \
    //    <div class=\"item-title\">" + item['name'] + "</div> \
    //    <div class=\"item-author\">" + item['author'] + "</div> \
    //    <input type=\"hidden\" class=\"rating\" data-fractions=\"2\"/> \
    //    </div> \
    //    </div>";
    //            $('.book-item-container').append(elem);
    //        }
    //        $('input.rating').rating();
    //        $('input.rating').on('change', function () {
    //            var current_item = $(this).parent().parent();
    //            $.ajax({
    //                type: 'POST',
    //                url: urlForBookRating,
    //                data: {
    //                    "item-id": $(this).parent().parent().attr('item-id'),
    //                    "rating": $(this).val()
    //                },
    //                success: function () {
    //                    current_item.remove();
    //                },
    //                error: function (xhr, type, exception) {
    //                    alert("ajax error response type2 " + type);
    //                }
    //            })
    //        })
    //    },
    //    error: function (xhr, type, exception) {
    //        alert("ajax error response type1 " + type);
    //    }
    //});
