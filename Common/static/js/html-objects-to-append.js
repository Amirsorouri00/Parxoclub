class DocCatAjaxActiveClass {

  constructor() {
    this._column_index = 1;
    this._item_index = 1;
    this._icon_name = 'icon-timefill'
    this._panel_id = '#MemberDetailHistory'
    this._hide_id = '#MemberPanelDocumentDetail'
  }

  get column() {
    return this._column_index;
  }

  get item() {
    return this._item_index;
  }

  get icon() {
    return this._icon_name;
  }  

  get panel_id(){
    return this._panel_id;
  }

  get show_hide(){

  }
}
var document_category_active_handler = new DocCatAjaxActiveClass();
RTL = ''
search_object_to_append = "<div class='result-item' uuid='__UUID' user_id='USER_ID' expertise='USER_EXPERTISE' prefix='USER_PREFIX' first_name='USER_FIRST_NAME' last_name='USER_LAST_NAME' gender='USER_GENDER' age='USER_AGE' membership='USER_MEMBERSHIP'><div class='photo-container'><div class='photo'></div></div><div class='detail'><span class='name'> first_name_text last_name_text </span><span class='position'>Title/Position</span></div></div>";
search_result = []
result_item_click_user_of_member_page = []
document_categories_object_to_append = "<div class='column' column_index = '_COLUMNINDEX'><div class='main main_ajax_id' icon_tmp = '_ICONNAME' menu_identifier='_MENUIDENTIFIER' submit_or_submenu='submit2'><div class='icon icon_name'></div><div class='title'>classTitle</div><div class='expander'></div></div></div>";
document_categories_object_to_appendto_submenu = "<div class='item' item_index = '_ITEMINDEX' parent='parent2' icon_parent_rtl='parent3' item_type='submenu'><span submenu_identifier='_SUBMENUIDENTIFIER' icon_tmp = '_ICONNAME' value='submenu_value'>● Sonography</span></div>";
general = '<div style={width:50;height:50; background-color:red}></div>'

calendar_after_sidenav_calendar_wrapper = '<div class="event-detial event-detail" event_id = "__EVENTID" id-modal="idShowEvent" modal-btn="show"> <div class="event-type-detail icon-labfill"></div> <div class="event-time-detail w-30"><span>event_time_range</span></div> <div class="event-title-detail w-50"><span>event_note</span></div> <div class="edit-event-detail-btn icon-edit" event_object="AmirEventObject" id-modal="idEditEvent" modal-btn="show"></div> <div class="remove-event-detail-btn icon-close" id-modal="idRemoveEvent" modal-btn="show"></div> </div>'
events_of_current_day_array = []

maintenance_user_info_fields_base = '<div id-modal="idEditUser" class="user-base-maintenance" user_id="2" modal-btn="show"> <div user_id="3" class="user-base-maintenance1 user-maintenance-photo-container"> <div class="user-maintenance-photo"></div> </div> <div user_id="4" class="user-base-maintenance1 user-maintenance-content-container"> <span class="user-maintenance-name">FirstName LastName</span> <span class="user-maintenance-title">Digestive Laboratory Supervisor</span> </div> <div user_id="5" id-modal="idRemoveUser" class="user-maintenance-remove icon-trashfill" modal-btn="show"></div> </div>'
maintenance_all_users_info_array = []
maintenance_add_user_photo = ''

test = '{{Token}}'
url_to_get_token = '/patientdoc/gettoken/'
//user_token = ''
url_document_filter = '/patientdoc/documentfilter/'

member_panel_documents_table_row = '<tr class="rowLink" document_id="praxo_doc_id" document_uuid="_DOCUMENTUUID"> <td class="notification clr-red icon-alertfill" style="font-size: 18px;"></td> <td>Document_Date</td> <td>Document_Title</td> <td>Document_Supervisor</td> <td>Nikan-East</td> </tr>'
member_panel_documents_array = []


member_panel_editoradd_document_modal_photos_info = '<div class="file-upload-row server-storage"> <div class="file-upload-stored icon-server"></div> <div class="thumbnail-container"><img src="{% static "img / nik2.png " %}"></div> <div class="file-upload-name"><span>FileName</span></div> <div class="file-upload-size">FileSize<span>kB</span></div> <div class="file-upload-trash icon-trashfill"></div> </div>'
member_personal_image_file_temp = ''

chat_talk_main_received_bubble = '<div class="received-bubble"> <div class="bubble-container"> <div class="bubble-text"> <span> BUBBLE-TEXT</span> </div> <div class="bubble-detail"> <span class="status"></span> <span class="time">BUBBLE-TIME</span> </div> </div> <div class="bubble-check"> <div class="bubble-checkbox"> <div class="bubble-checkbox-select"> <span class="bubble-checkbox-icon icon-check"></span> </div> </div> </div> </div>'
chat_talk_main_sent_bubble = '<div class="sent-bubble"> <div class="bubble-container"> <div class="bubble-text"> <span> BUBBLE-TEXT</span> </div> <div class="bubble-detail"> <span class="status"></span> <span class="time">BUBBLE-TIME</span> </div> </div> <div class="bubble-check"> <div class="bubble-checkbox"> <div class="bubble-checkbox-select"> <span class="bubble-checkbox-icon icon-check"></span> </div> </div> </div> </div>'
chat_scrollbar = ''
chat_user_chats_panel = '<div class="user-chat" room_id="_ROOMID" > <div class="photo-container-user-chat"> <div class="photo-user-chat"></div> </div> <div class="chat-content"> <div class="name-chat-content"> <div class="user-name-chat" user_id="USERS.ID"><span>USERS.NAME</span></div> <span class="user-status-chat icon-offline"></span> <span class="user-deliver-chat icon-delivered"></span> <span class="user-time-chat">3:15 pm</span> </div> <div class="text-chat-content"> <div class="text-chat"><span>As i said, photos will be send.</span></div> <span class="attach-chat icon-attach"></span> <div class="user-chat-badge-container"> <div class="user-chat-badge"> <span> 11 </span> </div> </div> </div> </div> </div>'
users_chats_array = []
rooms_messages_array = []


get_user_history_url = ''
member_history_document_section = '<div class="history-section" history_category_id = "_HISTORY_CATEGORY_ID"> <div class="history-section-title-container"> <div class="history-section-title"> _HISTORY_CATEGORY_TITLE </div> <div id-modal="idEditHistory" class="history-section-editor icon-edit" modal-btn="show"></div> </div> <div class="section-sep-container"> <div class="section-sep1"></div> <div class="section-sep2"></div> <div class="section-sep3"></div> <div class="section-sep4"></div> </div> <div class="section-content-container"> _HISTORY_CATEGORY_CONTEXT </div> </div>'
member_history_page_doctor_container = '<div class="dr-container"> <div class="dr-photo-container"></div> <div class="dr-content"> <div class="dr-name">_DOCTOR_PREFIX. _DOCTOR_LAST_NAME</div> <div class="dr-expertise"><span class="icon-dr-brain"></span>_DOCTOR_EXPERTISE</div> <!-- <div class="dr-location"><span class="icon-locationfill"></span>Clinic</div> --> </div> <div class="dr-record-count"><span class="icon-browsefill"></span>_DOCTOR_RECORD_NUMBER</div> </div>'

document_picture_carousel = '<div class="carousel-cell"> <div class="carousel-amir-img" style="background-image: url(_DOCUMENT_PICTURE);" id-modal="idMemberLargeCarousel" modal-btn="show"></div> </div>'
previously_uploaded_document_pictures = '<div class="file-upload-row server-storage"> <div class="file-upload-stored icon-server"></div> <div class="thumbnail-container"><img src=""></div> <div class="file-upload-name"><span>_FILENAME</span></div> <div class="file-upload-size">_FILESIZE<span>kB</span></div> <div class="file-upload-trash icon-trashfill"></div> </div>'
'{% static "img/nik2.png" %}'


news_objects_in_news_wrapper = '<div class="news-detial" news_id = "__NEWS_ID"> <div class="photo-container-news-detail"> <div class="photo-news-detail" ></div> </div> <div class="content-container-news-detail"> <div class="title-news-detail"><span> __NEWS_TITLE</span></div> <div class="content-news-detail"><span>__NEWS_DESCRIPTION</span> </div> <div class="time-news-detail"><span class="icon-time-news icon-time"></span><span>__NEWS_DATE</span></div> </div> </div>'
news_array = []