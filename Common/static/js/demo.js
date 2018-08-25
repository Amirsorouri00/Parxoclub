/* Modal */
$(document).on("click", "[modal-btn='show']", function(e) {
    if (!e) var e = window.event;
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();

    $("div.main").addClass("active");
    var idModal = this.getAttribute('id-modal');
    document.getElementById(idModal).classList.add("active");
});

/* DateTime Now! */
$(function() {
    $('input[type="Time"][value="now"]').each(function() {
        var d = new Date(),
            h = d.getHours(),
            m = d.getMinutes();
        if (h < 10) h = '0' + h;
        if (m < 10) m = '0' + m;
        $(this).attr({
            'value': h + ':' + m
        });
    });
});

var userChatCurrent = null;
$('.user-chat').click(function() {
    if (userChatCurrent != null)
        userChatCurrent.classList.toggle('active');
    userChatCurrent = this;
    userChatCurrent.classList.toggle('active');
});

var sideMenuCurrent = null;
$('.sidemenu .base .column ').click(function() {
    var isSame = (sideMenuCurrent == this);
    if (sideMenuCurrent != null)
        sideMenuCurrent.classList.toggle('active');
    if (isSame)
        sideMenuCurrent = null;
    else {
        sideMenuCurrent = this;
        sideMenuCurrent.classList.toggle('active');
    }
});

var memberMenuCurrent = null;
$('.member-menu .column .main ').click(function() {
    var isSame = (memberMenuCurrent == this.parentNode);
    if (memberMenuCurrent != null)
        memberMenuCurrent.classList.toggle('active');
    if (isSame)
        memberMenuCurrent = null;
    else {
        memberMenuCurrent = this.parentNode;
        memberMenuCurrent.classList.toggle('active');
    }
});

var memberSubMenuCurrent = null;
$('.member-menu .column .submenu .item ').click(function() {
    if (memberSubMenuCurrent != null)
        memberSubMenuCurrent.classList.toggle('active');

    memberSubMenuCurrent = this;
    memberSubMenuCurrent.classList.toggle('active');
});

var maintenanceMenuCurrent = null;
$('.menu-base-maintenance .column .main ').click(function() {
    var isSame = (maintenanceMenuCurrent == this.parentNode);
    if (maintenanceMenuCurrent != null)
        maintenanceMenuCurrent.classList.toggle('active');
    if (isSame)
        maintenanceMenuCurrent = null;
    else {
        maintenanceMenuCurrent = this.parentNode;
        maintenanceMenuCurrent.classList.toggle('active');
    }
});

var maintenanceSubMenuCurrent = null;
$('.menu-base-maintenance .column .submenu .item ').click(function() {
    if (maintenanceSubMenuCurrent != null)
        maintenanceSubMenuCurrent.classList.toggle('active');

    maintenanceSubMenuCurrent = this;
    maintenanceSubMenuCurrent.classList.toggle('active');
});


$('.event-detial').click(function() {
    $(".event-detial").removeClass("active");
    $(this).addClass("active");
});


$('.news-detial').click(function() {
    $(".news-detial").removeClass("active");
    $(this).addClass("active");
});


$('.calendar-table-base table tbody tr td').click(function() {
    $(".calendar-table-base table tbody tr td").removeClass("active");
    $(this).addClass("active");
});

$('.float-calendar-table-base table tbody tr td').click(function() {
    $(".float-calendar-table-base table tbody tr td").removeClass("active");
    $(".float-calendar-table-container").addClass("active");
    $('#idFloatPrev').css({
        'display': 'none',
    });
    $('#idFloatSep1').css({
        'display': 'none',
    });
    $('#idFloatToday').css({
        'display': 'none',
    });
    $('#idFloatSep2').css({
        'display': 'none',
    });
    $('#idFloatNext').css({
        'display': 'none',
    });
    $('#idFloatBack').css({
        'display': 'flex',
    });
    $(this).addClass("active");
});


$('#idFloatBack').click(function() {
    $(".float-calendar-table-base table tbody tr td").removeClass("active");
    $(".float-calendar-table-container").removeClass("active");
    $('#idFloatPrev').css({
        'display': 'flex',
    });
    $('#idFloatSep1').css({
        'display': 'flex',
    });
    $('#idFloatToday').css({
        'display': 'flex',
    });
    $('#idFloatSep2').css({
        'display': 'flex',
    });
    $('#idFloatNext').css({
        'display': 'flex',
    });
    $('#idFloatBack').css({
        'display': 'none',
    });
    $(this).addClass("active");
});