// Hammer On Talk Panel
var talkPanelHammer = document.querySelector('.talk-panel');
var hammer = new Hammer(talkPanelHammer);
hammer.get('pan').set({ direction: Hammer.DIRECTION_ALL });

hammer.on('panleft', function(ev) {
    $('.talk-panel').css({
        'transform': 'translateX(0px)'
    });
});