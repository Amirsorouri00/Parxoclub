/* Pjax form submit */
$(document).on("submit", "form[data-pjax]", function (event) {
    var url = $(this).attr('action');
    var container = $(this).attr('data-pjax-container');
    var beforeSendCallback = $(this).attr('data-pjax-beforeSend');
    var successCallback = $(this).attr('data-pjax-success');
    if ((url == null) || (container == null))
    {
        jQuery.error('\n\nPraxo: pjax missing attribute(s)!\n---------------------------------\n');
        return;
    } 

    if (container == "modal")
    {
        container = ".custom-modal";
        modal.show();
    }

    jQuery.pjax.submit(event, {
        "push":false,
        "replace":false,
        "timeout":1000,
        "scrollTo":false,
        "url": url,
        "container": container,
        "beforeSendCallback": beforeSendCallback,
        "successCallback": successCallback,
    });

    if ($(this).attr('show-spinner') != null)
        $('.spinner-base').addClass('active');
});

/* Pjax on all elements having [data-pjax] attribute */
$(document).on("click", "[data-pjax]", function (event) {
    var url = null;
    var tag_name = this.tagName.toUpperCase();
    if (tag_name == "FORM")
        return;
    else if (tag_name == "A")
    {
        event.preventDefault();
        url = $(this).attr('href');
    }
    else
        url = $(this).attr('data-pjax-url');

    var push = ($(this).attr('data-pjax-push') == null);
    var container = $(this).attr('data-pjax-container');
    var type = $(this).attr('data-pjax-type');
    if (type == null)
        type = "GET";
    var beforeSendCallback = $(this).attr('data-pjax-beforeSend');
    var successCallback = $(this).attr('data-pjax-success');
    
    if ($(this).attr('show-spinner') != null)
        $('.spinner-base').addClass('active');

    if ((url == null) || (container == null))
    {
        jQuery.error('\n\nPraxo: pjax missing attribute(s)!\n---------------------------------\n');
        return;
    }

    if (container == "modal")
    {
        container = ".custom-modal";
        modal.show();
    }

    $.pjax({
        push: push,
        type: type,
        url: url, 
        container: container,
        beforeSendCallback: beforeSendCallback,
        successCallback: successCallback,
    });
});

/* Pjax on beforeSend */
$(document).on('pjax:beforeSend', function(event, xhr, options) {
    if (options.beforeSendCallback != null)
    {
        var _callback = window[options.beforeSendCallback];
        if(typeof _callback === 'function')
            _callback(options);
    }
});

/* Pjax on success */
$(document).on('pjax:success', function(event, data, status, xhr, options) {
    $('.spinner-base').removeClass('active');
    
    if (options.successCallback != null)
    {
        var _callback = window[options.successCallback];
        if(typeof  _callback === 'function')
            _callback();
    }

    var json_data = null;
    try { 
        json_data = JSON.parse(data);
    }
    catch (err) { 
        json_data = null;
    }
    
    if (json_data != null)
    {
        if ("modal" in json_data)
            modal.close();

        if ("notification" in json_data)
        {
            notif_data = json_data['notification']
            type = notification.type.PRIMARY;
            if (notif_data.type == "success")
                type = notification.type.SUCCESS;
            notification.show(type, notif_data.message, 3000);
        }
    }   
})