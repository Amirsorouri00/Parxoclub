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
    //console.log('senddata from: ' + from + ' .url: ' + url);
    // callbackSuccess = RedirectInto;
    // callbackError = RedirectInto;
    $.ajax({
        type: type,
        url: url,
        data: data,
        success: function(data) {
            console.log('sendData: from = ' + from + 'data = ' + data + 'url: ' + url)
            console.dir(data)
            callbackSuccess(window, data, from);
        },
        error: function(data) {
            console.log('error: ' + JSON.stringify(data));
            callbackError(window, data, from);
        }
    });
};

function tConvert(time) {
    // Check correct time format and split into components
    time = time.toString().match(/^([01]\d|2[0-3])(:)([0-5]\d)(:[0-5]\d)?$/) || [time];

    if (time.length > 1) { // If time format correct
        time = time.slice(1); // Remove full string match value
        time[5] = +time[0] < 12 ? 'AM' : 'PM'; // Set AM/PM
        time[0] = +time[0] % 12 || 12; // Adjust hours
    }
    return time.join(''); // return adjusted time or original string
}

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
    console.log('in Bind, from = ' + from);
    //data2 = JSON.parse(data);
    console.log('in Bind, Data: ');
    //console.log('in Bind : '+ data2.DocCats[0].sub_menu);
    if (from == 'MemberSearch') {
        data2 = JSON.parse(data);
        $.each(data2.users, function(i, item) {
            //console.log('in Bind2 : '+ data2.users[0].username);
            //str = "<div class='result-item'><div class='photo-container'><div class='photo'></div></div><div class='detail'><span class='name'> first_name last_name </span><span class='position'>Title/Position</span></div></div>"
            res = search_object_to_append.replace("first_name", item.first_name).replace("last_name", item.last_name);
            //$('#idResultContainer .result-list').append("<div class='result-item'><div class='photo-container'><div class='photo'></div></div><div class='detail'><span class='name'>" + item.first_name + ' ' + item.last_name +"</span><span class='position'>Title/Position</span></div></div>");
            $('#idResultContainer .result-list').append(res);
        });
    } else if (from == 'DocumentCategories') {
        data2 = JSON.parse(data);
        //var object = $('.member-menu .overlay-scroll');
        CreateDocumentCategoryMenu(data2.DocCats);
        // $('#ajax_category').append(res);Calendar
    } else if (from == 'AddNewUserModalLiveChecks') {
        console.log('in Bind, from = ' + from);
        console.dir(data.field);
        //data2 = JSON.parse(data);
        $('#amir_error_add_user_modal_' + data.field).append(data.form)
    } else if (from == 'MaintenanceAddUserModalForm') {
        //data2 = JSON.parse(data);
        $('#amir_error_add_user_modal_email').append(data.form)
    } else if (from == 'EditUserModalLiveChecks') {
        //data2 = JSON.parse(data);
        console.log('Hello from: bind /n EditUserModalLiveChecks')
        tmp = data.form.replace("custom-modal", "custom-modal active");
        $("#idEditUser").replaceWith(tmp);
        // $('#amir_error_add_user_modal_email').append(data.form)
    } else if (from == 'RemoveUserModalLiveChecks') {
        //data2 = JSON.parse(data);
        console.log('Hello from: bind /n RemoveUserModalLiveChecks')
        tmp = data.form.replace("custom-modal", "custom-modal active");
        $("#idRemoveUser").replaceWith(tmp);
        // $('#amir_error_add_user_modal_email').append(data.form)
    } else if (from == 'member') {
        data2 = JSON.parse(data);
        $.each(data2.users, function(i, item) {
            //console.log('in Bind2 : '+ data2.users[0].username);
            //str = "<div class='result-item'><div class='photo-container'><div class='photo'></div></div><div class='detail'><span class='name'> first_name last_name </span><span class='position'>Title/Position</span></div></div>"
            res = search_object_to_append.replace("first_name", item.first_name).replace("last_name", item.last_name);
            //$('#idResultContainer .result-list').append("<div class='result-item'><div class='photo-container'><div class='photo'></div></div><div class='detail'><span class='name'>" + item.first_name + ' ' + item.last_name +"</span><span class='position'>Title/Position</span></div></div>");
        });
    } else if (from == 'Calendar') {
        //console.log('from calendar: ' + data);
        $('.calendar-wrapper').fadeOut("slow", function() {
            var div = $(data.form).hide();
            $(this).replaceWith(div);
            $('.calendar-wrapper').fadeIn("slow");
        });
        //$('.calendar-table-header .month-title').text()
        //$(".calendar-wrapper").replaceWith(data.form);
        //data2 = JSON.parse(data);
    } else if (from == 'CalendarGetData') {
        console.dir('from CalendarGetData: ' + data);
        data2 = JSON.parse(data);
        $.each(data2.types, function(i, item) {
            $('#calendar_my_select').append($('<option>', {
                value: item.name,
                text: item.name,
            }));
            $('#calendar_my_select_edit').append($('<option>', {
                value: item.name,
                text: item.name,
            }));
        });
        //$(".calendar-wrapper").replaceWith(data.form);
        //data2 = JSON.parse(data);
    } else if (from == 'CalendarForm') {
        console.dir('from CalendarForm: ' + data);

    } else if (from == 'GetOneDayEvents') {
        console.dir('from GetOneDayEvents: ' + data);
        data2 = JSON.parse(data);
        events_of_current_day_array = data2;
        console.log(events_of_current_day_array.events[0].id);
        html = '';
        $.each(data2.events, function(i, item) {
            start_time = tConvert(item.start_time);
            end_time = tConvert(item.end_time);
            event_time_range = start_time.toString() + '-' + end_time.toString();
            event_detail_html = calendar_after_sidenav_calendar_wrapper.replace('event_time_range', event_time_range).replace('event_note', item.event_note).replace('AmirEventObject', item.id);
            // $('.base-event-list .overlay-scroll').fadeOut("slow", function() {
            //     var div = $(data.form).hide();
            //     $(this).replaceWith(div);
            //     $('.calendar-wrapper').fadeIn("slow");
            // });
            html += event_detail_html;
        });
        $('.base-event-list .overlay-scroll .event-detial').remove();
        var object = $('.base-event-list .overlay-scroll').append(event_detail_html);
    } else {
        console.log("from doesn't match");
        //console.log(data)
    };
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

function MemberSearch(object, type, url, search_text, from) {
    console.log('insearch');
    //var from = 'MemberSearch';
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

function AddNewUserModalLiveChecks(winRef, data, from, type, url) {
    //url = '/ajax/member/validate_username/';
    //CheckUserNamePasswordExistance("#idUsername ", "POST ", url);
    if (from == 'AddNewUserModalLiveChecks') {
        type = 'POST';
        //console.log('return returned: ' + data);
        SendData(type, '/member/update/', data, Bind, ErrorManagement, 'AddNewUserModalLiveChecks');
    }
    //type = 'POST';
    //url = '{% url "validate_email" %}';
    var object = '#maintenance_email_id, #maintenance_birthdate_id';
    $(object).change(function() {
        console.log($(this).val());
        console.log($(this).attr('name'));
        type = 'POST';
        name = $(this).attr('name');
        value = $(this).val();
        var jsonvar = {};
        jsonvar['' + name] = value;
        console.log('jsonvar: ');
        console.dir(jsonvar);
        //value_field = { name : $(value) };
        data = {
            'field': $(this).attr('name'),
            'value': value,
        }
        console.dir(data);
        //SendData(type, url, '', Bind, ErrorManagement, 'AddNewUserModalLiveChecks');
        SendData(type, url, data, AddNewUserModalLiveChecks, ErrorManagement, 'AddNewUserModalLiveChecks');
        //console.log('return returned: '+data);
        //SendData(type, url, data, Bind, ErrorManagement, 'AddNewUserModalLiveChecks');
        /*$.ajax({
            type: 'Post',
            url: url,
            data: {
                'field': 'ali',
                'email': email
            },
            dataType: 'json',
            success: function(data) {
                console.log(data)
                if (data.is_taken) {
                    $.ajax({
                        type: 'Post',
                        url: "/member/update/",
                        data: data,
                        dataType: 'json',
                        success: function(tmp) {
                            $('#amir_error_add_user_modal_email').append(tmp)
                        }
                    });
                    alert(data.error);
                }
                else {console.log('no error detected in email')}
            }
        });*/
    });
};

function EditUserModalLiveChecks(winRef, data, from, type, url) {
    if (from == 'EditUserModalLiveChecks') {
        data2 = JSON.parse(data);
        console.dir('in EditUserModalLiveChecks, data  = ' + data2.user);
        tmp = { 'user': data2.user, 'id': data2.id }
        console.log(tmp)
        // console.dir('in EditUserModalLiveChecks, data  = ' + data);
        SendData("POST", '/member/edituser/', tmp, Bind, ErrorManagement, 'EditUserModalLiveChecks');
    } else if (from == 'page') {
        console.dir(data)
        SendData("POST", '/member/oneuserinfo/', data, EditUserModalLiveChecks, ErrorManagement, 'EditUserModalLiveChecks');
    }
};

function RemoveUserModalLiveChecks(winRef, data, from, type, url) {
    if (from == 'RemoveUserModalLiveChecks') {
        data2 = JSON.parse(data);
        console.dir('in RemoveUserModalLiveChecks, data  = ' + data2.user);
        tmp = { 'user': data2.user, 'id': data2.id }
        console.log(tmp)
        SendData("POST", '/member/removeuser/', tmp, Bind, ErrorManagement, 'RemoveUserModalLiveChecks');
    } else if (from == 'page') {
        console.dir(data)
        SendData("POST", '/member/oneuserinfo/', data, RemoveUserModalLiveChecks, ErrorManagement, 'RemoveUserModalLiveChecks');
    }
};

function Calendar(winRef, data, from, type, url) {
    $('body').on('click', '#calendar_prev_month', function() {
        //$(object).click(function() {
        var link_to_month = $('#calendar_prev_month').attr('month_link');
        SendData("GET", link_to_month, '', Bind, ErrorManagement, 'Calendar');
    });
    $('body').on('click', '#calendar_next_month', function() {
        //$(object).click(function() {
        var link_to_month = $('#calendar_next_month').attr('month_link');
        SendData("GET", link_to_month, '', Bind, ErrorManagement, 'Calendar');
    });

    $('body').on('click', ".calendar-table-base table tbody tr td", function() {
        GetOneDayEvents($(this));
        $(".calendar-table-base table tbody tr td").removeClass("active");
        $(this).addClass("active");
    });
    $('body').on('click', ".base-event-list .overlay-scroll .event-detial .edit-event-detail-btn", function() {
        event_id = $(".base-event-list .overlay-scroll .event-detial .edit-event-detail-btn").attr("event_object");
        result = '';
        result = events_of_current_day_array.events.find(event => (event.id == event_id));
        $('#calendar_input_title_edit').val('amir');
        $('#calendar_input_start_time_edit').val(result.start_time);
        $('#calendar_input_end_time_edit').val(result.end_time);
        $('#calendar_text_event_note_edit').val(result.event_note);
        $('#calendar_my_select_edit option[value=result.event_type]').attr("selected", "selected");
    });
};

function GetOneDayEvents(day) {
    month_val = $('.calendar-table-header .month-title').attr('value');
    thisday = $(day).find('.date-cell .date-container .date-1');
    month_val += thisday.text().toString();
    data = { 'month_val': month_val };
    url = $('.calendar-table-header .month-title').attr('url');
    SendData("GET", url, data, Bind, ErrorManagement, 'GetOneDayEvents');
}

function calendar_find(specific_array, property_to_check, value_to_check) {
    return specific_array.id === value_to_check;
}



// function CalendarGetData(winRef, url, method, data, bind_object) {
//     SendData("GET", url, '', Bind, ErrorManagement, 'CalendarGetData');
// }

// function AddNewUserModalLiveChecksSendToServer() {
//     $.ajax({
//         type: 'Post',
//         url: url,
//         data: {
//             'field': 'ali',
//             'email': email
//         },
//         dataType: 'json',
//         success: function(data) {
//             console.log(data)
//             if (data.is_taken) {
//                 $.ajax({
//                     type: 'Post',
//                     url: "/member/update/",
//                     data: data,
//                     dataType: 'json',
//                     success: function(tmp) {
//                         $('#amir_error_add_user_modal_email').append(tmp)
//                     }
//                 });
//                 alert(data.error);
//             } else { console.log('no error detected in email') }
//         }
//     });
// };



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