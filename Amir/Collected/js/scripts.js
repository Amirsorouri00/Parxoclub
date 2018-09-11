$(document).ready(function() {
    /* Slim scroll */
    $('.overlay-scroll').overlayScrollbars({
        className: "os-theme-dark",
        sizeAutoCapable: true,
        paddingAbsolute: true,
        normalizeRTL: true,
        scrollbars: {
            visibility: "auto",
            autoHide: "leave",
            autoHideDelay: 300,
            dragScrolling: true,
            clickScrolling: false,
            touchSupport: true,

        },
        overflowBehavior: {
            x: "hidden",
            y: "scroll"
        },
    });
    // slimScroll({
    //     height: '100%',
    //     distance: '5px',
    //     size: '5px',
    //     color: 'rgba(205, 214, 223, 1)',
    //     wheelStep: '7',
    // });

    /* Slick */
    $('.doc-carousel').slick({
        lazyLoad: 'ondemand', // ondemand progressive anticipated
        dots: true,

    });

    /* CSRF code */
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});


window.onload = function() {
    /* No Field Error */
    var noFieldHeight = $('.no-field-error-base').height();
    $('.no-field-error-base-fake').css('min-height', noFieldHeight + 'px');

    /* Doc No Field Error */
    var docNoFieldHeight = $('.doc-no-field-error').height();
    $('.doc-no-field-error-fake').css('min-height', docNoFieldHeight + 'px');


    // $('.news-photo-editor-container').appendTo('.add-user-input .onmobile-photo-editor')    

}


window.addEventListener('click', function(e) {
    var userPanelVisibility = $("#idUserPanel").attr("visible")
    if (document.getElementById('idUserPanel').contains(e.target) || document.getElementById('idHeaderUserContainer').contains(e.target)) {
        return;
    } else if (userPanelVisibility == "true") {
        var visible = ($("#idUserPanel").attr("visible") == "true");
        visible = !visible;
        document.getElementById("idUserPanel").setAttribute("visible", visible.toString());
        $('#idUserPanel').css({
            'transform': 'scaleY(0)'
        });
        $('#idUserPanelExpander').removeClass("active");
        $('#idUserPanelContainer').removeClass("active");
        $('#idLogoutContainer').css({
            'transition': '200ms ease 80ms',
            'opacity': '0',
        });
    }
    var userPanelVisibility = $("#idLangPanel").attr("visible")
    if (document.getElementById('idLangPanel').contains(e.target) || document.getElementById('idHeaderLangContainer').contains(e.target)) {
        return;
    } else if (userPanelVisibility == "true") {
        var visible = ($("#idLangPanel").attr("visible") == "true");
        visible = !visible;
        document.getElementById("idLangPanel").setAttribute("visible", visible.toString());
        $('#idLangPanel').css({
            'transform': 'scaleY(0)'
        });
        $('#idLangExpander').removeClass("active");
        $('#idLangPanelContainer').removeClass("active");
    }
});

$('#idHeaderUserContainer').click(function() {
    var visible = ($("#idUserPanel").attr("visible") == "true");
    visible = !visible;
    document.getElementById("idUserPanel").setAttribute("visible", visible.toString());
    if (visible) {
        $('#idUserPanel').css({
            'transform': 'scaleY(1)'
        });
        $('#idUserPanelExpander').toggleClass("active");
        $('#idUserPanelContainer').addClass("active");
        $('#idLogoutContainer').css({
            'transition': '500ms ease 80ms',
            'opacity': '1',
        });
    } else {
        $('#idUserPanel').css({
            'transform': 'scaleY(0)'
        });
        $('#idUserPanelExpander').toggleClass("active");
        $('#idUserPanelContainer').removeClass("active");

        $('#idLogoutContainer').css({
            'transition': '200ms ease 80ms',
            'opacity': '0',
        });
    }
});

$('#idHeaderLangContainer').click(function() {
    var visible = ($("#idLangPanel").attr("visible") == "true");
    visible = !visible;
    document.getElementById("idLangPanel").setAttribute("visible", visible.toString());
    if (visible) {
        $('#idLangPanel').css({
            'transform': 'scaleY(1)'
        });
        $('#idLangExpander').toggleClass("active");
        $('#idLangPanelContainer').addClass("active");
    } else {
        $('#idLangPanel').css({
            'transform': 'scaleY(0)'
        });
        $('#idLangExpander').toggleClass("active");
        $('#idLangPanelContainer').removeClass("active");
    }
});







/* Member search box */
$('#idSearchBoxMember').focus(function() {
    document.getElementById("idResultContainer").classList.toggle('active');
});
$('#idSearchBoxMember').blur(function() {
    document.getElementById("idResultContainer").classList.toggle('active');
});

/* Chat send button */
$(document).on('input', '#idChatInput', function() {
    if ($(this).val().length == 0) {
        var elmInput = $(".send-btn");
        elmInput.attr('disabled', 'disabled');
        elmInput.removeClass("active");
    } else {
        var elmInput = $(".send-btn");
        elmInput.removeAttr('disabled');
        elmInput.addClass("active");
    }
});

/* Documents panel menu selection */
$(document).on('click', '.member-menu .column', function() {
    $(this).addClass('active').siblings().removeClass("active");
});

/* Documents category record tr selection */
$(document).on("click", ".rowLink", function() {
    $(this).addClass('active').siblings().removeClass("active");
});

/* Meintenance panel menu selection */
$(document).on('click', '.menu-base-maintenance .column', function() {
    $(this).addClass('active').siblings().removeClass("active");
});

$(document).on('click', '.user-base-maintenance', function() {
    $(this).addClass('active').siblings().removeClass("active");
});


/* Check Box */
$('.check-box').click(function() {
    $(this).toggleClass('active');
});


$('.chat-check-box').click(function() {
    $(this).toggleClass('active');
});



/* Bubble Check Box */
$('.bubble-checkbox').click(function() {
    $(this).toggleClass('active');
    $('.remove-chat-tool').toggleClass('active');
});