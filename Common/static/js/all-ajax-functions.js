var csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function sendData(type, url, data) {
    $.ajax({
        type: type,
        url: url,
        data: data,
        success: function(data){
            console.log(data);
            alert(data);
            if (data.context) {
                // data.redirect contains the string URL to redirect to
                window.location.href = data.context;
            }
            if (data.is_taken) {
                alert(alert(data.error_message));
            }
        },
    });
};

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function checkUserNamePasswordExistance(object, type, url){
    $(object).change(function () {
        console.log( $(this).val() );
        var username = $(this).val();
        $.ajax({
            url: url,
            data: {
              'username': username
            },
            dataType: 'json',
            success: function (data) {
              if (data.is_taken) {
                alert(data.error_message);
              }
            }
        });
    });
}


function MemberSearch(object, type, url){
    $(object).keyup(function () {
        console.log( 'insearch' );
        var searchText = $(this).val();
        $.ajax({
            url: url,
            data: {
              'member_search': searchText
            },
            dataType: 'json',
            success: function (search_result) {
              console.log('in search');  
              if (search_result) {
                console.log('searched');
                console.log(search_result.users);
                //alert(search_result.error_message);
              }
            }
        });
    });
}
