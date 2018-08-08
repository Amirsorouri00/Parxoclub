var csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!CsrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function CsrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

function SendData(type, url, data, callbackSuccess, callbackError, from) {
    console.log('senddata from: ' + from);
    // callbackSuccess = RedirectInto;
    // callbackError = RedirectInto;
    $.ajax({
        type: type,
        url: url,
        data: data,
        success: function(data) {
            callbackSuccess(window, data, from);
        },
        error: function(data) {
            console.log('error: ' + JSON.stringify(data));
            callbackError(window, data, from);
        }
    });
};

function Login(type, url, username, password) {
    console.log('inlogin');
    if ((username != "") && (password != "")) {
        //hide(); //hide pop ups about empty field
        type = 'POST';
        url = url;
        data = { username: username, password: password }; //It would be best to put it like that, make it the same name so it wouldn't be confusing
        console.log(password);
        SendData(type, url, data, RedirectInto, ErrorManagement, 'Login'); // Pass the variables here as a parameter     
    } else {
        $("#empty").show();
    } // pop ups 
};

function RedirectInto(winref, data, bind, from) {
    console.log(data);
    alert(data);
    if (data.context) {
        // data.redirect contains the string URL to redirect to
        winref.location.href = data.context;
        //window.location.href = data.context;
    } else { console.log('context in the data has not any value'); }
    /*if (data.is_taken) {
        alert(alert(data.error_message));
    } */
};

function CheckUserNamePasswordExistance(object, type, url) {
    //url = '/ajax/member/validate_username/';
    //CheckUserNamePasswordExistance("#idUsername ", "POST ", url);
    $(object).change(function() {
        console.log($(this).val());
        var username = $(this).val();
        $.ajax({
            url: url,
            data: {
                'username': username
            },
            dataType: 'json',
            success: function(data) {
                if (data.is_taken) {
                    alert(data.error_message);
                }
            }
        });
    });
};

function Bind(winref, data, from) {
    data2 = JSON.parse(data);
    console.log('in Bind : ' + data);
    //console.log('in Bind : '+ data2.DocCats[0].sub_menu);
    console.log('from: ' + from);
    if (from == 'MemberSearch') {
        $.each(data2.users, function(i, item) {
            //console.log('in Bind2 : '+ data2.users[0].username);
            //str = "<div class='result-item'><div class='photo-container'><div class='photo'></div></div><div class='detail'><span class='name'> first_name last_name </span><span class='position'>Title/Position</span></div></div>"
            res = search_object_to_append.replace("first_name", item.first_name).replace("last_name", item.last_name);
            //$('#idResultContainer .result-list').append("<div class='result-item'><div class='photo-container'><div class='photo'></div></div><div class='detail'><span class='name'>" + item.first_name + ' ' + item.last_name +"</span><span class='position'>Title/Position</span></div></div>");
            $('#idResultContainer .result-list').append(res);
        });
    } else if (from == 'DocumentCategories') {
        console.log('in from');
        var object = $('.member-menu .overlay-scroll');
        CreateDocumentCategoryMenu(data2.DocCats);
        // $('#ajax_category').append(res);
    } else { console.log("from doesn't match") };
    //console.log($(bind_object).find('.result-list .result-item .detail span'));
    //$(bind_object).find('.result-list .result-item .detail .detail').append("<span class='name'>" + data + '</span>');
    //$('#idResultContainer .result-list').append("<div class='result-item'><div class='photo-container'><div class='photo'></div></div><div class='detail'><span class='name'>Masoud Nourbakhsh</span><span class='position'>Title/Position</span></div></div>");
    //$(bind_object).append("<span class='name'>"+data+'</span>');
}

function CreateDocumentCategoryMenu(data) {
    //console.log('CreateDocumentCategoryMenu:' + data);
    $.each(data, function(i, item) {
        var tmp = document_categories_object_to_append.replace("main_ajax_id", "main_ajax_" + item.id).replace("icon_name", item.icon_name).replace("classTitle", item.name);
        if (i == 0) {
            tmp = tmp.replace("column", "column active")
        }
        //console.log('submenu length: '+ item.sub_menu.length);
        if (item.sub_menu.length != 0) {
            tmp = tmp.replace("<div class='expander'></div>", "<div class='expander'><span class='icon-right'></span></div>");
        }
        var res = tmp;
        $('#ajax_category').append(res);
        var str = "<div class='submenu'>";
        var tmp2 = '';
        $.each(item.sub_menu, function(j, item_2) {
            //          console.log('submenu:')
            tmp2 = document_categories_object_to_appendto_submenu.replace("Sonography", item_2.name);
            str = str + tmp2;
        });
        res2 = str + "</div>"
        $("#ajax_category .column .main_ajax_" + item.id).after(res2);

    });
};

function ErrorManagement() {};

function MemberSearch(object, type, url, search_text) {
    console.log('insearch');
    var from = 'MemberSearch';
    //var searchText = $(this).val();
    var data = {
        'member_search': search_text
    };
    SendData(type, url, data, Bind, ErrorManagement, from);
};

function DocumentCategories(type, url) {
    var from = 'DocumentCategories';
    SendData(type, url, '', Bind, ErrorManagement, from);
};

// function for appending the users result into html
function SearchSuccess(data) {
    $('#search-results').html(data);
};


// success: function(data){
//     console.log(data);
//     alert(data);
//     if (data.context) {
//         // data.redirect contains the string URL to redirect to
//         window.location.href, data.context;
//         //window.location.href = data.context;
//     }
//     if (data.is_taken) {
//         alert(alert(data.error_message));
//     }
// }