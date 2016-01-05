//Bootstrap tooltip
jQuery(function () {
  $("[rel='tooltip']").tooltip();
});

//Back To Top
jQuery(document).ready(function() {
  var offset = 220;
  var duration = 500;
  jQuery(window).scroll(function() {
    if (jQuery(this).scrollTop() > offset) {
      jQuery('.back-to-top').fadeIn(duration);
    } else {
      jQuery('.back-to-top').fadeOut(duration);
    }
  });
  jQuery('.back-to-top').click(function(event) {
    event.preventDefault();
    jQuery('html, body').animate({scrollTop: 0}, duration);
    return false;
  })
});

//Temporary undo class
(function($){
  $.fn.extend({ 
    removeTemporaryClass: function(className, duration) {
      var elements = this;
      setTimeout(function() {
        elements.addClass(className);
      }, duration);
      return this.each(function() {
        $(this).removeClass(className);
      });
    }
  });
})(jQuery);

//Expand / collapse
jQuery(document).ready(function() {
  jQuery('.colfield').on('click', function (event) {
    if (event.target !== this) return;
    event.preventDefault();
    $(this).toggleClass("semiCollapsed");
  })
});


function setStatus(text, status){
  $("#status").empty();
  $("#status").removeClass();
  $("#status").addClass("alert alert-"+status);
  $("#status").append(text);
}
