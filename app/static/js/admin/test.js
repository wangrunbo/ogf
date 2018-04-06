$(function () {
    ajaxSetup();
    test_post();
});

function test_post() {
    $(".fileupload").fileupload({
        url: url.upload_icon,
        dropZone: null,
    });
}

function ajaxSetup() {
    $.ajaxSetup({
        type: 'post',
        dataType: 'json',
        contentType:'application/json',
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
}
