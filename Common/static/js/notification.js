/* Notification */
$(document).on("click", ".notif-base", function() {
    notification.close(this);
});

var notification = {
    type: {
        NEUTRAL: 'notif-bg-gray',
        PRIMARY: 'notif-bg-blue',
        SUCCESS : 'notif-bg-cyan',
        WARNING : 'notif-bg-yellow',
        ERROR : 'notif-bg-red',
    },

    show: function(type, message, timer=0) {
        var elementNotif = document.createElement('div');
        elementNotif.innerHTML = `
            <div class="notif-container">
                <span>${message}</span>
            </div>`;
        elementNotif.setAttribute('class', 'notif-base ' + type);
        // Code for Chrome, Safari and Opera
        elementNotif.addEventListener("webkitAnimationEnd", notification.dispose);
        // Standard syntax
        elementNotif.addEventListener("animationend", notification.dispose);
        // Close timer
        if (timer > 0)
            setTimeout(notification.close, timer, elementNotif);

        $(".notif-list").append(elementNotif);
    },
    
    close: function(elem) {
        $(elem).addClass("close");
    },

    dispose: function() {
        if ($(this).hasClass('close'))
            $(this).remove();
    }
}