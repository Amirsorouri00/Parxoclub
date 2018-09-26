function initCarousel() {
    /* Slick */
    $('.doc-carousel').slick({
        lazyLoad: 'ondemand', // ondemand progressive anticipated
        dots: true,
    });
    
    resizeCarousel();
};

function resizeCarousel() {
    var docCarouselHeight = $('.doc-carousel').height();
    var docCarouselWidth = $('.doc-carousel').width();
    $('.slick-track').css('width', docCarouselWidth);
    $('.carousel-cell').css('max-height', docCarouselHeight + 'px');
    $('.carousel-img').css('min-height', docCarouselHeight + 'px');
    $('.carousel-img').css('min-width', docCarouselWidth + 'px');
};

$(document).on("click", ".carousel-cell", function() {
    
})