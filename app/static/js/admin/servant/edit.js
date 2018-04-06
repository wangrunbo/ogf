$(function () {
    uploadIcon();
});

function uploadIcon() {
    // Upload Servant Icon
    $("#icon-upload").fileupload({
        url: url.upload_icon,
        dropZone: null,
        done: function (e, data) {
            if (data.result.success) {
                $("#icon-image").find('img').attr('src', data.result.icon + '?v=' + new Date().getTime());
            }
        },
        fail: function (e, data) {
            alert('网络异常！');
        }
    });
}
