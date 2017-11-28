$(function () {
    generate_data();
});


function generate_data() {
    var form = $("#generate-data").find('form');
    form.find('button[type=submit]').click(function () {
        $.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            data: form.serialize(),
            dataType: 'json',
            context: this,
            beforeSend: function () {
                $(this).prop('disabled', true);
                form.find("span[class^='validation-']").text('').hide();
            }
        }).done(function (error_messages) {
            if (error_messages === null) {
                alert('加载成功！');
            } else if (typeof error_messages === "object") {
                $.each(error_messages, function (name, error_message) {
                    $('span.validation-' + name).text(error_message).show();
                })
            } else {
                alert(error_messages);
            }
        }).fail(function () {

        }).always(function () {
            $(this).prop('disabled', false);
        });

        return false;
    })
}