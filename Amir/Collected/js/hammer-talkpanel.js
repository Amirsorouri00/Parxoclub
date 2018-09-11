// Hammer On Talk Panel
var talkPanelHammer = document.querySelector('.talk-panel');
var hammer = new Hammer(talkPanelHammer);
hammer.get('swipe').set({
    direction: Hammer.DIRECTION_ALL,
    touchAction: 'auto'
});

hammer.on('swiperight', function(ev) {
    $('.talk-panel').css({
        'transform': 'translateX(0px)'
    });
});