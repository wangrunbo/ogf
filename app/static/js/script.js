$(function () {
    ajaxSetup();
});

function ajaxSetup() {
    $.ajaxSetup({
        type: 'post',
        contentType: 'application/json',
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
}
