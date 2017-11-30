$(function () {
    generate_data();
});


function generate_data() {
    var form = $("#generate-data").find('form');
    form.find('button[type=submit]').click(function () {
        var token = Math.random().toString(36).substring(2) + $.now();
        var complete = false;

        $.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            data: form.serialize() + '&token=' + token,
            dataType: 'json',
            context: this,
            beforeSend: function () {
                $(this).prop('disabled', true);
                form.find("span[class^='validation-']").text('').hide();
            }
        }).done(function (error_messages) {
            if (error_messages !== null) {
                $.each(error_messages, function (name, error_message) {
                    $('span.validation-' + name).text(error_message).show();
                })
            }
        }).fail(function () {
            alert('加载失败，请重试！');
            window.location.reload(true);
        }).always(function () {
            complete = true;
            $(this).prop('disabled', false);
        });

        function get_console(line, is_complete) {
            var container = $("#console");
            var url = container.data('action');
            if (is_complete) {
                url = url + '?d=1';
            }

            $.ajax({
                url: url,
                type: 'post',
                data: {
                    token: token,
                    line: line
                },
                dataType: 'json',
                timeout: 60000,
                beforeSend: function(xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", container.find("input[name='_csrf_token']").val());
                    }
                }
            }).done(function (console) {
                if (console) {
                    if (line === 0) {
                        $.when(container.find('p').remove()).then(container.show());
                    }

                    $.each(console['messages'], function (i, message) {
                        if (container.scrollTop() + container.innerHeight() >= container[0].scrollHeight) {
                            container.append('<p>' + message + '</p>').scrollTop(container.prop("scrollHeight"));
                        } else {
                            container.append('<p>' + message + '</p>');
                        }

                    });

                    get_console(console['line'], complete);
                }
            })
        }

        get_console(0, false);

        return false;
    })
}