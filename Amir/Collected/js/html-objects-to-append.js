search_object_to_append = "<div class='result-item'><div class='photo-container'><div class='photo'></div></div><div class='detail'><span class='name'> first_name last_name </span><span class='position'>Title/Position</span></div></div>";
document_categories_object_to_append = "<div class='column'><div class='main main_ajax_id' submit_or_submenu='submit2'><div class='icon icon_name'></div><div class='title'>classTitle</div><div class='expander'></div></div></div>";
document_categories_object_to_appendto_submenu = "<div class='item' parent='parent2' item_type='submenu'><span value='submenu_value'>● Sonography</span></div>";
general = '<div style={width:50;height:50; background-color:red}></div>'

calendar_after_sidenav_calendar_wrapper = '<div class="event-detial" id-modal="idShowEvent" modal-btn="show"> <div class="event-type-detail icon-labfill"></div> <div class="event-time-detail w-30"><span>event_time_range</span></div> <div class="event-title-detail w-50"><span>event_note</span></div> <div class="edit-event-detail-btn icon-edit" event_object="AmirEventObject" id-modal="idEditEvent" modal-btn="show"></div> <div class="remove-event-detail-btn icon-close" id-modal="idRemoveEvent" modal-btn="show"></div> </div>'
events_of_current_day_array = []

maintenance_user_info_fields_base = '<div id-modal="idEditUser" class="user-base-maintenance" user_id="2" modal-btn="show"> <div user_id="3" class="user-base-maintenance1 user-maintenance-photo-container"> <div class="user-maintenance-photo"></div> </div> <div user_id="4" class="user-base-maintenance1 user-maintenance-content-container"> <span class="user-maintenance-name">FirstName LastName</span> <span class="user-maintenance-title">Digestive Laboratory Supervisor</span> </div> <div user_id="5" id-modal="idRemoveUser" class="user-maintenance-remove icon-trashfill" modal-btn="show"></div> </div>'
maintenance_all_users_info_array = []
maintenance_add_user_photo = ''

url_to_get_token = '/patientdoc/gettoken/'
user_token = ''
url_document_filter = '/patientdoc/documentfilter/'

member_panel_documents_table_row = '<tr class="rowLink" document_id="praxo_doc_id"> <td class="notification clr-red icon-alertfill" style="font-size: 18px;"></td> <td>Document_Date</td> <td>Document_Title</td> <td>Document_Supervisor</td> <td>Nikan-East</td> </tr>'
member_panel_documents_array = []


member_panel_editoradd_document_modal_photos_info = '<div class="file-upload-row server-storage"> <div class="file-upload-stored icon-server"></div> <div class="thumbnail-container"><img src="{% static "img / nik2.png " %}"></div> <div class="file-upload-name"><span>FileName</span></div> <div class="file-upload-size">FileSize<span>kB</span></div> <div class="file-upload-trash icon-trashfill"></div> </div>'
member_personal_image_file_temp = ''

chat_talk_main_member_bubble = '<div class="received-bubble"> <div class="bubble-container"> <div class="bubble-text"> <span> BUBBLE-TEXT</span> </div> <div class="bubble-detail"> <span class="status"></span> <span class="time">BUBBLE-TIME</span> </div> </div> <div class="bubble-check"> <div class="bubble-checkbox"> <div class="bubble-checkbox-select"> <span class="bubble-checkbox-icon icon-check"></span> </div> </div> </div> </div>'