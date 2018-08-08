/* Documents upload widget */
$.fn.docFileUploader = function (filesToUpload, uploadList) {
    var fileIdCounter = 0;
    this.closest("input[doc-upload]").change(function (event) {

        for (var i = 0; i < event.target.files.length; i++) {
            fileIdCounter++;
            var file = event.target.files[i];
            var fileId = fileIdCounter;

            filesToUpload.push({
                id: fileId,
                file: file
            });

            if (file.size < 5*1024*1024)
            {
                var reader = new FileReader();
                reader.name = file.name;
                reader.size = file.size;
                reader.fileId = fileId;
                reader.onload = function(e) {
                    var target = e.target;
                    var elementRow = `
                    <div file-id="${target.fileId}" class="file-upload-row">
                        <div class="file-upload-stored"></div>
                        <div class="thumbnail-container"><img src="${target.result}"></div>
                        <div class="file-upload-name"><span>${target.name}</span></div>
                        <div class="file-upload-size">${filesize(target.size)}</div>
                        <div class="file-upload-trash icon-trashfill"></div>
                    </div>`;
                    
                    $(uploadList).append(elementRow);
                }
                
                reader.readAsDataURL(file);    
            }
            else
                notification.show('notif-bg-red', 'The maximum size for file upload is 5.0 MB!', 3000);
        };
        
        //reset the input to null - nice little chrome bug!
        event.target.value = null;
    });
    
    $(document).on("click", ".file-upload-remove", function (e) {
        e.preventDefault();
        
        var fileId = $(this).parent().attr("file-id");
        // loop through the files array and check if the name of that file matches FileName
        // and get the index of the match
        for (var i = 0; i < filesToUpload.length; ++i) {
            if (filesToUpload[i].id == fileId)
                filesToUpload.splice(i, 1);
        }
        $(this).parent().remove();
    });

    this.clear = function () {
        filesToUpload.splice(0, filesToUpload.length);
        $(uploadList).empty();
    }

    return this;
};

