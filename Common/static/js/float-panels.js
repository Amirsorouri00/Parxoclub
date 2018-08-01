

$('.float-chat-btn').click(function() {
    $(".float-chat-base").toggleClass("active");
});

$('.float-calendar-btn').click(function() {
    $(".float-calendar-base").toggleClass("active");
});

$(function() {
    $(".chat-drag").draggable({ handle: ".float-chat-header", containment: "window", opacity: 0.8 });
});


$(function() {
    $(".calendar-drag").draggable({ handle: ".float-calendar-header ", containment: "window", opacity: 0.8 });
});


$('#idChatInputFloat').on('input', function() {

    if ($(this).val().length == 0)
        $(".float-send-btn").removeClass("active");
    else
        $(".float-send-btn").addClass("active");
});


$('.float-calendar-table-base table tbody tr td').click(function() {
    $(".float-calendar-table-base table tbody tr td").removeClass("active");
    $(".float-calendar-table-container").addClass("active");
    $(this).addClass("active");
    $("#idFloatPrev").toggle("active");
    $("#idFloatSep1").toggle("active");
    $("#idFloatToday").toggle("active");
    $("#idFloatSep2").toggle("active");
    $("#idFloatNext").toggle("active");
    $("#idFloatBack").toggle("active");
});


$('#idFloatBack').click(function() {
    $(".float-calendar-table-base table tbody tr td").removeClass("active");
    $(".float-calendar-table-container").removeClass("active");
    $(this).addClass("active");    
    $("#idFloatPrev").toggle("active");
    $("#idFloatSep1").toggle("active");
    $("#idFloatToday").toggle("active");
    $("#idFloatSep2").toggle("active");
    $("#idFloatNext").toggle("active");
    $("#idFloatBack").toggle("active");
});

$('#idFloatChatLoader').click(function() {
    var floatBtn = $('.chat-drag').hasClass('active'),
        floatBox = $('.float-chat-base').hasClass('active');
    $(".chat-drag").toggleClass("active");
    if (floatBtn == true && floatBox == true) {
        $(".float-chat-base").removeClass("active");
    } else if (floatBtn != true && floatBox != true) {
        setTimeout(function() {
            $(".float-chat-base").addClass("active");
        }, 200);
    }
});

$('#idFloatCalendarLoader').click(function() {
    var floatBtn = $('.calendar-drag').hasClass('active'),
        floatBox = $('.float-calendar-base').hasClass('active');
    $(".calendar-drag").toggleClass("active");
    if (floatBtn == true && floatBox == true) {
        $(".float-calendar-base").removeClass("active");
    } else if (floatBtn != true && floatBox != true) {
        setTimeout(function() {
            $(".float-calendar-base").addClass("active");
        }, 200);
    }
});