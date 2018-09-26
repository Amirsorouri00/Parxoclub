// Hammer On Menu
var menuHammer = document.querySelector('.mobile-menu-base');
var hammer = new Hammer(menuHammer);
hammer.get('pan').set({ direction: Hammer.DIRECTION_ALL });

hammer.on('panleft', function(ev) {
    $('.mobile-main').removeClass('active');
    $('.mobile-menu-back').removeClass('active');
    $('.header .nav .logo').removeClass('active');
    $('.mobile-menu-base').removeClass('active');
});