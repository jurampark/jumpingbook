var personal_info_container;
var book_item_container;
var friend_container;

function listMenuRefresh() {

    active_list_menu_item_id = $('.list-menu.active').attr('id');

    if ( active_list_menu_item_id == "personal-info" ) {
        personal_info_container.show();
        book_item_container.hide();
        friend_container.hide();
    } else if ( active_list_menu_item_id == "rating-list" ) {
        personal_info_container.hide();
        book_item_container.show();
        friend_container.hide();
    } else if ( active_list_menu_item_id == "friends" ) {
        personal_info_container.hide();
        book_item_container.hide();
        friend_container.show();
    }
}

$(function() {
    personal_info_container = $('.personal-info-container');
    book_item_container     = $('.book-item-container');
    friend_container        = $('.friend-container');

    listMenuRefresh();
});