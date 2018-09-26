$('.burger').click(function() {
    $('.mobile-main').toggleClass('active');
    $('.mobile-menu-back').toggleClass('active');
    $('.header .nav .logo').toggleClass('active');
    $('.mobile-menu-base').toggleClass('active');

});
$('.mobile-menu-back').click(function() {
    $('.mobile-main').toggleClass('active');
    $('.mobile-menu-back').toggleClass('active');
    $('.header .nav .logo').toggleClass('active');
    $('.mobile-menu-base').toggleClass('active');
});

$(".mobile-menu-base").click(function(event) {
    event.stopPropagation();
});


$('#idHeaderUserContainer').click(function() {
    $('.mobile-main').removeClass('active');
    $('.mobile-menu-back').removeClass('active');
    $('.header .nav .logo').removeClass('active');
    $('.mobile-menu-base').removeClass('active');
});

$('#idHeaderLangContainer').click(function() {
    $('.mobile-main').removeClass('active');
    $('.mobile-menu-back').removeClass('active');
    $('.header .nav .logo').removeClass('active');
    $('.mobile-menu-base').removeClass('active');
});

if ($(window).width() < 739) {
    var transformRatio = 'translateX(-' + $(window).width() + 'px)';
    $('.user-chat').click(function() {
        $('.talk-panel').css({
            'transform': transformRatio,
            'z-index': '100'
        });
    });
    $('.member-menu .column').click(function() {
        var memberSubMenuCHeck = $(this).find('.submenu').length;
        if (memberSubMenuCHeck != true) {
            $('.member-docs').css({
                'transform': transformRatio,
                'z-index': '100'
            });
        }
    });
    $('.member-menu .column .submenu .item ').click(function() {
        $('.member-docs').css({
            'transform': transformRatio,
            'z-index': '100'
        });
    });
}

$('.mobile-back-chat').click(function() {
    $('.talk-panel').css({
        'transform': 'translateX(0px)'
    });
});

$('.mobile-back-member').click(function() {
    $('.member-docs').css({
        'transform': 'translateX(0px)'
    });
});