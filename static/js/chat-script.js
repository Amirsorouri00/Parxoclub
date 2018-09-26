window.onload = function() {
        $('.back-last-talk-container').addClass("active"); 
}
$(document).on("click", ".back-last-talk-container", function() {
    $(this).toggleClass('active');
});