var csrftoken = Cookies.get('csrftoken');
// function CookieHandler(one, two) {
//     console.log('CookieHandler: ' + two);
//     var csrftoken = Cookies.get('csrftoken');
//     $.ajaxSetup({
//         beforeSend: function(xhr, settings) {
//             xhr.setRequestHeader(one, two);
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//     });
// }

function CsrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

function getCSRFToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

function getUserToken(from = ''){
    if(from == 'getUserToken'){
        //data2 = JSON.parse(data);
        console.log('in bind getUserToken get token: ' + data);
        return data.Token.key;
    }
    else{
        data = SendData("GET", url_to_get_token, '', getUserToken, ErrorManagement, 'getUserToken', '');
        //data2 = JSON.parse(data);
        console.log('in bind getUserToken gettoken2 : ' + data);
        return data.Token.key;   
    }
}


class PrivateTokenVariable {

  constructor(width, height) {
    this._user_token = width;
    this._django_csrf = height;
  }

  get token() {
    return this._user_token;
  }
}

const my_var = new PrivateTokenVariable(user_token, getCSRFToken())

function SendData(type, url, data, callbackSuccess, callbackError, from, data_to_send_next_function) {
    //console.log('senddata from: ' + from + ' .url: ' + url);
    // callbackSuccess = RedirectInto;
    // callbackError = RedirectInto;
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!CsrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
                //xhr.setRequestHeader("Content-Type", 'application/json');
            }
            BeforeSend(window, data, from, url);
        },
        complete: function() {
            // Handle the complete event
            setTimeout(AfterSend(window, data, from, url), 8000);
            //AfterSend(window, data, from, url);
        }

    });
    $.ajax({
        type: type,
        url: url,
        data: data,
        // beforeSend: function(data, xhr) {

        // },
        success: function(data) {
            console.log('sendData: from = ' + from + 'data = ' + data + 'url: ' + url)
            console.dir(data)
            callbackSuccess(window, data, from, data_to_send_next_function);
            return data;
        },
        error: function(data) {
            console.log('error: ' + JSON.stringify(data));
            callbackError(window, data, from);
        }

    });
};

function fileSendData(type, url, data, callbackSuccess, callbackError, from, contentType = false) {
    //console.log('senddata from: ' + from + ' .url: ' + url);
    // callbackSuccess = RedirectInto;
    // callbackError = RedirectInto;
    //var csrftoken = Cookies.get('csrftoken');
    console.log('filesendData: from = ' + from + ' .data = ' + data + ' .url: ' + url + ' .contentType ' + contentType);
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!CsrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
                //xhr.setRequestHeader("Content-Type", 'application/json');
            }
            BeforeSend(window, data, from, url);
        },
        complete: function() {
            // Handle the complete event
            AfterSend(window, data, from, url);
        }
    });
    $.ajax({
        type: type,
        url: url,
        data: data,
        contentType: contentType,
        processData: false,
        success: function(data) {
            console.log('filesendData: from = ' + from + ' .data = ' + data + ' .url: ' + url);
            console.dir(data)
            callbackSuccess(window, data, from, '');
        },
        error: function(data) {
            console.log('filesendData: from = ' + from + ' .data = ' + data + ' .url: ' + url + ' .contentType ' + contentType);
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
        SendData(type, url, data, RedirectInto, ErrorManagement, 'Login', ''); // Pass the variables here as a parameter     
    } else {
        $("#empty").show();
    } // pop ups 
};

function Lang() {
    Language = $('#idHeaderLangContainer span').text();
    Language = Language.replace(' ', '');
    if (Language == 'FA') {
        RTL = true;
    } else {
        RTL = false;
    }
    return;
}

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

function Bind(winref, data, from, data_from_last_function) {
    Lang()
    console.log('in Bind, from = ' + from);
    //data2 = JSON.parse(data);
    console.log('in Bind, Data: ');
    //console.log('in Bind : '+ data2.DocCats[0].sub_menu);
    if (from == 'MemberSearch') {
        data2 = JSON.parse(data);
        search_result = data2.users;
        $.each(data2.users, function(i, item) {
            //console.log('in Bind2 : '+ data2.users[0].username);
            //str = "<div class='result-item'><div class='photo-container'><div class='photo'></div></div><div class='detail'><span class='name'> first_name last_name </span><span class='position'>Title/Position</span></div></div>"
            res = search_object_to_append.replace("first_name_text", item.user.first_name).replace("last_name_text", item.user.last_name).replace('USER_ID', item.user.id).replace('USER_FIRST_NAME', item.user.first_name).replace('USER_LAST_NAME', item.user.last_name).replace('USER_AGE', 288).replace('USER_EXPERTISE', item.expertise).replace('USER_PREFIX', item.prefix).replace('USER_MEMBERSHIP', item.membership_set + ' Membership').replace('USER_GENDER', 'مذکرررر').replace('__UUID', item.uuid);
            //$('#idResultContainer .result-list').append("<div class='result-item'><div class='photo-container'><div class='photo'></div></div><div class='detail'><span class='name'>" + item.first_name + ' ' + item.last_name +"</span><span class='position'>Title/Position</span></div></div>");
            $('#idResultContainer .result-list').append(res);
        });
    } else if (from == 'maintenance_page_all_user_info') {
        data2 = JSON.parse(data);
        console.log(data2)
        maintenance_all_users_info_array = data2;
        $.each(data2.users, function(i, item) {
            console.log(item)
            tmp = maintenance_user_info_fields_base.replace('FirstName', item.first_name).replace('LastName', item.last_name).replace('user_id="2"', 'user_id="' + item.uuid + '"').replace('user_id="3"', 'user_id="' + item.uuid + '"').replace('user_id="4"', 'user_id="' + item.uuid + '"').replace('user_id="5"', 'user_id="' + item.uuid + '"')
            $('.maintenance-users-list .os-padding .os-viewport .os-content').append(tmp);
            data = {'user_uuid': item.uuid}
            data_for_next_function = {'user_id': item.uuid}
            SendData("POST", 'http://praxo.ir/getuserpic/' , data, Bind, ErrorManagement, 'MaintenanceUsersListPics', data_for_next_function);
        });
    } else if (from == 'MaintenanceUsersListPics') {
        console.log('in  MaintenanceUsersListPics: ');
        if(null == data.user_uuid){
            object = $('.user-maintenance-photo-container[user_id = ' + data_from_last_function.user_id + '] .user-maintenance-photo').css('background-image', 'url(' + data.user_picture + ')');
        }
        else{
            object = $('.user-maintenance-photo-container[user_id = ' + data.user_uuid + '] .user-maintenance-photo').css('background-image', 'url(' + data.user_picture + ')');
        }
    } else if (from == 'ChatUsersListPics') {
        console.log('in  ChatUsersListPics: ');
        if(null == data.user_uuid){
            object = $('.user-chat[user_id = ' + data_from_last_function.user_uuid + '] .photo-container-user-chat .photo-user-chat').css('background-image', 'url(' + data.user_picture + ')');
        }
        else{
            object = $('.user-chat[user_id = ' + data.user_uuid + '] .photo-container-user-chat .photo-user-chat').css('background-image', 'url(' + data.user_picture + ')');
        }
        
    } else if (from == 'ChatRoomsListPics') {
        console.log('in  ChatRoomsListPics: ');
        if(null == data.user_uuid){
            console.log(data_from_last_function.user_uuid);
            object = $('.user-chat[room_id = ' + data_from_last_function.user_uuid + '] .photo-container-user-chat .photo-user-chat').css('background-image', 'url(' + data.user_picture + ')');
        }
        else{
            object = $('.user-chat[room_id = ' + data.user_uuid + '] .photo-container-user-chat .photo-user-chat').css('background-image', 'url(' + data.user_picture + ')');
        }
        
    } else if (from == 'DocumentCategories') {
        data2 = JSON.parse(data);
        //var object = $('.member-menu .overlay-scroll');
        object = $('.search-result-wrapper .search-result-panel .search .container .label').text();

        if (object == 'جستجو') {
            CreateDocumentCategoryMenuRTL(data2.DocCats);
        } else { CreateDocumentCategoryMenu(data2.DocCats); }
        // $('#ajax_category').append(res);Calendar
    } else if (from == 'AddNewUserModalLiveChecks') {
        console.log('in Bind, from = ' + from);
        console.dir(data.field);
        //data2 = JSON.parse(data);
        $('#amir_error_add_user_modal_' + data.field).append(data.form);

    } else if (from == 'MemberGetToken') {
        data2 = JSON.parse(data);
        console.log('in bind member get token: ' + data2);
        // const winref.private_token = new PrivateTokenVariable(data2.Token.key, csrftoken);
        // console.log(winref.private_token.token); 
        //CookieHandler('Authorization', 'Token ' + data2.Token.key);
        /*
            error to be handled
            error: {"readyState":4,"responseText":"{\"detail\":\"Authentication credentials were not provided.\"}","responseJSON":{"detail":"Authentication credentials were not provided."},"status":403,"statusText":"Forbidden"}

        */
    } else if (from == 'MemberCategoryMenuFilter') {
        data2 = JSON.parse(data);
        console.log('in bind member category menu filter: ');
        //table = $('#idDocRecords');
        $('#idDocRecords .rowLink').remove();
        $('#MemberPanelDocumentDetail').show();
        $('#MemberDetailHistory').hide();
        // $('.plane-search-wrapper').after(data.form);
        member_panel_documents_array = data2.DocCats;
        tmp = member_panel_documents_table_row;
        $.each(member_panel_documents_array, function(i, item) {
            console.log(item)
            tmp = tmp.replace('Document_Date', item.date).replace('Document_Title', item.title).replace('Document_Supervisor', item.prefix + ' ' + item.supervisor).replace('praxo_doc_id', item.id);
            $('#idDocRecords').append(tmp);
        });
        
        // console.dir(data2);

    } else if (from == 'MemberCategoryMenuHistoryPageFilter') {
        //data2 = JSON.parse(data);
        console.log('in MemberCategoryMenuHistoryPageFilter: ');
        //$(".docs-main").remove();
        $('#MemberPanelDocumentDetail').hide();
        $('#MemberDetailHistory').show();
        //$('.plane-search-wrapper').after(data.form);

    } else if (from == 'MemberCategorySubmenuFilter') {
        $('#idDocRecords .rowLink').remove();
        data2 = JSON.parse(data);
        member_panel_documents_array = data2.DocCats;
        tmp = member_panel_documents_table_row;
        document_uuid = 0
        $.each(member_panel_documents_array, function(i, item) {
            console.log(item)
            if(i == 0){
                document_uuid = item.uuid;
            }
            tmp = tmp.replace('Document_Date', item.date).replace('Document_Title', item.title).replace('Document_Supervisor', item.prefix + ' ' + item.supervisor).replace('praxo_doc_id', item.id).replace('_DOCUMENTUUID', item.uuid);
            $('#idDocRecords').append(tmp);
        });
        $('#MemberPanelDocumentDetail').show();
        $('#MemberDetailHistory').hide();
        user_uuid = $('.detail-container').attr('uuid');
        data = {'name': '0', 'all':'1', 'user_uuid': user_uuid, 'doc_uuid': document_uuid}
        console.log('in MemberCategorySubmenuFilter' + data + ' , ' + document_uuid);
        $( "#idDocRecords .rowLink" ).first().addClass('active');
        SendData("POST", 'http://praxo.ir/patientdoc/getdocumentpic/' , data, Bind, ErrorManagement, 'Document_Picture', '');
        //console.dir(data2);
    } else if (from == 'Document_Picture') {
        $('.doc-photo .doc-carousel ').slick('unslick');
        tmp = document_picture_carousel
        console.dir('in Document_Picture ' + data);
        tmp = tmp.replace('_DOCUMENT_PICTURE', '' + data[0].picture)
        $('.carousel-cell').remove();
        $.each(data, function(i, item) {
            tmp = document_picture_carousel.replace('_DOCUMENT_PICTURE', item.picture);
            $('.doc-carousel').append(tmp);
        });
        console.log(tmp);
        $.each($('.carousel-cell'), function(i, item) {
            $(item).css('background-image', data[i].picture);
        });
        // $('.doc-carousel').append(tmp);
        // $('.doc-carousel').append(tmp);
        // $('.doc-carousel').append(tmp);
        // $('.doc-carousel').append(tmp);
        // $('.doc-carousel').append(tmp);
        $('.doc-carousel').slick({
            lazyLoad: 'ondemand', // ondemand progressive anticipated
            dots: true,
        });
        var docCarouselHeight = $('.doc-carousel').height();
        var docCarouselWidth = $('.doc-carousel').width();
        $('.slick-track').css('width', docCarouselWidth);
        $('.carousel-cell').css('max-height', docCarouselHeight + 'px');
        $('.carousel-amir-img').css('min-height', docCarouselHeight + 'px');
        $('.carousel-amir-img').css('min-width', docCarouselWidth + 'px');
        
    } else if (from == 'MemberAddNewDocumentsModalForm') {
        //data2 = JSON.parse(data);
        console.log('in bind member MemberAddNewDocumentsModalForm: ' + data);
        console.dir(data);
        //console.dir(data2);
    } else if (from == 'MaintenanceAddUserModalForm') {
        //data2 = JSON.parse(data);
        $('#amir_error_add_user_modal_email').append(data.form)
    } else if (from == 'EditUserModalLiveChecks') {
        
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
        // Check
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
        lang_code = $('#idHeaderLangContainer .lang-name').attr('lang_code');
        console.log(lang_code);
        link = $(document).find('.calendar-wrapper #calendar_next_month').attr('month_link');
        console.log(link);
        $(document).find('.calendar-wrapper #calendar_next_month').attr('month_link', '/' + lang_code + link);
        link2 = $(document).find('.calendar-wrapper #calendar_prev_month').attr('month_link');
        console.log(link2);
        $(document).find('.calendar-wrapper #calendar_prev_month').attr('month_link', '/' + lang_code + link2);
        text = $('.header-event-list .date-header-event-list').attr('event_panel_title')+' '+$('.amir_calendar_month tbody tr .active .date-cell .date-container .date-1').text()
        $('.header-event-list .date-header-event-list').text(text)

        text = $(document).find('.header-event-list .date-header-event-list').attr('event_panel_title')+' '+$(document).find('.amir_calendar_month tbody tr .active .date-cell .date-container .date-1').text()
        $(document).find('.header-event-list .date-header-event-list').text(text)

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
        //console.log(events_of_current_day_array.events[0].id);
        html = '';
        $.each(data2.events, function(i, item) {
            start_time = luxon.DateTime.fromISO(item.start_time);
            end_time = luxon.DateTime.fromISO(item.end_time);
            // start_time = tConvert(item.start_time);
            // end_time = tConvert(item.end_time);
            //console.log(time);
            //time = DateTime.fromISO(this.props.message.sent)
            //time = time.toFormat("h':'mm a");
            //console.log(time);
            start_time = start_time.toFormat("h':'mm a");
            end_time = end_time.toFormat("h':'mm a");
            event_time_range = start_time + '-' + end_time;
            event_detail_html = calendar_after_sidenav_calendar_wrapper.replace('event_time_range', event_time_range).replace('event_note', item.event_note).replace('AmirEventObject', item.id).replace('__EVENTID', item.id);
            html += event_detail_html;
        });
        ob = $('.base-event-list .overlay-scroll .os-padding')
        if(ob.length == 0){
            var instances = $(".base-event-list .overlay-scroll").overlayScrollbars({ }).overlayScrollbars();    
        }
        $('.base-event-list .overlay-scroll .os-padding .os-viewport .os-content .event-detial').remove();
        $('.base-event-list .overlay-scroll .os-padding .os-viewport .os-content').append(html);
        //$('.base-event-list .overlay-scroll .event-detial').remove();
        // var object = $('.base-event-list .overlay-scroll').append(html);
    } else if (from == 'Chat') {
        console.dir('from Chat: ' + data);
        //data2 = JSON.parse(data);
        //console.log('from Chat: ' + data2);
        time = luxon.DateTime.fromISO(data.sent);
        //time = DateTime.fromISO(this.props.message.sent)
        time = time.toFormat("h':'mm a");

        if (data.user == user_id) {
            tmp = chat_talk_main_sent_bubble.replace('BUBBLE-TEXT', data.text).replace('BUBBLE-TIME', time);
        } else {
            tmp = chat_talk_main_received_bubble.replace('BUBBLE-TEXT', data.text).replace('BUBBLE-TIME', time);
        }
        $('.talk-base .os-padding .os-viewport .os-content .talk-inside-container').append(tmp);
        console.log(chat_scrollbar);
        var newChatHeight = $('.talk-inside-container > .received-bubble').last().height() - 1;
        console.log(newChatHeight);
        chat_scrollbar.scroll({ y: "+=" + newChatHeight + "px" }, 500);
        chat_scrollbar.scroll({ y: "100%" }, 500);

    } else if (from == 'AddMemberUserHistory') {
        console.log('in bind AddMemberUserHistory: ' + data);

    } else if (from == 'HistoryCategory') {
        console.log('in bind HistoryCategory: ' + data);
        data2 = JSON.parse(data);
        $.each(data2.data, function(i, item) {
            tmp = ''
            if (!RTL) {
                tmp = member_history_document_section.replace('_HISTORY_CATEGORY_TITLE', item.name);
            } else { 
                tmp = member_history_document_section.replace('_HISTORY_CATEGORY_TITLE', item.rtl_name); 
            }
            tmp = tmp.replace('_HISTORY_CATEGORY_ID', item.id)
            //tmp = tmp.replace('_HISTORY_CATEGORY_CONTEXT', '');
            $('.doc-medic-history .os-padding .os-viewport .os-content').append(tmp);
                
        });
    } else if (from == 'GetUserHistory') {
        console.log('in bind GetUserHistory: ' + data);
        data2 = JSON.parse(data);
        var object = $('.doc-medic-history .os-padding .os-viewport .os-content');
        $.each(data2.data, function(i, item) {
            $.each(item.patient_histories, function(i1, item1) {
                if(item1.user_created_first_name == $('.info .container .detail-container').attr('first_name')){
                    $(object).find('.history-section[history_category_id = ' + item.id.toString() + '] .section-content-container').text('');
                    $(object).find('.history-section[history_category_id = ' + item.id.toString() + '] .section-content-container').append(item1.context);
                }
            });
        });
    } else if (from == 'OnclickEditDocModal') {
        console.log('in OnclickEditDocModal: ');
        object = $('.upload-files-container .overlay-scroll .os-padding .os-viewport .os-content #mydiv-edit-upload-files-container');
        $.each(data, function(i, item) {
            res = previously_uploaded_document_pictures.replace("_FILENAME", item.name).replace("_FILESIZE", item.size);
            $(object).append(res);
        });
    } else if (from == 'OnclickUserGetUserPic') {
        console.log('in OnclickUserGetUserPic: ');
        object = $('#news-photo-editor-edit').css('background-image', 'url(' + data.user_picture + ')');
        // $.each(data, function(i, item) {
        //     res = previously_uploaded_document_pictures.replace("_FILENAME", item.name).replace("_FILESIZE", item.size);
        //     $(object).append(res);
        // });
        
    } else if (from == 'GetAllNews') {
        console.log('in GetAllNews: ');
        data2 = JSON.parse(data);
        news_array = data2.data;
        $.each(data2.data, function(i, item) {
            time = luxon.DateTime.fromISO(item.created_at);
            time = time.toFormat("yyyy LLL dd '|' h':'mm a");
            res = news_objects_in_news_wrapper.replace("__NEWS_ID", item.id).replace("__NEWS_TITLE", item.title).replace('__NEWS_DATE', time).replace('__NEWS_DESCRIPTION', item.description);
            $('.base-news-list .os-padding .os-viewport .os-content').append(res);
            
        });
        //object = $('#news-photo-editor-edit').css('background-image', 'url(' + data.user_picture + ')');
        
    } else {
        console.log("from doesn't match");
    };
}

function CreateDocumentCategoryMenu(data) {
    //console.log('CreateDocumentCategoryMenu:' + data);
    $.each(data, function(i, item) {
        var tmp = document_categories_object_to_append.replace("main_ajax_id", "main_ajax_" + item.id).replace('_MENUIDENTIFIER', item.id).replace("icon_name", item.icon_name).replace("classTitle", item.name).replace('_ICONNAME', item.icon_name).replace('_COLUMNINDEX', item.index);
        if (item.index == document_category_active_handler._column_index) {
            tmp = tmp.replace("column", "column active");
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
            tmp2 = document_categories_object_to_appendto_submenu.replace("Sonography", item_2.name).replace("parent2", item.name).replace("parent3", item.name).replace('_SUBMENUIDENTIFIER', item_2.id).replace('submenu_value', item_2.name).replace('_ICONNAME', item.icon_name).replace('_ITEMINDEX', item_2.index);
            if (item_2.index == document_category_active_handler._column_index) {
                tmp = tmp.replace("item", "item active")
            }
            str = str + tmp2;
        });
        res2 = str + "</div>"
        $("#ajax_category .column .main_ajax_" + item.id).after(res2);
    });
};

function CreateDocumentCategoryMenuRTL(data) {
    //console.log('CreateDocumentCategoryMenu:' + data);
    $.each(data, function(i, item) {
        var tmp = document_categories_object_to_append.replace("main_ajax_id", "main_ajax_" + item.id).replace('_MENUIDENTIFIER', item.id).replace("icon_name", item.icon_name).replace("classTitle", item.rtl_name).replace('_ICONNAME', item.icon_name).replace('_COLUMNINDEX', item.index);
        if (item.index == document_category_active_handler._column_index) {
            tmp = tmp.replace("column", "column active")
        }
        //console.log('submenu length: '+ item.sub_menu.length);
        if (item.sub_menu.length != 0) {
            tmp = tmp.replace("<div class='expander'></div>", "<div class='expander'><span class='icon-left'></span></div>").replace('submit2', 'submenu');
        }
        var res = tmp;
        $('#ajax_category').append(res);
        var str = "<div class='submenu'>";
        var tmp2 = '';
        $.each(item.sub_menu, function(j, item_2) {
            //console.log('submenu:')
            tmp2 = document_categories_object_to_appendto_submenu.replace("Sonography", item_2.rtl_name).replace("parent2", item.rtl_name).replace("parent3", item.name).replace('_SUBMENUIDENTIFIER', item_2.id).replace('submenu_value', item_2.rtl_name).replace('_ICONNAME', item.icon_name).replace('_ITEMINDEX', item_2.index);
            if (item_2.index == document_category_active_handler._column_index) {
                tmp = tmp.replace("item", "item active")
            }
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
    SendData(type, url, data, Bind, ErrorManagement, 'MemberSearch', '');
};

function DocumentCategories(type, url) {
    var from = 'DocumentCategories';
    SendData(type, url, '', Bind, ErrorManagement, from, '');
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
        SendData("POST", '/member/edituser/', tmp, Bind, ErrorManagement, 'EditUserModalLiveChecks', '');
    } else if (from == 'page') {
        console.dir(data)
        SendData("POST", '/member/oneuserinfo/', data, EditUserModalLiveChecks, ErrorManagement, 'EditUserModalLiveChecks', '');
    }
};

function RemoveUserModalLiveChecks(winRef, data, from, type, url) {
    if (from == 'RemoveUserModalLiveChecks') {
        data2 = JSON.parse(data);
        console.dir('in RemoveUserModalLiveChecks, data  = ' + data2.user);
        tmp = { 'user': data2.user, 'id': data2.id }
        console.log(tmp)
        SendData("POST", '/member/removeuser/', tmp, Bind, ErrorManagement, 'RemoveUserModalLiveChecks', '');
    } else if (from == 'page') {
        console.dir(data)
        SendData("POST", '/member/oneuserinfo/', data, RemoveUserModalLiveChecks, ErrorManagement, 'RemoveUserModalLiveChecks', '');
    }
};

function Calendar(winRef, data, from, type, url) {
    $('body').on('click', '#calendar_prev_month', function() {
        //$(object).click(function() {
        var link_to_month = $('#calendar_prev_month').attr('month_link');
        lang_code = $('#idHeaderLangContainer .lang-name').attr('lang_code');
        SendData("GET", '/' + lang_code + link_to_month, '', Bind, ErrorManagement, 'Calendar', '');
    });
    $('body').on('click', '#calendar_next_month', function() {
        //$(object).click(function() {
        var link_to_month = $('#calendar_next_month').attr('month_link');
        lang_code = $('#idHeaderLangContainer .lang-name').attr('lang_code');
        SendData("GET", '/' + lang_code + link_to_month, '', Bind, ErrorManagement, 'Calendar', '');
    });

    $('body').on('click', ".calendar-table-base table tbody tr td", function() {
        GetOneDayEvents($(this));
        $(".calendar-table-base table tbody tr td").removeClass("active");
        $(this).addClass("active");
        text = $('.header-event-list .date-header-event-list').attr('event_panel_title')+' '+$(this).find('.date-cell .date-container .date-1').text()
        $('.header-event-list .date-header-event-list').text(text)
    });
    $('body').on('click', ".base-event-list .overlay-scroll .event-detial .edit-event-detail-btn", function() {
        event_id = $(".base-event-list .overlay-scroll .event-detial .edit-event-detail-btn").attr("event_object");
        result = '';
        result = events_of_current_day_array.events.find(event => (event.id == event_id));
        $('#calendar_input_event_type_edit').val(result.event_type);
        $('#calendar_input_title_edit').val('amir');
        $('#calendar_input_start_time_edit').val(result.start_time);
        $('#calendar_input_end_time_edit').val(result.end_time);
        $('#calendar_text_event_note_edit').val(result.event_note);
        //In case eventy types input was select input --> $("#calendar_my_select_edit").children('[value=' + result.event_type + ']').attr('selected', true);
        //$('#calendar_my_select_edit option[value=result.event_type]').attr("selected", "selected");
    });

    $('body').on('click', ".base-event-list .overlay-scroll .os-padding .os-viewport .os-content .event-detail", function() {
        event_id = $(this).attr("event_id");
        result = '';
        object = $('.show-event-header-text');
        $(object).find('.show-event-date').text($('.date-header-event-list').text());
        result = events_of_current_day_array.events.find(event => (event.id == event_id));
        object = $('.show-event-base .show-event-base-container');
        $(object).find('.show-event-title').text(result.event_title);
        $(object).find('p').text(result.event_note);
        //In case eventy types input was select input --> $("#calendar_my_select_edit").children('[value=' + result.event_type + ']').attr('selected', true);
        //$('#calendar_my_select_edit option[value=result.event_type]').attr("selected", "selected");
    });

    $('#AddEventForm').submit(function(event) {
        // do stuff
        console.log('AddEventForm: ');
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
        //fd.append('user_id', $('.detail-container').attr('user_id'));
        fd.append('event_note', $(this).find('.custom-textarea .textarea-box textarea').val());
        fd.append('user_id', 3);
        day = $(".calendar-table-base table tbody tr .active .date-cell .date-container .date-1").text();
        date = $('.header-event-list .date-header-event-list').attr('value');
        fd.append('date', date + day);
        language = $('#idHeaderLangContainer .lang-name').attr('lang_code')
        fd.append('language', language);
        console.log(fd.entries());
        console.log(fd.get('title'));
        for (var p of fd) {
            console.log(p);
        }
        fileSendData("POST", $(this).attr('action'), fd, Bind, ErrorManagement, 'CalendarAddEventForm');
        return false;
    });
};

function GetOneDayEvents(day) {
    month_val = $('.calendar-table-header .month-title').attr('value');
    thisday = $(day).find('.date-cell .date-container .date-1');
    month_val += thisday.text().toString();
    data = { 'month_val': month_val };
    url = $('.calendar-table-header .month-title').attr('url');
    tmp = url.split('/');
    if(tmp[1]=='en' || tmp[1]=='fa'){
        url = $('.calendar-table-header .month-title').attr('url');
    }
    else{
        url = $('.calendar-table-header .month-title').attr('url');
        url = '/' + $('#idHeaderLangContainer .lang-name').attr('lang_code') + url
    }
    console.log(url)
    SendData("GET", url, data, Bind, ErrorManagement, 'GetOneDayEvents', '');
};

function Maintenance(winRef, data, from, type, url) {
    $('body').on('click', ".user-base-maintenance", function() {
        console.log('in ideditmodal: ');
        user_id = $(this).attr("user_id");
        console.log('ideditmodal: ' + user_id);
        result = '';
        result = maintenance_all_users_info_array.users.find(user => (user.uuid == user_id));
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
        data = {'user_uuid': user_id}
        SendData("POST", 'http://praxo.ir/getuserpic/' , data, Bind, ErrorManagement, 'OnclickUserGetUserPic', '');
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
        result = maintenance_all_users_info_array.users.find(user => (user.uuid == user_id));
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
        var tmp = document.getElementById('files2');
        if(!tmp.files[0]){
            alert('Please upload one image');
            return false;
        }
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

function ShowHide(show, hide){
    console.log(show);
    console.log(hide);
    $(show).show();
    $(hide).hide();
}

function Member(winRef, data, from, type, url) {
    var sessionid = Cookies.get('sessionid');
    //CookieHandler('sessionid', sessionid);
    SendData("GET", url_to_get_token, '', Bind, ErrorManagement, 'MemberGetToken', '');
    //const member = PrivateTokenVariable(getUserToken('global'), getCSRFToken())
    $('body').on('keyup', "#idSearchBoxMember", function() {
        //search_text = $(this).val();
        MemberSearch("#idResultContainer", "GET", '/member/search/', $(this).val(), 'Member');
    });

    $('body').on('click', ".photo-container .photo", function() {
        $('#changeUserPhotoModalPreview').css("background-image", $(this).css("background-image"));
    });

    $('body').on('click', "#editUserInfoModal", function() {
        $('.header-member-edit .photo-container').css("background-image", $('.photo-container .photo').css("background-image"));
    });

    $('body').on('click', "#idMemberInfo", function() {
        $('.header-member-info .photo-container').css("background-image", $('.photo-container .photo').css("background-image"));
    });

    $('body').on('click', ".rowLink", function() {
        user_uuid = $('.detail-container').attr('uuid');
        document_uuid = $(this).attr('document_uuid');
        data = {'name': '0', 'all':'1', 'user_uuid': user_uuid, 'doc_uuid': document_uuid}
        console.log('in MemberCategorySubmenuFilter' + data + ' , ' + document_uuid);
        $(this).first().addClass('active');
        SendData("POST", 'http://praxo.ir/patientdoc/getdocumentpic/' , data, Bind, ErrorManagement, 'Document_Picture', '');
    });

    $('body').on('click', ".history-section-editor", function() {
        tmp = $(this).parent().next('.section-content-container p')
        tmp1 = $(this).parent().next('.section-content-container *')
        tmp2 = $(this).parent().next('.section-content-container').find('*')
        tmp3 = $(this).parent().next('.section-content-container p')
        tmp4 = $(this).parent().next('.section-content-container p')
        tmp5 = $(this).parent().next('.section-content-container p')
        tmp6 = $(this).parent().next('.section-content-container p')
        tmp7 = $(this).parent().next('.section-content-container p')
        console.log($(this).parent().nextAll('.section-content-container'));
        console.log(tmp);
        console.log(tmp1);
        console.log(tmp2);
        console.log(tmp3);
        $('#historyEditor .os-padding .os-viewport .os-content .ql-editor').text('')
        $('#historyEditor .os-padding .os-viewport .os-content .ql-editor').append(tmp);
    });

    $('body').on('click', ".column", function() {
        console.log('in column show hide icon name: ');
        if($(this).attr('column_index')!=1){
            console.log('in column show hide icon name: !=1');
            document_category_active_handler._panel_id = '#MemberPanelDocumentDetail'
            document_category_active_handler._hide_id = '#MemberDetailHistory'
        }
        else{
            console.log('in column show hide icon name: =1');
            document_category_active_handler._panel_id = '#MemberDetailHistory'
            document_category_active_handler._hide_id = '#MemberPanelDocumentDetail'   
        }
        icon_span = document_category_active_handler.panel_id + ' .member-docs .doc-container .doc-header .doc-header-icon span'
        $(icon_span).removeClass(document_category_active_handler.icon+'fill').addClass($(this).find('.main').attr('icon_tmp')+'fill');
        document_category_active_handler._column_index = $(this).attr('column_index');
        document_category_active_handler._icon_name = $(this).find('.main').attr('icon_tmp');
        
        ShowHide(document_category_active_handler._panel_id, document_category_active_handler._hide_id);
    });

    $('body').on('click', ".item", function() {
        ShowHide(document_category_active_handler._panel_id, document_category_active_handler._hide_id);
    });

    $('body').on('click', "#ajax_category .column .main", function() {
        $('.doc-header .doc-header-title').text($(this).find('.title').text().toString())
        icon_tmp = $(this).attr('icon_tmp');

        cat_type = $(this).attr('submit_or_submenu');
        console.log('in member ajax category click: ' + cat_type);
        if (cat_type == 'submit2') {
            title = $(this).find('.title').text().toString();
            identifier = $(this).attr('menu_identifier');
            if (title == "Member History" || title == "تاریخچه بیمار") {
                user_id = $('.detail-container').attr('user_id');
                data = { 'sub_or_not': 'menu', 'title': title, 'id': identifier, 'user_id': user_id };
                SendData("POST", '/ajax/patientdoc/member/', data, Bind, ErrorManagement, 'MemberCategoryMenuHistoryPageFilter', '');
            } else {
                if (!$('#idDocRecords').length) {
                    //SendData("POST", '/ajax/patientdoc/memberfemale/', data, Bind, ErrorManagement, 'MemberCategoryMenuHistoryPageFilter');
                }
                user_id = $('.detail-container').attr('user_id');
                data = { 'sub_or_not': 'menu', 'title': title, 'id': identifier, 'user_id': user_id };
                SendData("POST", url_document_filter, data, Bind, ErrorManagement, 'MemberCategoryMenuFilter', '');
            }

        } else { $('.doc-header .doc-header-title').text($(this).find('.title').text().toString()); }
    });

    $('body').on('click', "#ajax_category .column .submenu .item", function() {
        console.log('in member ajax submenu category click: ' + $(this).attr('parent'));
        cat_type = $(this).attr('item_type');
        $('.doc-header .doc-header-title').text($(this).attr('parent') + ' > ' + $(this).find('span').attr('value'));
        if (cat_type == 'submenu') {
            if (!$('#idDocRecords').length) {
                //SendData("POST", '/ajax/patientdoc/memberfemale/', data, Bind, ErrorManagement, 'MemberCategoryMenuHistoryPageFilter');
            }

            title = $(this).find('span').attr('value');
            identifier = $(this).find('span').attr('submenu_identifier');
            user_id = $('.detail-container').attr('user_id');
            data = { 'sub_or_not': 'submenu', 'title': title, 'id': identifier, 'user_id': user_id };
            SendData("POST", url_document_filter, data, Bind, ErrorManagement, 'MemberCategorySubmenuFilter', '');
        } else {}
    });
    $('body').on('click', ".doc-photo-header .edit-doc", function() {
        console.log('in ideditDocModal: ');
        console.log(member_panel_documents_array);
        $('#mydiv-edit-upload-files-container .file-upload-row').remove();
        document_id = $('#idDocRecords .active').attr("document_id");
        document_uuid = $('#idDocRecords .active').attr("document_uuid");
        console.log(document_id);
        result = '';
        result = member_panel_documents_array.find(doc => (doc.id == document_id));
        console.log(result);
        var edit_document_object = $("#EditDoc .custom-input");
        //$('#remove_form').attr('user_id', user_id);
        //console.log(edit_user_object);
        edit_document_object.find("input[name='date']").val(result.date);
        edit_document_object.find("input[name='title']").val(result.title);
        edit_document_object.find("input[name='supervisor']").val(result.supervisor);
        edit_document_object.find("input[name='site']").val(result.site);
        user_uuid = $('.detail-container').attr('uuid');
        data = {'name': '0', 'all':'1', 'user_uuid': user_uuid, 'doc_uuid': document_uuid}
        console.log('in MemberCategorySubmenuFilter' + data)
        SendData("POST", 'http://praxo.ir/patientdoc/getdocumentpic/' , data, Bind, ErrorManagement, 'OnclickEditDocModal', '');


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
        fd.append('user_id', $('.detail-container').attr('user_id'));
        var photo = document.getElementById('files');
        fd.append('files', photo.files);
        $.each(photo.files, function(i, item) {
            console.log(item);
            fd.append("fileToUpload[]", item);
            fd.append('photo_' + i, photo.files[i]);
            fd.append('photo_' + i + '_name', photo.files[i].name);
        });
        category_index = $('body').find('#MemberCategoryMenu .os-padding .os-viewport .os-content #ajax_category .active').attr('column_index')
        if(!category_index){
            category_index = 3
        }
        category_index = document_category_active_handler._column_index;
        fd.append('category_index', category_index);
        item_index = -1
        if($('#ajax_category .active .main').attr('submit_or_submenu') == 'submenu'){
            if($('#ajax_category .active .submenu .active').length != 0){
                item_index = $('#ajax_category .active .submenu .active').attr('item_index')   
            }
            else{
                //item_index = $('#ajax_category .active .submenu .item')[0].attr('item_index')      
                item_index = 1
            }
        }
        else{
            item_index = 0
        }
        item_index = document_category_active_handler._item_index;
        fd.append('item_index', item_index);
        console.log(fd.entries());
        console.log(fd.get('title'));
        for (var p of fd) {
            console.log(p);
        }
        fileSendData("POST", $(this).attr('action'), fd, Bind, ErrorManagement, 'MemberAddNewDocumentsModalForm');
        return false;
    });

    $('#EditDoc').submit(function(event) {
        // do stuff
        event.preventDefault();
        console.log('EditDocumentSubmmit: ');
        var fd = new FormData();
        var edit_form = $(this).find('.custom-input :input');
        console.log($(edit_form));
        $(edit_form).each(function(index) {
            //console.log('here');
            console.log($(this).attr('name'));
            console.log($(this).val());
            fd.append($(this).attr('name'), $(this).val());
        });
        fd.append('document_uuid', $('#idDocRecords .rowLink').attr('document_uuid'));
        fd.append('document_id', $('#idDocRecords .rowLink').attr('document_id'));
        fd.append('user_id', $('.detail-container').attr('user_id'));
        var photo = document.getElementById('editFiles');
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

    $('body').on('click', "#editUserInfoModal", function() {
        console.log('in editUserInfoModal onclick: ');
        edit_form = $('#edit_form');
        data2 = result_item_click_user_of_member_page;
        $(edit_form).find("input[name='first_name']").val(data2.user.first_name);
        $(edit_form).find("input[name='last_name']").val(data2.user.last_name);
        $(edit_form).find("input[name='email']").val(data2.user.email);
        $(edit_form).find("input[name='mobile']").val(data2.mobile);
        $(edit_form).find("input[name='address']").val(data2.address);
        //  Check $("#myselect").val(3);
        $(edit_form).find('#member_membership_type_id_edit option[value=' + data2.membership_set + ']').attr('selected', 'selected');;
        $(edit_form).attr('user_id', data2.user.id);
        //console.log(res);
        //$('.detail-container').attr('user_id', $(this).attr('user_id'));
        // // result = '';
        // // result = member_panel_documents_array.find(doc => (doc.id == document_id));
        // // console.log(result);
        // $(".ok-btn-container ").click(function() {
        //     //SendData("POST", url_document_filter, data, Bind, ErrorManagement, 'MemberCategorySubmenuFilter');
        // });
    });

    $('body').on('click', ".detail-container .detail-bold", function() {
        console.log('in UserInfoModal onclick: ');
        object = $('.member-info-content .member-info-content-wrapper');
        data2 = result_item_click_user_of_member_page;
        $(object).find("span[name='first_name']").text(data2.user.first_name);
        $(object).find("span[name='last_name']").text(data2.user.last_name);
        $(object).find("span[name='email']").text(data2.user.email);
        $(object).find("span[name='mobile']").text(data2.mobile);
        $(object).find("span[name='address']").text(data2.address);
        $(object).attr('user_id', data2.user.id);
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
        console.log('editUserSubmmit: ');
        console.log(fd.entries());
        console.log(fd.get('first_name'));
        for (var p of fd) {
            console.log(p);
        }
        fileSendData("POST", $(this).attr('action'), fd, Bind, ErrorManagement, 'MemberEditUserInfoModalForm');
        //$('#news-photo-editor').css({ 'background-image': 'url()' });
        return false;
    });

    $('#changeUserPhotoModal').submit(function(event) {
        // do stuff
        event.preventDefault();
        var fd = new FormData();
        //var edit_form = $('#changeUserPhotoModal .custom-input :input');
        //console.log($(edit_form));
        fd.append('user_id', $('.detail-container').attr('user_id'));
        var photo = document.getElementById('personal_photo_change');
        fd.append('photo_name', photo.files[0].name);
        fd.append('photo', photo.files[0]);
        console.log('changeUserPhotoModal ');
        for (var p of fd) {
            console.log(p);
        }
        fileSendData("POST", $(this).attr('action'), fd, Bind, ErrorManagement, 'ChangeUserPhotoModalForm');
        //$('#news-photo-editor').css({ 'background-image': 'url()' });
        return false;
    });

    $('body').on('click', "#closeChangeUserPhotoModal", function() {
        console.log('in close modal edit onclick: ');
        var edit_form = $('#closeChangeUserPhotoModal .custom-input :input');
        $(edit_form).each(function(index) {
            //console.log('here');
            $(this).val('');
            console.log($(this));
        });
    });

    $('body').on('click', "#editFormCloseModal", function() {
        console.log('in close modal edit onclick: ');
        var edit_form = $('#edit_form .custom-input :input');
        $(edit_form).each(function(index) {
            //console.log('here');
            $(this).val('');
            console.log($(this));
        });
        // // result = '';
        // // result = member_panel_documents_array.find(doc => (doc.id == document_id));
        // // console.log(result);
        // $(".ok-btn-container ").click(function() {
        //     //SendData("POST", url_document_filter, data, Bind, ErrorManagement, 'MemberCategorySubmenuFilter');
        // });
    });

    $('body').on('click', ".result-item", function() {
        data = { 'user_id': $(this).attr('user_id') }
        SendData("POST", get_user_history_url, data, Bind, ErrorManagement, 'GetUserHistory', '');
        console.log('in search result onclick: ');
        console.log($(this).attr('user_id'));
        user = $(this).find('.detail .name').text();
        // console.log(user)
        $('#MemberDetailHistory').show(1000);
        $('#MemberCategoryMenu').show(1000);
        $('.info').show(1000);
        $('.detail-container .detail-bold').text(user);
        $('.detail-container').attr('user_id', $(this).attr('user_id')).attr('first_name', $(this).attr('first_name')).attr('last_name', $(this).attr('last_name')).attr('gender', $(this).attr('gender')).attr('age', $(this).attr('age')).attr('expertise', $(this).attr('expertise')).attr('uuid', $(this).attr('uuid'));
        $('.detail-container').find('span[name="position"]').text('بیکار ' + $(this).attr('expertise'));
        $('.detail-container').find('span[name="age|gender"]').text($(this).attr('gender') + $(this).attr('age'));
        $('.detail-container').find('span[name="membership"]').text($(this).attr('membership'));
        result = search_result.find(item => (item.user.id == $(this).attr('user_id')));
        result_item_click_user_of_member_page = result;
        console.log('result-item clicked: ' + result);
        // // result = '';
        // // result = member_panel_documents_array.find(doc => (doc.id == document_id));
        // // console.log(result);
        // $(".ok-btn-container ").click(function() {
        //     //SendData("POST", url_document_filter, data, Bind, ErrorManagement, 'MemberCategorySubmenuFilter');
        // });
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
    $("#editFiles").change(function() {
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
            $('#mydiv-edit-upload-files-container').append(tmp);
            // $(obj).find('.file-upload-name span').text(item.name)
            // $(obj).find('.file-upload-size').text(item.name)
        });
    });

    $('body').on('click', ".history-submit .text-submit-btn-container .text-submit-btn", function() {
        var submitted = $('.ql-editor').html();
        data = { 'history': submitted, 'title': 'Past Medical History', 'user_id': 1 };
        SendData("POST", 'http://praxo.ir/patientdoc/adddochistory/', data, Bind, ErrorManagement, 'AddMemberUserHistory', '');
    });
}

function UpdateChatMessages(room_id = '5bc88b40c23ffe0017680bbe'){
    //room_id  = $('.users-base-chat .os-padding .os-viewport .os-content .active').attr('room_id')
    result = rooms_messages_array.find(room => (room.room_id == room_id));
    $('.talk-base .os-padding .os-viewport .os-content .talk-inside-container div').remove().append(result.form);
    $('.talk-base .os-padding .os-viewport .os-content .talk-inside-container').append(result.form);
}



function Chat(winRef, data, from, type, url) {
    //var userChatCurrent = null;
    const socket = io('ws://185.211.58.216:3300/chatroom', {
        transports: ["websocket"],
        query: "userId=" + "6ed955c6506a53439be42c0afae02eef"
    });

    room1 = {'userId':user_id}
    axios.post('http://185.211.58.216:3020/getallmessageofuser/', room1).then(function(response){
        console.log(response.data);
        var data = response.data
        users_chats_array = response.data.rooms
        //var user_rooms_div = $('.chat-grouping').
        i = 0;
        $.each(response.data.rooms, function(i, item) {
            console.log(item);
            tmp = chat_user_chats_panel.replace('_ROOMID', item._id).replace('USERS.NAME', item.title).replace('USERS.ID', data.userId);
            $(tmp).insertBefore('.chat-grouping')
            form = ''
            $.each(item.messages, function(i1, item1) {
                time = luxon.DateTime.fromISO(item1.sent);
                time = time.toFormat("h':'mm a");
                if(item1.user == user_id){
                    tmp1 = chat_talk_main_sent_bubble.replace('BUBBLE-TEXT', item1.text).replace('BUBBLE-TIME', time);
                } else{
                    tmp1 = chat_talk_main_received_bubble.replace('BUBBLE-TEXT', item1.text).replace('BUBBLE-TIME', time);
                }
                form = tmp1 + form;
            });
            tmp2 = {'room_id': item._id, 'form':form}
            rooms_messages_array.push(tmp2);
        });

    }).catch(function(error){
        console.log(error);
    });

    
    $.each($('.user-chat'), function(i, item) {
        user_uuid = $(item).attr('user_id');
        data = {'user_uuid': user_uuid}
        data_for_next_function = {'user_id': user_uuid}
        SendData("POST", 'http://praxo.ir/getuserpic/' , data, Bind, ErrorManagement, 'ChatUsersListPics', data_for_next_function);
    });

    $.each($('.user-chat'), function(i, item) {
        user_uuid = $(item).attr('room_id');
        data = {'user_uuid': user_uuid}
        data_for_next_function = {'user_uuid': user_uuid}
        SendData("POST", 'http://praxo.ir/getuserpic/' , data, Bind, ErrorManagement, 'ChatRoomsListPics', data_for_next_function);
    });

    room = {'users':[{'userId':'6ed955c6506a53439be42c0afae02eef'}, {'userId':'b04965e6a9bb591f8f8a1adcb2c8dc39'}, {'userId':'98123fde012f5ff38b50881449dac91a'}, ]}
    console.dir(room);
    axios.post('http://185.211.58.216:3020/createroom/', room).then(function(response){
        console.log(response);
    }).catch(function(error){
        console.log(error);
    });

    $('body').on('click', ".users-base-chat .os-padding .os-viewport .os-content .user-chat", function(event) {
        $('.users-base-chat .os-padding .os-viewport .os-content .active').removeClass('active');
        $(this).addClass('active');
        room_id = $(this).attr('room_id');
        if(room_id != undefined){
            result = rooms_messages_array.find(room => (room.room_id == room_id));
            $('.talk-base .os-padding .os-viewport .os-content .talk-inside-container div').remove()
            $('.talk-base .os-padding .os-viewport .os-content .talk-inside-container').append(result.form);    
        }
        else{
            $('.talk-base .os-padding .os-viewport .os-content .talk-inside-container div').remove()
        }
        image = $('.users-base-chat .os-padding .os-viewport .os-content .active .photo-container-user-chat .photo-user-chat').css('background-image');
        console.log(image);
        $('.talk-photo').css('background-image', image);
    });


    $('body').on('click', ".bubble-checkbox", function() {
        $(this).toggleClass('active');
        $('.remove-chat-tool').toggleClass('active');
    });

    $('.emoji').click(function() {
        value = $(this).attr('value');
        $('#idChatInput').val($('#idChatInput').val() + value);
    });
    //UpdateChatMessages(room_id);

    $('.users-base-chat .os-padding .os-viewport .os-content .user-chat').first().addClass('active');
    image = $('.users-base-chat .os-padding .os-viewport .os-content .user-chat[user_id] .photo-container-user-chat .photo-user-chat').first().css('background-image');
    $('.talk-photo').css('background-image', 'url(' + image + ')');

    socket.on("connect", function() {
        console.log("conected");
    });
    socket.on('chat', function(data) {
        console.log('message recieve on chat event: ' + data);
        console.dir(data);
        Bind(window, data, 'Chat');

    });
    socket.on('disconnect', function() {
    });
    console.log(user_id);
    console.log(users);
    $('body').on('keyup', "#idSearchBoxMember", function() {
        //search_text = $(this).val();
        MemberSearch("#idResultContainer", "GET", '/member/search/', $(this).val(), 'Member');
    });

    $('body').on('click', ".user-chat", function() {
        username = $(this).find('.chat-content .name-chat-content .user-name-chat span').text();
        $('.talk-header .user-talk-header .user-name-talk span').text(username);
    });

    $('#chat_input_send_form').submit(function(event) {
        // do stuff
        event.preventDefault();
        room_id = $('.users-base-chat .os-padding .os-viewport .os-content .active').attr('room_id');
        chat_text = $(this).find('input').val();
        $('#idChatInput').val('');
        console.log(chat_text);
        console.log('chat_input_send_form: ');
        //socket.emit('chat', { hello: 'world' });
        socket.send(JSON.stringify({ 'groupId': room_id, 'message': chat_text }))
        return false;
    });
}


function News(winRef, data, from, type, url){

    $('body').on('click', ".news-detial", function() {
        $(".news-detial").removeClass("active");
        $(this).addClass("active");
        result = news_array.find(item => (item.id == $(this).attr('news_id')));
        // check if result is not defined and you must alert and handle this error
        time = luxon.DateTime.fromISO(result.created_at);
        time = time.toFormat("yyyy LLL dd '|' h':'mm a");
        $('.news-view-header .time-news-view').text(time);
        $('.text-news-view-container').text('');
        $('.text-news-view-container').append(result.description);
    });

    $('#AddNewsForm').submit(function(event) {
        // do stuff
        event.preventDefault();
        console.log('AddNewsSubmmit: ');
        var fd = new FormData();
        var edit_form = $(this).find('.custom-input :input');
        console.log($(edit_form));
        // $(edit_form).each(function(index) {
        //     //console.log('here');
        //     console.log($(this).attr('name'));
        //     console.log($(this).val());
        //     fd.append($(this).attr('name'), $(this).val());
        // });
        fd.append('title', $('#title').val());
        fd.append('description', $('#newsEditor p').text());
        var photo = document.getElementById('AddNewsFiles');
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
}

function BeforeSend(winref, data, from, url) {
    console.log('MemberUserHistory in BeforeSuccess: ' + from);
    $('.spinner-base').addClass('active');
    if (from == 'AddMemberUserHistory') {
        $('.spinner-base').addClass('active');
    }
}

function AfterSend(winref, data, from, url) {
    console.log('MemberUserHistory in AfterSend: ' + from);
    $('.spinner-base').removeClass('active');
    if (from == 'AddMemberUserHistory') {

        $('.spinner-base').removeClass('active');
    }
}

//
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