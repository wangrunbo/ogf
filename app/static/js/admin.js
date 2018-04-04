$(function () {
    ajaxSetup();
    // init_sidebar();
});

function ajaxSetup() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
}

/**
 * Init SideBar
 */
function init_sidebar() {
    $(window).scroll(function () {
        var headerHeight = $('header').innerHeight();
        var contentHeight = $('.content').innerHeight();
        var sidebarHeight = $('.sidebar').height();
        var sidebarBottomPos = contentHeight - sidebarHeight;
        var trigger = $(window).scrollTop() - headerHeight;

      	if ($(window).scrollTop() >= headerHeight) {
          	$('.sidebar').addClass('fixed');
      	} else {
          	$('.sidebar').removeClass('fixed');
      	}

      	if (trigger >= sidebarBottomPos) {
          	$('.sidebar').addClass('bottom');
      	} else {
          	$('.sidebar').removeClass('bottom');
      	}
    });
}
