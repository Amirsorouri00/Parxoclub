    var toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'], // toggled buttons      
        ['blockquote'],
        [{ 'list': 'ordered' }, { 'list': 'bullet' }],
        [{ 'indent': '-1' }, { 'indent': '+1' }], // outdent/indent
        [{ 'align': [] }],
        [{ 'direction': 'rtl' }], // text direction
        [{ 'font': [] }],
        [{ 'size': ['small', false, 'large', 'huge'] }], // custom dropdown         
        ['image'], 
    ];
    var editor = new Quill('#historyEditor', {
        modules: {
            toolbar: toolbarOptions
        },
        theme: 'snow'
    });