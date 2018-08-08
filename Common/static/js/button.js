/* Button taint effect */
$(document).on('click', '.btn-taint', function(e){
    var taint, d, x, y;
    if ($(this).find(".btn-taint-host").length == 0) {
        $(this).prepend("<span class='btn-taint-host'></span>")
    }
    taint = $(this).find(".btn-taint-host");
    taint.removeClass("drop");
    if (!taint.height() && !taint.width()) {
        d = Math.max($(this).outerWidth(), $(this).outerHeight());
        taint.css({ height: d, width: d });
    }
    x = e.pageX - $(this).offset().left - taint.width() / 2;
    y = e.pageY - $(this).offset().top - taint.height() / 2;
    taint.css({ top: y + 'px', left: x + 'px' }).addClass("drop");
});