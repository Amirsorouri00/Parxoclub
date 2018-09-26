// Hammer On Member Docs
var memberDocsHammer = document.querySelector('.member-docs');
var hammer = new Hammer(memberDocsHammer);
hammer.get('pan').set({ direction: Hammer.DIRECTION_ALL });

hammer.on('panleft', function(e) {
    var target = $(e.target);
    var isCarousel = target.hasClass("doc-photo") || target.hasClass("doc-carousel") || target.hasClass("carousel-cell") || target.hasClass("carousel-img");
    if (!isCarousel) {
        $('.member-docs').css({
            'transform': 'translateX(0px)'
        });
    }
});