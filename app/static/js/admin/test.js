$(function () {
    ajaxSetup();
    test_post();
});

function test_post() {
    $("#sub").click(function () {
        var value = $("#input").val();
        var value_1 = $("#input_1").val();

        $.ajax({
            url: url.edit_basic,
            data: JSON.stringify({
                'name': value,
                'star': value_1
            }),
            dataType: 'json'
        }).done(function (result) {
            console.log(result);
            console.log(typeof result);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        });
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
