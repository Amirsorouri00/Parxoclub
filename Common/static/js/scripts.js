$(document).ready(function() {
    /* Slim scroll */
    $('.overlay-scroll').overlayScrollbars({ 
        className: "os-theme-dark",
        sizeAutoCapable: true,
        paddingAbsolute: true,
        scrollbars : {
            autoHide: "leave",
            autoHideDelay: 500,
        },
    });

    initCarousel();

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

    /* Carousel Height */
    resizeCarousel();
}

$(window).resize(function() {
    /* Carousel Height */
    resizeCarousel();    
});

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

/* Member search box */
$('#idSearchBoxMember').focus(function() {
    document.getElementById("idResultContainer").classList.toggle('active');
});
$('#idSearchBoxMember').blur(function() {
    document.getElementById("idResultContainer").classList.toggle('active');
});

/* Chat send button */
$(document).on('input', '#idChatInput', function() {
    if ($(this).val().length == 0)
    {
        var elmInput = $(".send-btn");
        elmInput.attr('disabled','disabled');
        elmInput.removeClass("active");
    }
    else
    {
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
$(document).on('click', '.check-box', function() {
    $(this).toggleClass('active');
});

/* Bubble Check Box */
$(document).on('click', '.bubble-checkbox', function() {
    $(this).toggleClass('active');
    $('.remove-chat-tool').toggleClass('active');
});