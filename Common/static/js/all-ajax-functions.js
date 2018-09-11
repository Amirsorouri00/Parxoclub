var csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!CsrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function CookieHandler(one, two) {
    console.log('CookieHandler: ' + two);
    var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader(one, two);
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
}

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

function fileSendData(type, url, data, callbackSuccess, callbackError, from) {
    //console.log('senddata from: ' + from + ' .url: ' + url);
    // callbackSuccess = RedirectInto;
    // callbackError = RedirectInto;
    $.ajax({
        type: type,
        url: url,
        data: data,
        contentType: false,
        processData: false,
        success: function(data) {
            console.log('filesendData: from = ' + from + ' .data = ' + data + ' .url: ' + url);
            //console.dir(data)
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

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m, key, value) {
        vars[key] = value;
    });
    return vars;
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
    //alert(data);
    if (data.context) {
        // data.redirect contains the string URL to redirect to
        var next = getUrlVars()["next"];
        if (next) {
            winref.location.href = next;
        } else {
            winref.location.href = data.context;
        }
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
    } else if (from == 'maintenance_page_all_user_info') {
        data2 = JSON.parse(data);
        console.log(data2)
        maintenance_all_users_info_array = data2;
        $.each(data2.users, function(i, item) {
            console.log(item)
            tmp = maintenance_user_info_fields_base.replace('FirstName', item.first_name).replace('LastName', item.last_name).replace('user_id="2"', 'user_id="' + item.id + '"').replace('user_id="3"', 'user_id="' + item.id + '"').replace('user_id="4"', 'user_id="' + item.id + '"').replace('user_id="5"', 'user_id="' + item.id + '"')
            $('.maintenance-users-list .os-padding .os-viewport .os-content').append(tmp);

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
        $('#amir_error_add_user_modal_' + data.field).append(data.form);

    } else if (from == 'MemberGetToken') {
        data2 = JSON.parse(data);
        console.log('in bind member get token: ' + data2);
        CookieHandler('Authorization', 'Token ' + data2.Token.key);
        /*
            error to be handled
            error: {"readyState":4,"responseText":"{\"detail\":\"Authentication credentials were not provided.\"}","responseJSON":{"detail":"Authentication credentials were not provided."},"status":403,"statusText":"Forbidden"}

        */
    } else if (from == 'MemberCategoryMenuFilter') {
        data2 = JSON.parse(data);
        console.log('in bind member category menu filter: ');
        //table = $('#idDocRecords');
        $('#idDocRecords .rowLink').remove();
        member_panel_documents_array = data2.DocCats;
        tmp = member_panel_documents_table_row;
        $.each(member_panel_documents_array, function(i, item) {
            console.log(item)
            tmp = tmp.replace('Document_Date', item.date).replace('Document_Title', item.title).replace('Document_Supervisor', item.prefix + ' ' + item.supervisor);
        });
        $('#idDocRecords').append(tmp);
        console.dir(data2);
    } else if (from == 'MemberCategorySubmenuFilter') {
        $('#idDocRecords .rowLink').remove();
        data2 = JSON.parse(data);
        member_panel_documents_array = data2.DocCats;
        tmp = member_panel_documents_table_row;
        $.each(member_panel_documents_array, function(i, item) {
            console.log(item)
            tmp = tmp.replace('Document_Date', item.date).replace('Document_Title', item.title).replace('Document_Supervisor', item.prefix + ' ' + item.supervisor).replace('praxo_doc_id', item.id);
        });
        $('#idDocRecords').append(tmp);
        //console.dir(data2);
    } else if (from == 'MemberAddNewDocumentsModalForm') {
        //data2 = JSON.parse(data);
        console.log('in bind member MemberAddNewDocumentsModalForm: ' + data);
        for (var p of data) {
            console.log(p);
        }
        //console.dir(data2);
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
    } else if (from == 'Chat') {
        console.dir('from Chat: ' + data);
        //data2 = JSON.parse(data);
        //console.log('from Chat: ' + data2);
        time = luxon.DateTime.fromISO(data.sent);
        //time = DateTime.fromISO(this.props.message.sent)
        time = time.toFormat("HH ':' mm  ");
        tmp = chat_talk_main_member_bubble.replace('BUBBLE-TEXT', data.text).replace('BUBBLE-TIME', time);
        $('.talk-base .os-padding .os-viewport .os-content').append(tmp);

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
            tmp = tmp.replace("<div class='expander'></div>", "<div class='expander'><span class='icon-right'></span></div>").replace('submit2', 'submenu');
        }
        var res = tmp;
        $('#ajax_category').append(res);
        var str = "<div class='submenu'>";
        var tmp2 = '';
        $.each(item.sub_menu, function(j, item_2) {
            //console.log('submenu:')
            tmp2 = document_categories_object_to_appendto_submenu.replace("Sonography", item_2.name).replace("parent2", item.name).replace('submenu_value', item_2.name);
            str = str + tmp2;
        });
        res2 = str + "</div>"
        $("#ajax_category .column .main_ajax_" + item.id).after(res2);
    });
};

function ErrorManagement() {};

function MemberSearch(object, type, url, search_text, from) {
    console.log('inMembersearch');
    $('#idResultContainer .result-list .result-item').remove();
    var data = {
        'member_search': search_text
    };
    SendData(type, url, data, Bind, ErrorManagement, 'MemberSearch');
};

function DocumentCategories(type, url) {
    var from = 'DocumentCategories';
    SendData(type, url, '', Bind, ErrorManagement, from);
};

// function for appending the users result into html
function SearchSuccess(data) {
    $('#search-results').html(data);
};

/*function AddNewUserModalLiveChecks(winRef, data, from, type, url) {
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
    });
};
*/
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
        $("#calendar_my_select_edit").children('[value=' + result.event_type + ']').attr('selected', true);
        //$('#calendar_my_select_edit option[value=result.event_type]').attr("selected", "selected");
    });
};

function GetOneDayEvents(day) {
    month_val = $('.calendar-table-header .month-title').attr('value');
    thisday = $(day).find('.date-cell .date-container .date-1');
    month_val += thisday.text().toString();
    data = { 'month_val': month_val };
    url = $('.calendar-table-header .month-title').attr('url');
    SendData("GET", url, data, Bind, ErrorManagement, 'GetOneDayEvents');
};

function Maintenance(winRef, data, from, type, url) {
    $('body').on('click', ".user-base-maintenance", function() {
        console.log('in ideditmodal: ');
        user_id = $(this).attr("user_id");
        console.log('ideditmodal: ' + user_id);
        result = '';
        result = maintenance_all_users_info_array.users.find(user => (user.id == user_id));
        var edit_user_object = $("#edit-user-input-wrapper");
        $('#edit_form').attr('user_id', user_id);
        $('#news-photo-editor-edit').css({ 'background-image': 'url()' });
        edit_user_object.find("input[name='first_name']").val(result.first_name);
        edit_user_object.find("input[name='last_name']").val(result.last_name);
        edit_user_object.find("input[name='email']").val(result.email);
        edit_user_object.find("input[name='birthdate']").val(result.profile_user.birthdate);
        edit_user_object.find("input[name='mobile']").val(result.profile_user.mobile);
        edit_user_object.find("input[name='address']").val(result.address);
        edit_user_object.find("select[name='membership']").val(result.member_user.membership_set);
        console.dir('ideditmodal: ' + result.first_name);
        //$('#calendar_my_select_edit option[value=result.event_type]').attr("selected", "selected");
    });

    $('body').on('click', ".btn-new-doc-container", function() {
        console.log('in idaddusermodal: ');
        var edit_user_object = $("#add-user-input-wrapper");
        $('#news-photo-editor').css({ 'background-image': 'url()' });
        edit_user_object.find("input[name='first_name']").val();
        edit_user_object.find("input[name='last_name']").val();
        edit_user_object.find("input[name='email']").val();
        edit_user_object.find("input[name='birthdate']").val();
        edit_user_object.find("input[name='mobile']").val();
        edit_user_object.find("input[name='address']").val();
        edit_user_object.find("select[name='membership']").val();
        //$('#calendar_my_select_edit option[value=result.event_type]').attr("selected", "selected");
    });

    $('body').on('click', ".user-base-maintenance .user-maintenance-remove", function() {
        console.log('in idremovemodal: ');
        user_id = $(this).attr("user_id");
        result = '';
        result = maintenance_all_users_info_array.users.find(user => (user.id == user_id));
        var remove_user_object = $("#remove-user-input-wrapper");
        $('#remove_form').attr('user_id', user_id);
        //console.log(edit_user_object);
        remove_user_object.find("span[name='first_name']").text(result.first_name);
        remove_user_object.find("span[name='last_name']").text(result.last_name);
        remove_user_object.find("span[name='email']").text(result.email);
        remove_user_object.find("span[name='birthdate']").text(result.profile_user.birthdate);
        remove_user_object.find("span[name='mobile']").text(result.profile_user.mobile);
        remove_user_object.find("span[name='address']").text(result.address);
        remove_user_object.find("span[name='membership']").text(result.member_user.membership_set);
        console.dir('ideditmodal: ' + result.first_name);
        //$('#calendar_my_select_edit option[value=result.event_type]').attr("selected", "selected");
    });

    $('#edit_form').submit(function(event) {
        // do stuff
        event.preventDefault();
        var fd = new FormData();
        var edit_form = $('#edit_form .custom-input :input');
        console.log($(edit_form));
        $(edit_form).each(function(index) {
            //console.log('here');
            console.log($(this).attr('name'));
            console.log($(this).val());
            fd.append($(this).attr('name'), $(this).val());
        });
        fd.append('user_id', $(this).attr('user_id'));
        var photo = document.getElementById('files2');
        fd.append('photo_name', photo.files[0].name);
        fd.append('photo', photo.files[0]);
        console.log('editUserSubmmit: ');
        console.log(fd.entries());
        console.log(fd.get('first_name'));
        for (var p of fd) {
            console.log(p);
        }
        fileSendData("POST", $(this).attr('action'), fd, Bind, ErrorManagement, 'MaintenanceEditUserModalForm');
        $('#news-photo-editor').css({ 'background-image': 'url()' });
        return false;
    });

    $('body').on('click', "#remove_form", function() {
        console.log('in ideditmodal: ');
        user_id = $(this).attr("user_id");
        var fd = new FormData();
        fd.append("user_id", user_id);
        console.log('remove submit: ' + user_id);
        fileSendData("POST", $(this).attr('action'), fd, Bind, ErrorManagement, 'MaintenanceRemoveUserModalForm');
        //$('#calendar_my_select_edit option[value=result.event_type]').attr("selected", "selected");
    });
}

function Member(winRef, data, from, type, url) {
    var sessionid = Cookies.get('sessionid');
    CookieHandler('sessionid', sessionid);
    SendData("GET", url_to_get_token, '', Bind, ErrorManagement, 'MemberGetToken');
    $('body').on('keyup', "#idSearchBoxMember", function() {
        //search_text = $(this).val();
        MemberSearch("#idResultContainer", "GET", '/member/search/', $(this).val(), 'Member');
    });

    $('body').on('click', "#ajax_category .column .main", function() {
        $('.doc-header .doc-header-title').text($(this).find('.title').text().toString())
        cat_type = $(this).attr('submit_or_submenu');
        console.log('in member ajax category click: ' + cat_type);
        if (cat_type == 'submit2') {
            title = $(this).find('.title').text().toString();
            data = { 'sub_or_not': 'menu', 'title': title }
            SendData("POST", url_document_filter, data, Bind, ErrorManagement, 'MemberCategoryMenuFilter');
        } else { $('.doc-header .doc-header-title').text($(this).find('.title').text().toString()); }
    });

    $('body').on('click', "#ajax_category .column .submenu .item", function() {
        console.log('in member ajax submenu category click: ' + $(this).attr('parent'));
        cat_type = $(this).attr('item_type');
        $('.doc-header .doc-header-title').text($(this).attr('parent') + '>' + $(this).find('span').attr('value'));
        if (cat_type == 'submenu') {
            title = $(this).find('span').attr('value');
            data = { 'sub_or_not': 'submenu', 'title': title }
            SendData("POST", url_document_filter, data, Bind, ErrorManagement, 'MemberCategorySubmenuFilter');
        } else {}
    });
    $('body').on('click', ".doc-photo-header .edit-doc", function() {
        console.log('in ideditDocModal: ');
        console.log(member_panel_documents_array);
        $('#mydiv-upload-files-container .file-upload-row').remove();
        document_id = $('#idDocRecords .active').attr("document_id");
        console.log(document_id);
        result = '';
        result = member_panel_documents_array.find(doc => (doc.id == document_id));
        console.log(result);
        var edit_document_object = $("#idNewDoc .doc-input-container .custom-input");
        //$('#remove_form').attr('user_id', user_id);
        //console.log(edit_user_object);
        edit_document_object.find("input[name='date']").val(result.date);
        edit_document_object.find("input[name='title']").val(result.title);
        edit_document_object.find("input[name='supervisor']").val(result.supervisor);
        edit_document_object.find("input[name='site']").val(result.site);
        // File Images of Documents should be placed
        // $.each(names, function(i, item) {
        //     console.log(item);
        //     tmp = member_panel_editoradd_document_modal_photos_info.replace('FileName', item.name).replace('FileSize', item.size);
        //     $('#mydiv-upload-files-container').append(tmp);
        //     // $(obj).find('.file-upload-name span').text(item.name)
        //     // $(obj).find('.file-upload-size').text(item.name)
        // });
        console.dir('ideditmodal: ' + result.supervisor);
        //$('#calendar_my_select_edit option[value=result.event_type]').attr("selected", "selected");
    });

    $('body').on('click', ".btn-new-doc ", function() {
        console.log('in idAddDocModal: ');
        $('#mydiv-upload-files-container .file-upload-row').remove();
        var edit_document_object = $("#idNewDoc .doc-input-container .custom-input");
        //$('#remove_form').attr('user_id', user_id);
        //console.log(edit_user_object);
        edit_document_object.find("input[name='date']").val('');
        edit_document_object.find("input[name='title']").val('');
        edit_document_object.find("input[name='supervisor']").val('');
        edit_document_object.find("input[name='site']").val('');

        // File Images of Documents should be placed
        // $.each(names, function(i, item) {
        //     console.log(item);
        //     tmp = member_panel_editoradd_document_modal_photos_info.replace('FileName', item.name).replace('FileSize', item.size);
        //     $('#mydiv-upload-files-container').append(tmp);
        //     // $(obj).find('.file-upload-name span').text(item.name)
        //     // $(obj).find('.file-upload-size').text(item.name)
        // });
        //console.dir('idaddmodal: ' + result.supervisor);
        //$('#calendar_my_select_edit option[value=result.event_type]').attr("selected", "selected");
    });
    $('#AddNewDoc').submit(function(event) {
        // do stuff
        console.log('AddDocumentSubmmit: ');
        event.preventDefault();
        var fd = new FormData();
        var edit_form = $(this).find('.custom-input :input');
        console.log($(edit_form));
        $(edit_form).each(function(index) {
            //console.log('here');
            console.log($(this).attr('name'));
            console.log($(this).val());
            fd.append($(this).attr('name'), $(this).val());
        });
        var photo = document.getElementById('files');
        fd.append('files', photo.files);
        $.each(photo.files, function(i, item) {
            console.log(item);
            fd.append("fileToUpload[]", item);
            fd.append('photo_' + i, photo.files[i]);
            fd.append('photo_' + i + '_name', photo.files[i].name);
        });
        console.log(fd.entries());
        console.log(fd.get('title'));
        for (var p of fd) {
            console.log(p);
        }
        fileSendData("POST", $(this).attr('action'), fd, Bind, ErrorManagement, 'MemberAddNewDocumentsModalForm');
        return false;
    });
    $('body').on('click', ".doc-photo-header .remove-doc", function() {
        console.log('in idremoveDocModal: ');
        console.log(member_panel_documents_array);
        document_id = $('#idDocRecords .active').attr("document_id");
        console.log(document_id);
        // result = '';
        // result = member_panel_documents_array.find(doc => (doc.id == document_id));
        // console.log(result);
        $(".ok-btn-container ").click(function() {
            //SendData("POST", url_document_filter, data, Bind, ErrorManagement, 'MemberCategorySubmenuFilter');
        });
    });

    $('body').on('click', ".submit-change-photo .text-submit-btn-container", function() {
        console.log('submited');
        //var inputFiles = $('#personal_photo_change').files;
        var inputFiles = [member_personal_image_file_temp];
        console.log(inputFiles);
        if (inputFiles == undefined || inputFiles.length == 0) return;
        else {
            preview = $('.info .container .photo-container .photo');
            console.log(preview);
            var inputFile = inputFiles[0];
            var reader = new FileReader();
            reader.onload = function(event) {
                //alert("I AM result: " + event.target.result);
                content = event.target.result;
                maintenance_add_user_photo = content;
                // $('#news-photo-editor, #news-photo-editor_edit').css({ 'background-image': 'url(' + content + ')' });
                $(preview).css({ 'background-image': 'url(' + content + ')' });
                // $(this).closest('#news-photo-editor').css({ 'background-image': 'url(' + event.target.result + ')' });
                //img.title = '' + escape(theFile.name);
                //$(this).closest('.news-photo-editor').append(img);
            };
            reader.onerror = function(event) {
                alert("I AM ERROR: " + event.target.error.code);
            };
            reader.readAsDataURL(inputFile);
        }
    });

    $("#files").change(function() {
        console.log('input');
        var names = [];
        for (var i = 0; i < $(this).get(0).files.length; ++i) {
            data = { 'name': $(this).get(0).files[i].name, 'size': $(this).get(0).files[i].size };
            names.push(data);
        }
        console.dir(names);
        // var obj = $('.file-upload-row');
        $.each(names, function(i, item) {
            console.log(item);
            tmp = member_panel_editoradd_document_modal_photos_info.replace('FileName', item.name).replace('FileSize', item.size);
            $('#mydiv-upload-files-container').append(tmp);
            // $(obj).find('.file-upload-name span').text(item.name)
            // $(obj).find('.file-upload-size').text(item.name)
        });
    });

}

function Chat(winRef, data, from, type, url) {
    const socket = io('ws://192.168.30.98:3300/chatroom', {
        transports: ["websocket"],
        query: "userId=" + "5b90f6ba060cce44848daefb"
    });
    socket.on("connect", function() {
        console.log("conected");
    });
    // socket.on('event', function (data) { console.log('connected:', data) });
    socket.on('chat', function(data) {
        console.log('message recieve on chat event: ' + data);
        console.dir(data);
        Bind(window, data, 'Chat');

    });
    socket.on('disconnect', function() {

    });
}
// function calendar_find(specific_array, property_to_check, value_to_check) {
//     return specific_array.id === value_to_check;
// }

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