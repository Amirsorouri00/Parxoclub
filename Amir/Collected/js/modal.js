/*
 * Shortcut key to close modal form
 */ 
$(document).keydown(function(e){
    /* Escape key = 27*/ 
    if(e.which == 27){
        if ($('.spinner-base').hasClass('active'))
            return false;    
        modal.close();
    }
});

/*
 * Modal close button
 */ 
$(document).on("click", "[modal-close]", function() {
    modal.close();
});

/*
 * Modal functions
 */ 
var modal = {
    show: function() {
        $("div.main").addClass("active");
        var elemModal = $(".custom-modal");
        elemModal.addClass("active");
    },
    close: function() {
        $("div.main").removeClass("active");
        var elemModal = $(".custom-modal");
        elemModal.removeClass("active");
        //elemModal.empty();
    }
}